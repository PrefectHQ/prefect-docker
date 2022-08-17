"""Credential classes used to perform authenticated interactions with Docker"""

from typing import Any, Dict

from httpx import AsyncClient, AsyncHTTPTransport
from prefect.blocks.core import Block
from pydantic import Field


class DockerCredentials(Block):
    """
    Block used to manage Docker authentication.

    Args:
        base_url (str): The base URL to prepend to endpoints.
        unix_domain_socket (str): The path to the docker socket.

    Examples:
        Load stored Docker credentials:
        ```python
        from prefect_docker import DockerCredentials
        docker_credentials_block = DockerCredentials.load("BLOCK_NAME")
        ```
    """

    _block_type_name = "Docker Credentials"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/2IfXXfMq66mrzJBDFFCHTp/6d8f320d9e4fc4393f045673d61ab612/Moby-logo.png?h=250"  # noqa

    base_url: str = Field(
        "http://docker", description="The base URL to prepend to endpoints"
    )
    unix_domain_socket: str = Field(
        "/var/run/docker.sock", description="The path to the docker socket"
    )
    client_kwargs: Dict[str, Any] = Field(default_factory=dict)

    def get_client(self) -> AsyncClient:
        """
        Gets an authenticated Docker REST AsyncClient.

        Returns:
            An authenticated Docker REST AsyncClient

        Example:
            Gets an authenticated Docker REST AsyncClient.
            ```python
            from prefect import flow
            from prefect_docker import DockerCredentials

            @flow
            def example_get_client_flow():
                base_url = "http://docker"
                docker_credentials = DockerCredentials(base_url=base_url)
                client = docker_credentials.get_client()
                return client

            example_get_client_flow()
            ```
        """
        transport = AsyncHTTPTransport(uds=self.unix_domain_socket)
        client = AsyncClient(
            base_url=self.base_url, transport=transport, **self.client_kwargs
        )
        return client
