"""Module containing docker settings."""
from typing import Any, Dict, Optional

import docker
from prefect.blocks.core import Block
from pydantic import Field


class DockerSettings(Block):
    """
    Block used to manage settings for interacting with a Docker host.

    Attributes:
        base_url: URL to the Docker server, e.g. `unix:///var/run/docker.sock`
            or `tcp://127.0.0.1:1234`. If this is not set, the client will
            be configured from environment variables.
        version: The version of the API to use. Set to auto to
            automatically detect the server's version.
        timeout: Default timeout for API calls, in seconds.
        max_pool_size: The maximum number of connections to save in the pool.
        credstore_env: Override environment variables when calling the
            credential store process.
        client_kwargs: Additional keyword arguments to pass to
            `docker.from_env()` or `DockerClient`.
    """

    _block_type_name = "Docker Settings"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/2IfXXfMq66mrzJBDFFCHTp/6d8f320d9e4fc4393f045673d61ab612/Moby-logo.png?h=250"  # noqa
    _description = "Store settings for a interacting with a Docker host."

    base_url: Optional[str] = Field(
        default=None,
        description="URL to the Docker server.",
        title="Base URL",
        example="unix:///var/run/docker.sock",
    )
    version: str = Field(default="auto", description="The version of the API to use")
    timeout: Optional[int] = Field(
        default=None, description="Default timeout for API calls, in seconds."
    )
    max_pool_size: Optional[int] = Field(
        default=None,
        description="The maximum number of connections to save in the pool.",
    )
    credstore_env: Dict[str, Any] = Field(
        default_factory=dict,
        title="Credential Store Environment Variables",
        description=(
            "Override environment variables when calling "
            "the credential store process."
        ),
    )
    client_kwargs: Dict[str, Any] = Field(
        default_factory=dict,
        title="Additional Configuration",
        description=(
            "Additional keyword arguments to pass to "
            "`docker.from_env()` or `DockerClient`."
        ),
    )

    def get_client(self) -> docker.DockerClient:
        """
        Gets a Docker client to communicate with a Docker server.
        """
        client_kwargs = {
            "version": self.version,
            "timeout": self.timeout,
            "max_pool_size": self.max_pool_size,
            "credstore_env": self.credstore_env,
            **self.client_kwargs,
        }
        client_kwargs = {
            key: value for key, value in client_kwargs.items() if value is not None
        }
        if self.base_url is None:
            client_kwargs.pop("credstore_env")
            client = docker.from_env(**client_kwargs)
        else:
            client = docker.DockerClient(base_url=self.base_url, **client_kwargs)
        return client
