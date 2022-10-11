"""Integrations with Docker Images."""

from typing import List, Optional, Union

from docker.models.images import Image
from prefect import task

from prefect_docker.credentials import DockerRegistryCredentials
from prefect_docker.settings import DockerSettings


@task
def pull_docker_image(
    repository: str,
    docker_settings: Optional[DockerSettings] = None,
    docker_credentials: Optional[DockerRegistryCredentials] = None,
    tag: Optional[str] = None,
    platform: Optional[str] = None,
    all_tags: Optional[bool] = None,
) -> Union[Image, List[Image]]:
    """
    Pull an image of the given name and return it. Similar to the docker pull command.

    If all_tags is set, the tag parameter is ignored and all image tags will be pulled.

    Args:
        repository: The repository to pull.
        docker_settings: Docker Settings for interacting with a Docker host;
            provide either this or docker_credentials, not both.
        docker_credentials: Docker Credentials for interacting
            with a Docker host and pass `auth_config` automatically;
            provide either this or docker_credentials, not both.
        tag: The tag to pull; if not provided, it is set to latest.
        platform: Platform in the format os[/arch[/variant]].
        all_tags: Pull all image tags which will return a list of Images.

    Returns:
        The image that has been pulled, or images if `all_tags` is `True`.
    """
    if not (bool(docker_settings) ^ bool(docker_credentials)):
        raise ValueError(
            "Either docker_settings or docker_credentials must be "
            "provided, but not both"
        )

    if docker_credentials:
        docker_settings = docker_credentials.docker_settings
        auth_config = {
            "username": docker_credentials.username,
            "password": docker_credentials.password.get_secret_value(),
        }
    else:
        auth_config = None

    pull_kwargs = {
        "repository": repository,
        "tag": tag,
        "platform": platform,
        "all_tags": all_tags,
        "auth_config": auth_config,
    }

    client = docker_settings.get_client()
    image = client.images.pull(**pull_kwargs)
    return image
