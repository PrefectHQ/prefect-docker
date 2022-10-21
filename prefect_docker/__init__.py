from . import _version
from .host import DockerHost  # noqa
from .credentials import DockerRegistryCredentials  # noqa

__version__ = _version.get_versions()["version"]
