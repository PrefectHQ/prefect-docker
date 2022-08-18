"""
This is a module containing tasks for interacting with:
Docker distribution
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.570962

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def distribution_inspect(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Return image digest and platform information by contacting the registry.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/distribution/{name}/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | descriptor and platform information. |
    | 401 | Failed authentication or no image found. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/distribution/{name}/json"  # noqa
    responses = {
        200: "descriptor and platform information.",  # noqa
        401: "Failed authentication or no image found.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.GET,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents
