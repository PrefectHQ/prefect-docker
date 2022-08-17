"""
This is a module containing tasks for interacting with:
Docker build
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.726730

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def image_build(
    docker_credentials: "DockerCredentials",
    input_stream: str = None,
    dockerfile: str = "Dockerfile",
    t: str = None,
    extrahosts: str = None,
    remote: str = None,
    q: bool = False,
    nocache: bool = False,
    cachefrom: str = None,
    pull: str = None,
    rm: bool = True,
    forcerm: bool = False,
    memory: int = None,
    memswap: int = None,
    cpushares: int = None,
    cpusetcpus: str = None,
    cpuperiod: int = None,
    cpuquota: int = None,
    buildargs: str = None,
    shmsize: int = None,
    squash: bool = None,
    labels: str = None,
    networkmode: str = None,
    content_type: str = "application/x-tar",
    x_registry_config: str = None,
    platform: str = None,
    target: str = None,
    outputs: str = None,
) -> Dict[str, Any]:
    """
    Build an image from a tar archive with a `Dockerfile` in it.  The `Dockerfile`
    specifies how the image is built from the tar archive. It is typically in
    the archive's root, but can be at a different path or have a different name
    by specifying the `dockerfile` parameter. [See the `Dockerfile` reference
    for more information](/engine/reference/builder/).  The Docker daemon
    performs a preliminary validation of the `Dockerfile` before starting the
    build, and returns an error if the syntax is incorrect. After that, each
    instruction is run one-by-one until the ID of the new image is output.  The
    build is canceled if the client drops the connection by quitting or being
    killed.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        input_stream:
            A tar archive compressed with one of the following algorithms: identity
            (no compression), gzip, bzip2, xz.
        dockerfile:
            Path within the build context to the `Dockerfile`. This is ignored if
            `remote` is specified and points to an external
            `Dockerfile`.
        t:
            A name and optional tag to apply to the image in the `name:tag` format.
            If you omit the tag the default `latest` value is assumed.
            You can provide several `t` parameters.
        extrahosts:
            Extra hosts to add to /etc/hosts.
        remote:
            A Git repository URI or HTTP/HTTPS context URI. If the URI points to a
            single text file, the file’s contents are placed into a file
            called `Dockerfile` and the image is built from that file.
            If the URI points to a tarball, the file is downloaded by
            the daemon and the contents therein used as the context for
            the build. If the URI points to a tarball and the
            `dockerfile` parameter is also specified, there must be a
            file with the corresponding path inside the tarball.
        q:
            Suppress verbose build output.
        nocache:
            Do not use the cache when building the image.
        cachefrom:
            JSON array of images used for build cache resolution.
        pull:
            Attempt to pull the image even if an older image exists locally.
        rm:
            Remove intermediate containers after a successful build.
        forcerm:
            Always remove intermediate containers, even upon failure.
        memory:
            Set memory limit for build.
        memswap:
            Total memory (memory + swap). Set as `-1` to disable swap.
        cpushares:
            CPU shares (relative weight).
        cpusetcpus:
            CPUs in which to allow execution (e.g., `0-3`, `0,1`).
        cpuperiod:
            The length of a CPU period in microseconds.
        cpuquota:
            Microseconds of CPU time that the container can get in a CPU period.
        buildargs:
            JSON map of string pairs for build-time variables. Users pass these
            values at build-time. Docker uses the buildargs as the
            environment context for commands run via the `Dockerfile`
            RUN instruction, or for variable expansion in other
            `Dockerfile` instructions. This is not meant for passing
            secret values.  For example, the build arg `FOO=bar` would
            become `{'FOO':'bar'}` in JSON. This would result in the
            query parameter `buildargs={'FOO':'bar'}`. Note that
            `{'FOO':'bar'}` should be URI component encoded.  [Read more
            about the buildargs instruction.](/engine/reference/builder/
            arg).
        shmsize:
            Size of `/dev/shm` in bytes. The size must be greater than 0. If omitted
            the system uses 64MB.
        squash:
            Squash the resulting images layers into a single layer. *(Experimental
            release only.)*.
        labels:
            Arbitrary key/value labels to set on the image, as a JSON map of string
            pairs.
        networkmode:
            Sets the networking mode for the run commands during build. Supported
            standard values are: `bridge`, `host`, `none`, and
            `container:<name|id>`. Any other value is taken as a custom
            network's name or ID to which this container should connect
            to.
        content_type:

        x_registry_config:
            This is a base64-encoded JSON object with auth configurations for
            multiple registries that a build may refer to.  The key is a
            registry URL, and the value is an auth configuration object,
            [as described in the authentication section](
            section/Authentication). For example:  ``` {
            'docker.example.com': {     'username': 'janedoe',
            'password': 'hunter2'   },   'https://index.docker.io/v1/':
            {     'username': 'mobydock',     'password':
            'conta1n3rize14'   } } ```  Only the registry domain name
            (and port if not the default 443) are required. However, for
            legacy reasons, the Docker Hub registry must be specified
            with both a `https://` prefix and a `/v1/` suffix even
            though Docker will prefer to use the v2 registry API.
        platform:
            Platform in the format os[/arch[/variant]].
        target:
            Target build stage.
        outputs:
            BuildKit output configuration.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/build`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 400 | Bad parameter. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/build"  # noqa

    responses = {
        200: "no error.",  # noqa
        400: "Bad parameter.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "input_stream": input_stream,
        "dockerfile": dockerfile,
        "t": t,
        "extrahosts": extrahosts,
        "remote": remote,
        "q": q,
        "nocache": nocache,
        "cachefrom": cachefrom,
        "pull": pull,
        "rm": rm,
        "forcerm": forcerm,
        "memory": memory,
        "memswap": memswap,
        "cpushares": cpushares,
        "cpusetcpus": cpusetcpus,
        "cpuperiod": cpuperiod,
        "cpuquota": cpuquota,
        "buildargs": buildargs,
        "shmsize": shmsize,
        "squash": squash,
        "labels": labels,
        "networkmode": networkmode,
        "content_type": content_type,
        "x_registry_config": x_registry_config,
        "platform": platform,
        "target": target,
        "outputs": outputs,
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
async def build_prune(
    docker_credentials: "DockerCredentials",
    keep_storage: int = None,
    all: bool = None,
    filters: str = None,
) -> Dict[str, Any]:
    """
    Delete builder cache.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        keep_storage:
            Amount of disk space in bytes to keep for cache.
        all:
            Remove all types of build cache.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the list of build cache objects.  Available filters:  -
            `until=<duration>`: duration relative to daemon's time,
            during which build cache was not used, in Go's duration
            format (e.g., '24h') - `id=<id>` - `parent=<id>` -
            `type=<string>` - `description=<string>` - `inuse` -
            `shared` - `private`.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/build/prune`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/build/prune"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "keep_storage": keep_storage,
        "all": all,
        "filters": filters,
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
