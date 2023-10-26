try:
    from pytacite._version import __version__
    from pytacite._version import __version_tuple__
except ImportError:
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)


from pytacite.api import DOI
from pytacite.api import Client
from pytacite.api import ClientPrefix
from pytacite.api import ClientPrefixes
from pytacite.api import Clients
from pytacite.api import DOIs
from pytacite.api import Event
from pytacite.api import Events
from pytacite.api import Prefix
from pytacite.api import Prefixes
from pytacite.api import Provider
from pytacite.api import ProviderPrefix
from pytacite.api import ProviderPrefixes
from pytacite.api import Providers

# from pytacite.api import Report
# from pytacite.api import Reports
from pytacite.base import QueryError
from pytacite.base import config

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
