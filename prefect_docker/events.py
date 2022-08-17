"""
This is a module containing tasks for interacting with:
Docker events
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.731850

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def system_events(
    docker_credentials: "DockerCredentials",
    since: str = None,
    until: str = None,
    filters: str = None,
) -> Dict[str, Any]:
    """
    Stream real-time events from the server.  Various objects within Docker report
    events when something happens to them.  Containers report these events:
    `attach`, `commit`, `copy`, `create`, `destroy`, `detach`, `die`,
    `exec_create`, `exec_detach`, `exec_start`, `exec_die`, `export`,
    `health_status`, `kill`, `oom`, `pause`, `rename`, `resize`, `restart`,
    `start`, `stop`, `top`, `unpause`, `update`, and `prune`  Images report
    these events: `delete`, `import`, `load`, `pull`, `push`, `save`, `tag`,
    `untag`, and `prune`  Volumes report these events: `create`, `mount`,
    `unmount`, `destroy`, and `prune`  Networks report these events: `create`,
    `connect`, `disconnect`, `destroy`, `update`, `remove`, and `prune`  The
    Docker daemon reports these events: `reload`  Services report these events:
    `create`, `update`, and `remove`  Nodes report these events: `create`,
    `update`, and `remove`  Secrets report these events: `create`, `update`, and
    `remove`  Configs report these events: `create`, `update`, and `remove`  The
    Builder reports `prune` events.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        since:
            Show events created since this timestamp then stream new events.
        until:
            Show events created until this timestamp then stop streaming.
        filters:
            A JSON encoded value of filters (a `map[string][]string`) to process on
            the event list. Available filters:  - `config=<string>`
            config name or ID - `container=<string>` container name or
            ID - `daemon=<string>` daemon name or ID - `event=<string>`
            event type - `image=<string>` image name or ID -
            `label=<string>` image or container label -
            `network=<string>` network name or ID - `node=<string>` node
            ID - `plugin`=<string> plugin name or ID - `scope`=<string>
            local or swarm - `secret=<string>` secret name or ID -
            `service=<string>` service name or ID - `type=<string>`
            object to filter by, one of `container`, `image`, `volume`,
            `network`, `daemon`, `plugin`, `node`, `service`, `secret`
            or `config` - `volume=<string>` volume name.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/events`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | bad parameter. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/events"  # noqa

    responses = {
        200: "no error.",  # noqa
        400: "bad parameter.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "since": since,
        "until": until,
        "filters": filters,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.GET,
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
