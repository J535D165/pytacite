try:
    from pydatacite._version import __version__
    from pydatacite._version import __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)


from pydatacite.api import DOI
from pydatacite.api import Client
from pydatacite.api import ClientPrefix
from pydatacite.api import ClientPrefixes
from pydatacite.api import Clients
from pydatacite.api import DOIs
from pydatacite.api import Event
from pydatacite.api import Events
from pydatacite.api import Prefix
from pydatacite.api import Prefixes
from pydatacite.api import Provider
from pydatacite.api import ProviderPrefix
from pydatacite.api import ProviderPrefixes
from pydatacite.api import Providers

# from pydatacite.api import Report
# from pydatacite.api import Reports
from pydatacite.base import QueryError
from pydatacite.base import config

__all__ = [
    "DOI",
    "DOIs",
    "Client",
    "Clients",
    "ClientPrefix",
    "ClientPrefixes",
    "Event",
    "Events",
    "Prefix",
    "Prefixes",
    "Provider",
    "Providers",
    "ProviderPrefix",
    "ProviderPrefixes",
    # "Report",
    # "Reports",
    "QueryError",
    "config",
]
