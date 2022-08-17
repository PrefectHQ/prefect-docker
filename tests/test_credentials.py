from httpx import AsyncClient

from prefect_docker import DockerCredentials


def test_docker_credentials_get_client():
    client = DockerCredentials().get_client()
    assert isinstance(client, AsyncClient)
