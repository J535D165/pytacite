from pytacite.base import BaseDataCite
from pytacite.base import _pipe_method


class DOI(dict):
    """DataCite DOI object."""

    pass


class DOIs(BaseDataCite):
    resource_class = DOI

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)

    @_pipe_method
    def random(self):

        self._add_params("random", True)


class Client(dict):
    pass


class Clients(BaseDataCite):
    resource_class = Client

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)


class ClientPrefix(dict):
    pass


class ClientPrefixes(BaseDataCite):
    resource_class = ClientPrefix

    def _collection_name(self):
        return "client-prefixes"

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)


class Event(dict):
    pass


class Events(BaseDataCite):
    resource_class = Event

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)


class Prefix(dict):
    pass


class Prefixes(BaseDataCite):
    resource_class = Prefix

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)


class Provider(dict):
    pass


class Providers(BaseDataCite):
    resource_class = Provider

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)


class ProviderPrefix(dict):
    pass


class ProviderPrefixes(BaseDataCite):
    resource_class = ProviderPrefix

    def _collection_name(self):
        return "provider-prefixes"

    @_pipe_method
    def filter(self, **kwargs):

        for argument, value in kwargs.items():
            self._add_params(argument, value)

    @_pipe_method
    def query(self, *args, **kwargs):

        if len(args) > 1:
            raise ValueError("Maximal 1 positional argument possible")

        if len(args) == 1:
            self._add_params("query", args[0])
        else:
            self._add_params("query", kwargs)

    @_pipe_method
    def sort(self, by, ascending=True):

        if not ascending:
            by = f"-{by}"

        self._add_params("sort", by)
