from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_docker_settings():
    client = MagicMock()
    docker_settings = MagicMock()
    docker_settings.get_client.side_effect = lambda: client
    return docker_settings
