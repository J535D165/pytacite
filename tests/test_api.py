import json
from pathlib import Path

import pytest
import requests
from requests import HTTPError

import pytacite
from pytacite import DOI
from pytacite import ClientPrefixes
from pytacite import Clients
from pytacite import DOIs
from pytacite import Events
from pytacite import Prefixes
from pytacite import ProviderPrefixes
from pytacite import Providers

# from pytacite import Reports


def test_config():
    pytacite.config.email = "pytacite_github_unittests@example.com"

    assert pytacite.config.email == "pytacite_github_unittests@example.com"


@pytest.mark.parametrize(
    "class_",
    [DOIs, Clients, Providers, ClientPrefixes, Events, Prefixes, ProviderPrefixes],
)
def test_meta_entities(class_):

    _, m = class_().get(return_meta=True)
    assert "total" in m


def test_dois_params():

    assert len(DOIs(params={"provider-id": "datacite"}).get()) == 25
    assert len(DOIs(params={"prefix": "10.5438"}).get()) == 25


def test_dois():

    assert len(DOIs().filter(provider_id="datacite").get()) == 25
    assert len(DOIs().filter(prefix="10.5438").get()) == 25


def test_dois_count():

    assert DOIs().filter(prefix="10.5438").count() > 300


def test_per_page():

    assert len(DOIs().filter(prefix="10.5438").get(per_page=200)) == 200


def test_10_14454_dois():

    assert isinstance(DOIs()["10.14454/FXWS-0523"], DOI)
    assert DOIs()["10.14454/FXWS-0523"]["id"] == "10.14454/fxws-0523"


def test_work_error():

    with pytest.raises(HTTPError):
        DOIs()["NotAWorkID"]


def test_random_dois():

    d = DOIs().random().get(per_page=10)

    assert isinstance(d, list)
    assert len(d) == 10


def test_sample():

    url = "https://api.datacite.org/dois?prefix=10.5438&random=true"
    assert url == DOIs().filter(prefix="10.5438").random().url

    r = DOIs().filter(prefix="10.5438").random().get(per_page=4)
    assert len(r) == 4


def test_query_single():

    r = requests.get("https://api.datacite.org/dois?query=climate%20change").json()

    n = DOIs().query("climate change").count()

    assert n == r["meta"]["total"]


def test_query_count():

    r = requests.get(
        "https://api.datacite.org/dois?query=titles.title:(climate+change)"
    ).json()

    n = DOIs().query(titles={"title": "(climate+change)"}).count()

    assert n == r["meta"]["total"]


def test_query_get():

    r = DOIs().query(titles={"title": "(climate+change)"}).get()

    assert isinstance(r, list)


def test_query_multi():

    r = requests.get(
        "https://api.datacite.org/dois?query=creators.nameIdentifiers.nameIdentifierScheme:ORCID+publicationYear:2016+language:es"
    ).json()

    n = (
        DOIs()
        .query(creators={"nameIdentifiers": {"nameIdentifierScheme": "ORCID"}})
        .query(publicationYear=2016)
        .query(language="es")
        .count()
    )

    assert n == r["meta"]["total"]


def test_dois_multifilter():

    r = requests.get(
        "https://api.datacite.org/dois?certificate=CoreTrustSeal&resource-type-id=software"
    ).json()

    n1 = DOIs().filter(certificate="CoreTrustSeal", resource_type_id="software").count()
    n2 = (
        DOIs()
        .filter(certificate="CoreTrustSeal")
        .filter(resource_type_id="software")
        .count()
    )

    assert n1 == r["meta"]["total"]
    assert n2 == r["meta"]["total"]


def test_dois_url():

    url = "https://api.datacite.org/dois?prefix=10.5438&client_id=datacite.datacite"

    assert url == DOIs().filter(prefix="10.5438", client_id="datacite.datacite").url
    assert (
        url == DOIs().filter(prefix="10.5438").filter(client_id="datacite.datacite").url
    )

    assert DOIs().url == "https://api.datacite.org/dois"


def test_sort_dois():

    newest_first = (
        DOIs().query("climate").sort("created", ascending=False).get(per_page=1)
    )
    assert newest_first[0]["attributes"]["created"] >= "2023"

    oldest_first = (
        DOIs().query("climate").sort("created", ascending=True).get(per_page=1)
    )
    assert oldest_first[0]["attributes"]["created"] <= "2012"


# def test_query_error():

#     with pytest.raises(QueryError):
#         DOIs().filter(publicationYear_error=2020).get()


def test_manual_paging():

    # get the number of records
    n = DOIs().filter(prefix="10.5438").count()

    # example query
    query = DOIs().filter(prefix="10.5438")

    # set the page
    page = 1

    # store the results
    results = []

    # loop till page is None
    while page is not None:

        # get the results
        r, m = query.get(return_meta=True, per_page=100, page=page)

        # results
        results.extend(r)
        page = None if len(r) == 0 else m["page"] + 1

    assert len(results) == n


def test_number_paging():

    # get the number of records
    n = DOIs().filter(prefix="10.5438").count()

    # example query
    pager = DOIs().filter(prefix="10.5438").paginate(method="number", per_page=100)

    n_paging = 0
    for page in pager:

        n_paging += len(page)

    assert n_paging == n


def test_cursor_paging():

    # get the number of records
    n = DOIs().filter(prefix="10.5438").count()

    # example query
    pager = DOIs().filter(prefix="10.5438").paginate(per_page=100)

    n_paging = 0
    for page in pager:

        n_paging += len(page)

    assert n_paging == n


def test_cursor_paging_n_max():

    # example query
    pager = DOIs().filter(prefix="10.5438").paginate(per_page=50, n_max=200)

    n = 0
    for page in pager:

        n = n + len(page)

    assert n == 200


def test_cursor_paging_n_max_none():

    # get the number of records
    n = DOIs().filter(prefix="10.5438").count()

    # example query
    pager = DOIs().filter(prefix="10.5438").paginate(per_page=100, n_max=None)

    n_paging = 0
    for page in pager:

        n_paging += len(page)

    assert n_paging == n


def test_serializable(tmpdir):

    with open(Path(tmpdir, "test.json"), "w") as f:
        json.dump(DOIs()["10.14454/fxws-0523"], f)

    with open(Path(tmpdir, "test.json")) as f:
        assert "10.14454/fxws-0523" in json.load(f)["id"]


# def test_and_operator():

#     # https://github.com/J535D165/pytacite/issues/11
#     url = "https://api.datacite.org/dois?filter=institutions.country_code:tw,institutions.country_code:hk,institutions.country_code:us,publicationYear:2022"  # noqa

#     assert (
#         url
#         == DOIs()
#         .filter(
#             institutions={"country_code": ["tw", "hk", "us"]}, publicationYear=2022
#         )
#         .url
#     )
#     assert (
#         url
#         == DOIs()
#         .filter(institutions={"country_code": "tw"})
#         .filter(institutions={"country_code": "hk"})
#         .filter(institutions={"country_code": "us"})
#         .filter(publicationYear=2022)
#         .url
#     )
#     assert (
#         url
#         == DOIs()
#         .filter(institutions={"country_code": ["tw", "hk"]})
#         .filter(institutions={"country_code": "us"})
#         .filter(publicationYear=2022)
#         .url
#     )
