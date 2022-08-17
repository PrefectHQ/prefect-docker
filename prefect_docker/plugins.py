"""
This is a module containing tasks for interacting with:
Docker plugins
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.738020

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def plugin_list(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Returns information about installed plugins.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the plugin list.  Available filters:  -
            `capability=<capability name>` - `enable=<true>|<false>`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/plugins"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
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


@task
async def get_plugin_privileges(
    remote: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Get plugin privileges.

    Args:
        remote:
            The name of the plugin. The `:latest` tag is optional, and is the
            default if omitted.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/privileges`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/plugins/privileges"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "remote": remote,
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


@task
async def plugin_pull(
    remote: str,
    docker_credentials: "DockerCredentials",
    name: str = None,
    x_registry_auth: str = None,
    body: List = None,
) -> Dict[str, Any]:
    """
    Pulls and installs a plugin. After the plugin is installed, it can be enabled
    using the [`POST /plugins/{name}/enable` endpoint](
    operation/PostPluginsEnable).

    Args:
        remote:
            Remote reference for plugin to install.  The `:latest` tag is optional,
            and is used as the default if omitted.
        docker_credentials:
            Credentials to use for authentication with Docker.
        name:
            Local name for the pulled plugin.  The `:latest` tag is optional, and is
            used as the default if omitted.
        x_registry_auth:
            A base64url-encoded auth configuration to use when pulling a plugin from
            a registry.  Refer to the [authentication section](
            section/Authentication) for details.
        body:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/pull`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/plugins/pull"  # noqa

    responses = {
        204: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "remote": remote,
        "name": name,
        "x_registry_auth": x_registry_auth,
        "body": body,
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


@task
async def plugin_inspect(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Inspect a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | plugin is not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/json"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "plugin is not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
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


@task
async def plugin_delete(
    name: str,
    docker_credentials: "DockerCredentials",
    force: bool = False,
) -> Dict[str, Any]:
    """
    Remove a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        force:
            Disable the plugin before removing. This may result in issues if the
            plugin is in use by a container.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | plugin is not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "plugin is not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
        "force": force,
    }

    try:
        response = await execute_endpoint.fn(
            endpoint,
            docker_credentials,
            http_method=HTTPMethod.DELETE,
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


@task
async def plugin_enable(
    name: str,
    docker_credentials: "DockerCredentials",
    timeout: int = 0,
) -> Dict[str, Any]:
    """
    Enable a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        timeout:
            Set the HTTP client timeout (in seconds).

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/enable`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | plugin is not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/enable"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "plugin is not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
        "timeout": timeout,
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


@task
async def plugin_disable(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Disable a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/disable`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | plugin is not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/disable"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "plugin is not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
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


@task
async def plugin_upgrade(
    name: str,
    remote: str,
    docker_credentials: "DockerCredentials",
    x_registry_auth: str = None,
    body: List = None,
) -> Dict[str, Any]:
    """
    Upgrade a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        remote:
            Remote reference to upgrade to.  The `:latest` tag is optional, and is
            used as the default if omitted.
        docker_credentials:
            Credentials to use for authentication with Docker.
        x_registry_auth:
            A base64url-encoded auth configuration to use when pulling a plugin from
            a registry.  Refer to the [authentication section](
            section/Authentication) for details.
        body:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/upgrade`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 404 | plugin not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/upgrade"  # noqa
    responses = {
        204: "no error.",  # noqa
        404: "plugin not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
        "remote": remote,
        "x_registry_auth": x_registry_auth,
        "body": body,
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


@task
async def plugin_create(
    name: str,
    docker_credentials: "DockerCredentials",
    tar_context: str = None,
) -> Dict[str, Any]:
    """
    Create a plugin.

    Args:
        name:
            The name of the plugin. The `:latest` tag is optional, and is the
            default if omitted.
        docker_credentials:
            Credentials to use for authentication with Docker.
        tar_context:
            Path to tar containing plugin rootfs and manifest.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/plugins/create"  # noqa

    responses = {
        204: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
        "tar_context": tar_context,
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


@task
async def plugin_push(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Push a plugin to the registry.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/push`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | plugin not installed. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/push"  # noqa
    responses = {
        200: "no error.",  # noqa
        404: "plugin not installed.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "name": name,
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


@task
async def plugin_set(
    name: str,
    docker_credentials: "DockerCredentials",
    body: List = None,
) -> Dict[str, Any]:
    """
    Configure a plugin.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        body:


    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/plugins/{name}/set`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 204 | No error. |
    | 404 | Plugin not installed. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/plugins/{name}/set"  # noqa
    responses = {
        204: "No error.",  # noqa
        404: "Plugin not installed.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
        "body": body,
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
