"""
This is a module containing tasks for interacting with:
Docker commit
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.731235

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def image_commit(
    docker_credentials: "DockerCredentials",
    container_config: str = None,
    container: str = None,
    repo: str = None,
    tag: str = None,
    comment: str = None,
    author: str = None,
    pause: bool = True,
    changes: str = None,
) -> Dict[str, Any]:
    """
    Create a new image from a container.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        container_config:
            The container configuration.
        container:
            The ID or name of the container to commit.
        repo:
            Repository name for the created image.
        tag:
            Tag name for the create image.
        comment:
            Commit message.
        author:
            Author of the image (e.g., `John Hannibal Smith <hannibal@a-team.com>`).
        pause:
            Whether to pause the container before committing.
        changes:
            `Dockerfile` instructions to apply while committing.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/commit`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | no error. |
    | 404 | no such container. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/commit"  # noqa

    responses = {
        201: "no error.",  # noqa
        404: "no such container.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "container_config": container_config,
        "container": container,
        "repo": repo,
        "tag": tag,
        "comment": comment,
        "author": author,
        "pause": pause,
        "changes": changes,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.POST,
            params=params,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        helpful_error_response = (responses or {}).get(response.status_code, "")
        try:
            helpful_error_response += f"JSON response: {response.json()}"
        except Exception:
            pass
        if helpful_error_response:
            raise httpx.HTTPStatusError(
                helpful_error_response, request=exc.request, response=exc.response
            ) from exc
        else:
            raise

    result = response.json()
    return result
