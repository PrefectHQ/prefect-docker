from . import _version
from .host import DockerHost  # noqa

__version__ = _version.get_versions()["version"]
