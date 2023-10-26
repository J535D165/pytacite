# pydatacite

![PyPI](https://img.shields.io/pypi/v/pydatacite) [![DOI](https://zenodo.org/badge/557541347.svg)](https://zenodo.org/badge/latestdoi/557541347)

Pydatacite is a Python library for [DataCite](https://datacite.org/). Datacite is a non-profit organisation that provides persistent identifiers (DOIs) for research data and other research outputs. It holds a large index of metadata of outputs. DataCite offers an open and free [REST API](https://support.datacite.org/docs/api) to query metadata.
Pydatacite is a lightweight and thin Python interface to this API. Pydatacite aims to
stay as close as possible to the design of the original service.

The following features of DataCite are currently supported by pydatacite:

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

- **Pipe operations** - pydatacite can handle multiple operations in a sequence. This allows the developer to write understandable queries. For examples, see [code snippets](#code-snippets).
- **Permissive license** - [DataCite data is CC0 licensed](https://support.datacite.org/docs/datacite-data-file-use-policy) :raised_hands:. pydatacite is published under the MIT license.

## Installation

pydatacite requires Python 3.7 or later.

```sh
pip install pydatacite
```

## Getting started

Pydatacite offers support for:
[DOIs](https://support.datacite.org/reference/get_dois),
[Clients](https://support.datacite.org/reference/get_clients),
[ClientPrefixes](https://support.datacite.org/reference/get_client-prefixes),
[Events](https://support.datacite.org/reference/get_events),
[Prefixes](https://support.datacite.org/reference/get_prefixes),
[Providers](https://support.datacite.org/reference/get_providers), and
[ProviderPrefixes](https://support.datacite.org/reference/get_provider-prefixes).


```python
from pydatacite import DOIs, Clients, Events, Prefixes, ClientPrefixes, Providers, ProviderPrefixes
```

### Get single entity

Get a single DOI, Event, Prefix, ProviderPrefix from DataCite by the id.

```python
DOIs()["10.14454/FXWS-0523"]
```

The result is a `DOI` object, which is very similar to a dictionary. Find the available fields with `.keys()`.

For example, get the titles:

```python
DOIs()["10.14454/FXWS-0523"]["titles"]
```

```python
[{'title': 'DataCite Metadata Schema for the Publication and Citation of Research Data and Other Research Outputs v4.4'}]
```

It works similar for other resource collections.

```python
Prefixes()["10.12682"]
Events()["9a34e232-5b30-453b-a393-ea10a6ce565d"]
```

#### Get random DOIs

Get [random DOIs](https://support.datacite.org/docs/api-sampling).

```python
DOIs().random().get(per_page=10)
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
# 47824931
```

For lists of entities, you can return the result as well as the metadata. By default, only the results are returned.

```python
results, meta = DOIs().get(return_meta=True)
```

```python
print(meta)
{'count': 65073, 'db_response_time_ms': 16, 'page': 1, 'per_page': 25}
```

#### Filters and queries

DataCite makes use of filter and queries. Filters can narrow down queries and queries can help to search fields. See:

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
DOIs()
  .query(creators={"nameIdentifiers": {"nameIdentifierScheme": "ORCID"}})
  .query(publicationYear=2016)
  .query(language="es")
  .count()
```

#### Sort entity lists

```python
Clients().sort("created", ascending=True).get()
```

#### Logical expressions

See DataCite on [logical operators](https://support.datacite.org/docs/api-queries#boolean-operators) like AND, OR, and NOT.


#### Paging

DataCite offers two methods for paging: [basic paging](https://support.datacite.org/docs/pagination#page-number-up-to-10000-records) and [cursor paging](https://support.datacite.org/docs/pagination#cursor). Both methods are supported by
pydatacite.

##### Basic paging

Only the first 10,000 records can be retrieved with basic paging.

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


## Code snippets

A list of awesome use cases of the DataCite dataset.

### Creators of a dataset

```python
from pydatacite import DOIs

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

```python
from pydatacite import Clients

c = Clients().query("Zenodo").get()
print(c[0]["id"])
[{'id': 'cern.zenodo',
  'type': 'clients',
  'attributes': {'name': 'Zenodo',
   'symbol': 'CERN.ZENODO',
   'year': 2013,
   'alternateName': 'Research. Shared',
   'description': 'ZENODO builds and operates a simple and innovative service<...>',
   'language': ['en'],
   'clientType': 'repository',
   'domains': 'openaire.cern.ch,zenodo.org',
   're3data': 'https://doi.org/10.17616/R3QP53',
   'opendoar': None,
   'issn': {},
   'url': 'https://zenodo.org/',
   'created': '2013-01-28T12:07:48Z',
   'updated': '2020-06-26T12:22:29Z',
   'isActive': True},
  'relationships': {'provider': {'data': {'id': 'cern', 'type': 'providers'}},
   'prefixes': {'data': [{'id': '10.5281', 'type': 'prefixes'}]}}}]

DOIs() \
  .filter(client_id=c[0]["id"]) \
  .filter(resource_type_id="software") \
  .query(publicationYear=2016) \
  .get()
# 9720
```

### Number of dataverse instances

```python
from pydatacite import Clients

Clients() \
  .filter(software="dataverse") \
  .count()
# 31
```

## Experimental

### Authentication

DataCite experiments with authenticated requests at the moment. Authenticate your requests with

```python
import pydatacite

pydatacite.config.api_key = "<MY_KEY>"
```

## Alternatives

[datacite](https://pypi.org/project/datacite/) is a nice Python wrapper for Metadata Store API which is not covered by pydatacite.

R users can use [RDataCite](https://github.com/ropensci/rdatacite) library.

## License

[MIT](/LICENSE)

## Contact

Feel free to reach out with questions, remarks, and suggestions. The
[issue tracker](/issues) is a good starting point. You can also email me at
[jonathandebruinos@gmail.com](mailto:jonathandebruinos@gmail.com).
