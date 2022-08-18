"""
This is a module containing tasks for interacting with:
Docker version
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.553609

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def system_version(
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Returns the version of Docker that is running and various information about the
    system that Docker is running on.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/version`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/version"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.GET,
    )

    contents = _unpack_contents(response, responses)
    return contents
