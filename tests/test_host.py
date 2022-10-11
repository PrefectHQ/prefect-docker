from unittest.mock import MagicMock

from prefect_docker.host import DockerHost


def test_docker_host_get_client(mock_docker: MagicMock):
    settings_kwargs = dict(
        base_url="unix:///var/run/docker.sock",
        version="1.35",
        max_pool_size=8,
        client_kwargs={"tls": True},
        credstore_env=None,
    )
    settings = DockerHost(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.DockerClient.assert_called_once_with(
        base_url="unix:///var/run/docker.sock",
        version="1.35",
        max_pool_size=8,
        tls=True,
    )


def test_docker_host_get_client_from_env(mock_docker: MagicMock):
    settings_kwargs = dict(
        version="1.35",
        max_pool_size=8,
        client_kwargs={"assert_hostname": True},
        credstore_env=None,
    )
    settings = DockerHost(**settings_kwargs)
    for key, val in settings_kwargs.items():
        assert getattr(settings, key) == val

    settings.get_client()
    mock_docker.from_env.assert_called_once_with(
        version="1.35",
        max_pool_size=8,
        assert_hostname=True,
    )
