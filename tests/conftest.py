from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_docker_host():
    client = MagicMock()
    client.get.side_effect = lambda container_id: MagicMock()
    docker_host = MagicMock()
    docker_host.get_client.side_effect = lambda: client
    return docker_host
