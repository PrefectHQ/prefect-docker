"""
This is a module containing tasks for interacting with:
Docker session
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-18T00:04:16.571299

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

from prefect import task

from prefect_docker.rest import HTTPMethod, _unpack_contents, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def session(
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Start a new interactive session with a server. Session allows server to call
    back to the client for advanced capabilities.
    Hijacking  This endpoint hijacks the HTTP connection to HTTP2 transport that
    allows the client to expose gPRC services on that connection.  For example,
    the client sends this request to upgrade the connection:  ``` POST /session
    HTTP/1.1 Upgrade: h2c Connection: Upgrade ```  The Docker daemon responds
    with a `101 UPGRADED` response follow with the raw stream:  ``` HTTP/1.1 101
    UPGRADED Connection: Upgrade Upgrade: h2c ```.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/session`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 101 | no error, hijacking successful. |
    | 400 | bad parameter. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/session"  # noqa

    responses = {
        101: "no error, hijacking successful.",  # noqa
        400: "bad parameter.",  # noqa
        500: "server error.",  # noqa
    }

    response = await execute_endpoint.fn(
        endpoint,
        docker_credentials,
        http_method=HTTPMethod.POST,
    )

    contents = _unpack_contents(response, responses)
    return contents
