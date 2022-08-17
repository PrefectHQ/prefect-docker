from . import _version
from .credentials import DockerCredentials  # noqa

__version__ = _version.get_versions()["version"]
