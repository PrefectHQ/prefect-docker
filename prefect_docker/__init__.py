from . import _version
from .host import DockerHost  # noqa
from .credentials import DockerRegistryCredentials  # noqa
from .worker import DockerWorker  # noqa

from prefect._internal.compatibility.deprecated import (
    register_renamed_module,
)

register_renamed_module(
    "prefect_docker.projects", "prefect_docker.deployments", start_date="Jun 2023"
)


__version__ = _version.get_versions()["version"]
