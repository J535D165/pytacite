import functools
import logging
from urllib.parse import quote_plus

import requests

try:
    from pytacite._version import __version__
except ImportError:
    __version__ = "0.0.0"


class Config(dict):
    def __getattr__(self, key):
        return super().__getitem__(key)

    def __setattr__(self, key, value):
        return super().__setitem__(key, value)


config = Config(email=None, api_url="https://api.datacite.org")


def _pipe_method(func):
    @functools.wraps(func)
    def wrapper_decorator(self, *args, **kwargs):
        func(self, *args, **kwargs)
        return self

    return wrapper_decorator


def _flatten_key_value_dict(d, prefix=""):

    if isinstance(d, dict):

        t = []
        for k, v in d.items():
            if isinstance(v, list):
                t.extend([f"{prefix}.{k}:{i}" for i in v])
            else:
                new_prefix = f"{prefix}.{k}" if prefix else f"{k}"
                x = _flatten_key_value_dict(v, prefix=new_prefix)
                t.append(x)

        return "+".join(t)
    else:

        # workaround for bug https://groups.google.com/u/1/g/datacite-users/c/t46RWnzZaXc
        d = str(d).lower() if isinstance(d, bool) else d

        if prefix:
            return f"{prefix}:{d}"
        else:
            return str(d)


def _params_merge(params, add_params):

    for k, _v in add_params.items():
        if (
            k in params
            and isinstance(params[k], dict)
            and isinstance(add_params[k], dict)
        ):
            _params_merge(params[k], add_params[k])
        elif (
            k in params
            and not isinstance(params[k], list)
            and isinstance(add_params[k], list)
        ):
            # example: params="a" and add_params=["b", "c"]
            params[k] = [params[k]] + add_params[k]
        elif (
            k in params
            and isinstance(params[k], list)
            and not isinstance(add_params[k], list)
        ):
            # example: params=["b", "c"] and add_params="a"
            params[k] = params[k] + [add_params[k]]
        elif k in params:
            params[k] = [params[k], add_params[k]]
        else:
            params[k] = add_params[k]


class QueryError(ValueError):
    pass


class Paginator:
    def __init__(self, link, endpoint_class=None, n_max=None):

        self.endpoint_class = endpoint_class
        self.link = link
        self.n_max = n_max

    def __iter__(self):

        self.n = 0

        return self

    def _is_max(self):
        if self.n_max and self.n >= self.n_max:
            return True
        return False

    def __next__(self):

        if self.link is None or self._is_max():
            raise StopIteration

        res_json = self.endpoint_class._get_raw(self.link)
        results = [self.endpoint_class.resource_class(ent) for ent in res_json["data"]]

        try:
            self.link = res_json["links"]["next"]
        except KeyError:
            self.link = None

        self.n = self.n + len(results)

        return results


class BaseDataCite:
    """Base class for DataCite objects."""

    def __init__(self, params=None):

        self.params = params

    def _collection_name(self):

        return self.__class__.__name__.lower()

    def _full_collection_name(self):

        return config.api_url + "/" + self._collection_name()

    def __getattr__(self, key):

        return getattr(self, key)

    def __getitem__(self, record_id):

        url = self._full_collection_name() + "/" + record_id
        res_json = self._get_raw(url)["data"]

        return self.resource_class(res_json)

    @property
    def url(self):

        if not self.params:
            return self._full_collection_name()

        l_params = []
        for k, v in self.params.items():

            if v is None:
                pass
            elif isinstance(v, list):
                v_quote = [quote_plus(q) for q in v]
                l_params.append(k + "=" + ",".join(v_quote))
            elif k in ["filter", "query", "sort", "random"]:
                l_params.append(k + "=" + _flatten_key_value_dict(v))
            else:
                l_params.append(k + "=" + quote_plus(str(v)))

        if l_params:
            return self._full_collection_name() + "?" + "&".join(l_params)

        return self._full_collection_name()

    def _add_params(self, argument, new_params):

        if self.params is None:
            self.params = {argument: new_params}
        elif argument in self.params and isinstance(self.params[argument], dict):
            _params_merge(self.params[argument], new_params)
        else:
            self.params[argument] = new_params

        logging.debug("Params updated:", self.params)

    def _get_raw(self, url):

        res = requests.get(
            url,
            headers={"User-Agent": "pytacite/" + __version__, "email": config.email},
        )

        # handle query errors
        if res.status_code == 403:
            res_json = res.json()
            if (
                isinstance(res_json["error"], str)
                and "query parameters" in res_json["error"]
            ):
                raise QueryError(res_json["message"])
        res.raise_for_status()

        return res.json()

    def get(self, return_meta=False, page=None, per_page=None, cursor=None):

        if per_page is not None and (per_page < 1 or per_page > 200):
            raise ValueError("per_page should be a number between 1 and 200.")

        self._add_params("page[size]", per_page)
        self._add_params("page[number]", page)
        self._add_params("page[cursor]", cursor)

        res_json = self._get_raw(self.url)
        results = [self.resource_class(ent) for ent in res_json["data"]]

        # return result and metadata
        if return_meta:
            return results, res_json["meta"]
        else:
            return results

    def count(self):
        _, m = self.get(return_meta=True, per_page=1)

        return m["total"]

    def paginate(self, method="cursor", page=1, per_page=None, cursor="*", n_max=10000):
        """Used for paging results of large responses using cursor paging.

        DataCite offers two methods for paging: basic paging and cursor paging.
        Both methods are supported by pytacite, although cursor paging seems to be
        easier to implement and less error-prone.

        Args:
            per_page (_type_, optional): Entries per page to return. Defaults to None.
            cursor (str, optional): _description_. Defaults to "*".
            n_max (int, optional): Number of max results (not pages) to return.
                Defaults to 10000.

        Returns:
            Paginator: Iterator to use for returning and processing each page
            result in sequence.
        """

        self._add_params("page[size]", per_page)

        if method == "cursor":
            self._add_params("page[cursor]", cursor)
        elif method == "number":
            self._add_params("page[number]", page)
        else:
            raise ValueError("Method should be 'cursor' or 'number'")

        return Paginator(link=self.url, endpoint_class=self, n_max=n_max)
