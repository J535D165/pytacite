# pytacite

![PyPI](https://img.shields.io/pypi/v/pytacite) [![DOI](https://zenodo.org/badge/557541347.svg)](https://zenodo.org/badge/latestdoi/557541347)

Pytacite is a Python library for [DataCite](https://datacite.org/). DataCite is a non-profit organisation that provides persistent identifiers (DOIs) for research data and other research outputs. It holds a large index of metadata of outputs. DataCite offers an open and free [REST API](https://support.datacite.org/docs/api) to query metadata.
Pytacite is a lightweight and thin Python interface to this API. Pytacite aims to
stay as close as possible to the design of the original service.

The following features of DataCite are currently supported by pytacite:

- [x] Get single entities
- [x] Filter and query entities
- [x] Sort entities
- [x] Sample entities
- [x] Pagination
- [ ] [Usage reports](https://support.datacite.org/docs/usage-reports-api-guide)
- [ ] Authentication
- [ ] Side-load associations with include

We aim to cover the entire API, and we are looking for help. We are welcoming Pull Requests.

## Key features

- **Pipe operations** - pytacite can handle multiple operations in a sequence. This allows the developer to write understandable queries. For examples, see [code snippets](#code-snippets).
- **Permissive license** - [DataCite data is CC0 licensed](https://support.datacite.org/docs/datacite-data-file-use-policy) :raised_hands:. pytacite is published under the MIT license.

## Installation

pytacite requires Python 3.8 or later.

```sh
pip install pytacite
```

## Getting started

Pytacite offers support for:
[DOIs](https://support.datacite.org/reference/get_dois),
[Clients](https://support.datacite.org/reference/get_clients),
[ClientPrefixes](https://support.datacite.org/reference/get_client-prefixes),
[Events](https://support.datacite.org/reference/get_events),
[Prefixes](https://support.datacite.org/reference/get_prefixes),
[Providers](https://support.datacite.org/reference/get_providers), and
[ProviderPrefixes](https://support.datacite.org/reference/get_provider-prefixes).


```python
from pytacite import DOIs, Clients, Events, Prefixes, ClientPrefixes, Providers, ProviderPrefixes
```

### Get single entity

Get a single DOI, Event, Prefix, ProviderPrefix from DataCite by the id.

```python
DOIs()["10.14454/FXWS-0523"]
```

The result is a `DOI` object, which is very similar to a dictionary. Find the
available fields with `.keys()`. Most interesting attributes are stored in
the `"attributes"` field.

For example, get the titles:

```python
DOIs()["10.14454/FXWS-0523"]["attributes"]["titles"]
```

```python
[{'title': 'DataCite Metadata Schema for the Publication and Citation of Research Data and Other Research Outputs v4.4'}]
```

It works similar for other resource collections.

```python
Prefixes()["10.12682"]
Events()["9a34e232-5b30-453b-a393-ea10a6ce565d"]
```

### Get lists of entities

```python
results = DOIs().get()
```

For lists of entities, you can also `count` the number of records found
instead of returning the results. This also works for search queries and
filters.

```python
DOIs().count()
# 50869984
```

For lists of entities, you can return the result as well as the metadata. By default, only the results are returned.

```python
results, meta = DOIs().get(return_meta=True)
```

```python
print(meta)
{'total': 50869984,
 'totalPages': 400,
 'page': 1,
 'states': [{'id': 'findable', 'title': 'Findable', 'count': 50869984}],
 'resourceTypes': [{'id': 'dataset', 'title': 'Dataset', 'count': 15426144}, <...>]
 <...>
 'subjects': [{'id': 'FOS: Biological sciences',
   'title': 'Fos: Biological Sciences',
   'count': 3304486}, <...>],
 'citations': [],
 'views': [],
 'downloads': []}
 ```

#### Filters and queries

DataCite makes use of filter and queries. Filters can narrow down queries `
(~.~)` and queries can help to search fields. See:

- Filtering: https://support.datacite.org/docs/api-queries#filtering-list-responses
- Making Queries: https://support.datacite.org/docs/api-queries#making-queries

The following example returns records created in the year 2020 on Dryad.

```python
DOIs().filter(created=2020, client_id="dryad.dryad").get()
```

which is identical to:

```python
DOIs().filter(created=2020).filter(client_id="dryad.dryad").get()
```

Queries can work in a similar fashion and can be applied to all fields. For example, search for records with `climate change` in the title.

```python
DOIs().query("climate change").get()
```

Important to note, this returns [a list of all the DOI records that contain the phrases `climate` and `change` in their metadata](https://support.datacite.org/docs/api-queries#making-queries) (potential mistake in DataCite documentation).


#### Nested attribute filters

Some attribute filters are nested and separated with dots by DataCite. For
example, filter on [`creators.nameIdentifiers.nameIdentifierScheme`](https://support.datacite.org/docs/api-queries#field-names).

In case of nested attribute filters, use a dict to build the query.

```python
DOIs() \
  .query(creators={"nameIdentifiers": {"nameIdentifierScheme": "ORCID"}}) \
  .query(publicationYear=2016) \
  .query(language="es") \
  .count()
# 562
```

#### Sort entity lists

```python
Clients().sort("created", ascending=True).get()
```

#### Logical expressions

See DataCite on [logical operators](https://support.datacite.org/docs/api-queries#boolean-operators) like AND, OR, and NOT.


#### Paging

DataCite offers two methods for paging: [basic paging](https://support.datacite.org/docs/pagination#page-number-up-to-10000-records) and [cursor paging](https://support.datacite.org/docs/pagination#cursor). Both methods are supported by
pytacite.

##### Basic (offset) paging

Only the first 10,000 records can be retrieved with basic (offset)paging.

```python
pager = DOIs().filter(prefix="10.5438").paginate(method="number", per_page=100)

for page in pager:
    print(len(page))
```

##### Cursor paging

Use `paginate()` for paging results. By default, `paginate`s argument `n_max`
is set to 10000. Use `None` to retrieve all results.

```python
pager = DOIs().filter(prefix="10.5438").paginate(per_page=100)

for page in pager:
    print(len(page))
```

> Looking for an easy method to iterate the records of a pager?

```python
from itertools import chain
from pytacite import DOIs

query = DOIs().filter(prefix="10.5438")

for record in chain(*query.paginate(per_page=100)):
    print(record["id"])
```

#### Get random DOIs

Get [random DOIs](https://support.datacite.org/docs/api-sampling). Somehow, this has very slow response times (caused by DataCite).

```python
DOIs().random().get(per_page=10)
```

## Code snippets

A list of awesome use cases of the DataCite dataset.

### Creators of a dataset

```python
from pytacite import DOIs

w = DOIs()["10.34894/HE6NAQ"]

w["attributes"]["creators"]
```

### Get the works of a single creator

Work in progress: get rid of quotes.

```python
DOIs() \
  .query(creators={"nameIdentifiers": {"nameIdentifier": "\"https://orcid.org/0000-0001-7736-2091\""}}) \
  .get()
```

### Software published on Zenodo in 2016

Resources:
- https://support.datacite.org/reference/get_clients
- https://support.datacite.org/reference/get_dois

Get the DataCite identifier of the client first:
```python
from pytacite import Clients

c = Clients().query("Zenodo").get()
print(c[0]["id"])
# cern.zenodo
```

Filter the DOIs on the client identifier. It can be a bit confusing when to use `filter` and `query` here.

```python
DOIs() \
  .filter(client_id=c[0]["id"]) \
  .filter(resource_type_id="software") \
  .query(publicationYear=2016) \
  .get()
# 9720
```

### Number of repositories running on Dataverse software

```python
from pytacite import Clients

Clients() \
  .filter(software="dataverse") \
  .count()
# 31
```

## Alternatives

[datacite](https://pypi.org/project/datacite/) is a nice Python wrapper for Metadata Store API which is not covered by pytacite.

R users can use [RDataCite](https://github.com/ropensci/rdatacite) library.

## License

[MIT](/LICENSE)

## Contact

> This library is a community contribution. The authors of this Python library aren't affiliated with DataCite.

Feel free to reach out with questions, remarks, and suggestions. The
[issue tracker](/issues) is a good starting point. You can also email me at
[jonathandebruinos@gmail.com](mailto:jonathandebruinos@gmail.com).
