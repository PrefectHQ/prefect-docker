"""
This is a module containing tasks for interacting with:
Docker auth
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.553120

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def system_auth(
    docker_credentials: "DockerCredentials",
    auth_config: str = None,
) -> Dict[str, Any]:
    """
    Validate credentials for a registry and, if available, get an identity token for
    accessing the registry without password.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        auth_config:
            Authentication to check.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/auth`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | An identity token was generated successfully. |
    | 204 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/auth"  # noqa

    responses = {
        200: "An identity token was generated successfully.",  # noqa
        204: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "auth_config": auth_config,
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
        params=params,
    )

    contents = _unpack_contents(response, responses)
    return contents
