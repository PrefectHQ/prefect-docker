from unittest.mock import MagicMock

import pytest
from prefect.logging import disable_run_logger

from prefect_docker.images import pull_docker_image


class TestPullDockerImage:
    def test_tag_and_all_tags(self, mock_docker: MagicMock):
        pull_kwargs = dict(repository="prefecthq/prefect", tag="latest", all_tags=True)
        with pytest.raises(
            ValueError, match="Cannot pass `tags` and `all_tags` together"
        ):
            with disable_run_logger():
                pull_docker_image.fn(**pull_kwargs)

    def test_defaults(self, mock_docker: MagicMock):
        with disable_run_logger():
            image_id = pull_docker_image.fn(repository="prefecthq/prefect")
        assert image_id == "id_1"

    def test_host(self, mock_docker_host: MagicMock):
        pull_kwargs = dict(
            repository="prefecthq/prefect",
        )
        with disable_run_logger():
            image_id = pull_docker_image.fn(docker_host=mock_docker_host, **pull_kwargs)
        assert image_id == "id_1"

        client = mock_docker_host.get_client()
        client.images.pull.assert_called_once_with(**pull_kwargs)

    def test_login(
        self, mock_docker_host: MagicMock, mock_docker_registry_credentials: MagicMock
    ):
        pull_kwargs = dict(
            repository="prefecthq/prefect",
            tag="latest",
        )
        with disable_run_logger():
            image_id = pull_docker_image.fn(
                docker_host=mock_docker_host,
                docker_registry_credentials=mock_docker_registry_credentials,
                **pull_kwargs
            )
        assert image_id == "id_1"

        client = mock_docker_host.get_client()
        client.images.pull.assert_called_once_with(**pull_kwargs)
        assert client._authenticated

    def test_all_tags(self, mock_docker_host: MagicMock):
        pull_kwargs = dict(repository="prefecthq/prefect", all_tags=True)
        with disable_run_logger():
            image_ids = pull_docker_image.fn(
                docker_host=mock_docker_host, **pull_kwargs
            )
        assert image_ids == ["id_1", "id_2"]

        client = mock_docker_host.get_client()
        client.images.pull.assert_called_once_with(**pull_kwargs)
