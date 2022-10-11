"""Module containing docker credentials."""
import docker
from prefect.blocks.core import Block
from pydantic import Field, SecretStr


class DockerRegistryCredentials(Block):
    """
    Block used to manage credentials for interacting with a Docker Registry.
    """

    _block_type_name = "Docker Registry"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/2IfXXfMq66mrzJBDFFCHTp/6d8f320d9e4fc4393f045673d61ab612/Moby-logo.png?h=250"  # noqa
    _description = "Store credentials for interacting with a Docker Registry."

    username: str = Field(
        default=..., description="The username to log into the registry with."
    )
    password: SecretStr = Field(
        default=..., description="The password to log into the registry with."
    )
    registry_url: str = Field(
        default=...,
        description=(
            'The URL to the registry. Generally, "http" or "https" can be omitted.',
        ),
    )
    reauth: bool = Field(
        default=True,
        description="Whether or not to reauthenticate on each interaction.",
    )

    def login(self, client: docker.DockerClient):
        """
        Logs into the Docker registry.
        """
        client.login(
            username=self.username,
            password=self.password.get_secret_value(),
            registry=self.registry_url,
            # See https://github.com/docker/docker-py/issues/2256 for information on
            # the default value for reauth.
            reauth=self.reauth,
        )
