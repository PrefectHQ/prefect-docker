"""
This is a module containing tasks for interacting with:
Docker images
"""

# This module was auto-generated using prefect-collection-generator so
# manually editing this file is not recommended. If this module
# is outdated, rerun scripts/generate.py.

# OpenAPI spec: v1.41.yaml
# Updated at: 2022-08-17T00:00:42.725406

from typing import TYPE_CHECKING, Any, Dict, List, Union  # noqa

import httpx
from prefect import task

from prefect_docker.rest import HTTPMethod, execute_endpoint

if TYPE_CHECKING:
    from prefect_docker import DockerCredentials


@task
async def image_list(
    docker_credentials: "DockerCredentials",
    all: bool = False,
    filters: str = None,
    digests: bool = False,
) -> Dict[str, Any]:
    """
    Returns a list of images on the server. Note that it uses a different, smaller
    representation of an image than inspecting a single image.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        all:
            Show all images. Only images from a final layer (no children) are shown
            by default.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the images list.  Available filters:  -
            `before`=(`<image-name>[:<tag>]`,  `<image id>` or
            `<image@digest>`) - `dangling=true` - `label=key` or
            `label='key=value'` of an image label -
            `reference`=(`<image-name>[:<tag>]`) - `since`=(`<image-
            name>[:<tag>]`,  `<image id>` or `<image@digest>`).
        digests:
            Show digest information as a `RepoDigests` field on each image.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | Summary image data for the images matching the query. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/images/json"  # noqa

    responses = {
        200: "Summary image data for the images matching the query.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "all": all,
        "filters": filters,
        "digests": digests,
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
async def image_create(
    docker_credentials: "DockerCredentials",
    from_image: str = None,
    from_src: str = None,
    repo: str = None,
    tag: str = None,
    message: str = None,
    input_image: str = None,
    x_registry_auth: str = None,
    changes: List = None,
    platform: str = None,
) -> Dict[str, Any]:
    """
    Create an image by either pulling it from a registry or importing it.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        from_image:
            Name of the image to pull. The name may include a tag or digest. This
            parameter may only be used when pulling an image. The pull
            is cancelled if the HTTP connection is closed.
        from_src:
            Source to import. The value may be a URL from which the image can be
            retrieved or `-` to read the image from the request body.
            This parameter may only be used when importing an image.
        repo:
            Repository name given to an image when it is imported. The repo may
            include a tag. This parameter may only be used when
            importing an image.
        tag:
            Tag or digest. If empty when pulling an image, this causes all tags for
            the given image to be pulled.
        message:
            Set commit message for imported image.
        input_image:
            Image content if the value `-` has been specified in fromSrc query
            parameter.
        x_registry_auth:
            A base64url-encoded auth configuration.  Refer to the [authentication
            section](
            section/Authentication) for details.
        changes:
            Apply `Dockerfile` instructions to the image that is created, for
            example: `changes=ENV DEBUG=true`. Note that `ENV
            DEBUG=true` should be URI component encoded.  Supported
            `Dockerfile` instructions:
            `CMD`|`ENTRYPOINT`|`ENV`|`EXPOSE`|`ONBUILD`|`USER`|`VOLUME`|`WORKDIR`.
        platform:
            Platform in the format os[/arch[/variant]].

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/create`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 404 | repository does not exist or no read access. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/images/create"  # noqa

    responses = {
        200: "no error.",  # noqa
        404: "repository does not exist or no read access.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "from_image": from_image,
        "from_src": from_src,
        "repo": repo,
        "tag": tag,
        "message": message,
        "input_image": input_image,
        "x_registry_auth": x_registry_auth,
        "changes": changes,
        "platform": platform,
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
async def image_inspect(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Return low-level information about an image.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}/json`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | No such image. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/images/{name}/json"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "No such image.",  # noqa
        500: "Server error.",  # noqa
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
async def image_history(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Return parent layers of an image.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}/history`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | List of image layers. |
    | 404 | No such image. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/images/{name}/history"  # noqa
    responses = {
        200: "List of image layers.",  # noqa
        404: "No such image.",  # noqa
        500: "Server error.",  # noqa
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
async def image_push(
    name: str,
    x_registry_auth: str,
    docker_credentials: "DockerCredentials",
    tag: str = None,
) -> Dict[str, Any]:
    """
    Push an image to a registry.  If you wish to push an image on to a private
    registry, that image must already have a tag which references the registry.
    For example, `registry.example.com/myimage:latest`.  The push is cancelled
    if the HTTP connection is closed.

    Args:
        name:
            Name used in formatting the endpoint URL.
        x_registry_auth:
            A base64url-encoded auth configuration.  Refer to the [authentication
            section](
            section/Authentication) for details.
        docker_credentials:
            Credentials to use for authentication with Docker.
        tag:
            The tag to associate with the image on the registry.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}/push`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 404 | No such image. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/images/{name}/push"  # noqa
    responses = {
        200: "No error.",  # noqa
        404: "No such image.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
        "tag": tag,
        "x_registry_auth": x_registry_auth,
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
async def image_tag(
    name: str,
    docker_credentials: "DockerCredentials",
    repo: str = None,
    tag: str = None,
) -> Dict[str, Any]:
    """
    Tag an image so that it becomes part of a repository.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        repo:
            The repository to tag in. For example, `someuser/someimage`.
        tag:
            The name of the new tag.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}/tag`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 201 | No error. |
    | 400 | Bad parameter. |
    | 404 | No such image. |
    | 409 | Conflict. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/images/{name}/tag"  # noqa
    responses = {
        201: "No error.",  # noqa
        400: "Bad parameter.",  # noqa
        404: "No such image.",  # noqa
        409: "Conflict.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
        "repo": repo,
        "tag": tag,
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
async def image_delete(
    name: str,
    docker_credentials: "DockerCredentials",
    force: bool = False,
    noprune: bool = False,
) -> Dict[str, Any]:
    """
    Remove an image, along with any untagged parent images that were referenced by
    that image.  Images can't be removed if they have descendant images, are
    being used by a running container or are being used by a build.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.
        force:
            Remove the image even if it is being used by stopped containers or has
            other tags.
        noprune:
            Do not delete untagged parent images.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | The image was deleted successfully. |
    | 404 | No such image. |
    | 409 | Conflict. |
    | 500 | Server error. |
    """  # noqa
    endpoint = f"/images/{name}"  # noqa
    responses = {
        200: "The image was deleted successfully.",  # noqa
        404: "No such image.",  # noqa
        409: "Conflict.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "name": name,
        "force": force,
        "noprune": noprune,
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
async def image_search(
    term: str,
    docker_credentials: "DockerCredentials",
    limit: int = None,
    filters: str = None,
) -> Dict[str, Any]:
    """
    Search for an image on Docker Hub.

    Args:
        term:
            Term to search.
        docker_credentials:
            Credentials to use for authentication with Docker.
        limit:
            Maximum number of results to return.
        filters:
            A JSON encoded value of the filters (a `map[string][]string`) to process
            on the images list. Available filters:  - `is-
            automated=(true|false)` - `is-official=(true|false)` -
            `stars=<number>` Matches images that has at least 'number'
            stars.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/search`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/images/search"  # noqa

    responses = {
        200: "No error.",  # noqa
        500: "Server error.",  # noqa
    }

    params = {
        "term": term,
        "limit": limit,
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
async def image_prune(
    docker_credentials: "DockerCredentials",
    filters: str = None,
) -> Dict[str, Any]:
    """
    Delete unused images.

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        filters:
            Filters to process on the prune list, encoded as JSON (a
            `map[string][]string`). Available filters:  -
            `dangling=<boolean>` When set to `true` (or `1`), prune only
            unused *and* untagged images. When set to `false`    (or
            `0`), all unused images are pruned. - `until=<string>` Prune
            images created before this timestamp. The `<timestamp>` can
            be Unix timestamps, date formatted timestamps, or Go
            duration strings (e.g. `10m`, `1h30m`) computed relative to
            the daemon machine’s time. - `label` (`label=<key>`,
            `label=<key>=<value>`, `label!=<key>`, or
            `label!=<key>=<value>`) Prune images with (or without, in
            case `label!=...` is used) the specified labels.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/prune`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | No error. |
    | 500 | Server error. |
    """  # noqa
    endpoint = "/images/prune"  # noqa

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
async def image_get(
    name: str,
    docker_credentials: "DockerCredentials",
) -> Dict[str, Any]:
    """
    Get a tarball containing all images and metadata for a repository.  If `name` is
    a specific name and tag (e.g. `ubuntu:latest`), then only that image (and
    its parents) are returned. If `name` is an image ID, similarly only that
    image (and its parents) are returned, but with the exclusion of the
    `repositories` file in the tarball, as there were no image names referenced.
    Image tarball format  An image tarball contains one directory per image
    layer (named using its long ID), each containing these files:  - `VERSION`:
    currently `1.0` - the file format version - `json`: detailed layer
    information, similar to `docker inspect layer_id` - `layer.tar`: A tarfile
    containing the filesystem changes in this layer  The `layer.tar` file
    contains `aufs` style `.wh..wh.aufs` files and directories for storing
    attribute changes and deletions.  If the tarball defines a repository, the
    tarball should also include a `repositories` file at the root that contains
    a list of repository and tag names mapped to layer IDs.  ```json {   'hello-
    world': {     'latest':
    '565a9d68a73f6706862bfe8409a7f659776d4d60a8d096eb4a3cbce6999cc2a1'   } } ```.

    Args:
        name:
            Name used in formatting the endpoint URL.
        docker_credentials:
            Credentials to use for authentication with Docker.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/{name}/get`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = f"/images/{name}/get"  # noqa
    responses = {
        200: "no error.",  # noqa
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
async def image_get_all(
    docker_credentials: "DockerCredentials",
    names: List = None,
) -> Dict[str, Any]:
    """
    Get a tarball containing all images and metadata for several image repositories.
    For each value of the `names` parameter: if it is a specific name and tag
    (e.g. `ubuntu:latest`), then only that image (and its parents) are returned;
    if it is an image ID, similarly only that image (and its parents) are
    returned and there would be no names referenced in the 'repositories' file
    for this image ID.  For details on the format, see the [export image
    endpoint](
    operation/ImageGet).

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        names:
            Image names to filter by.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/get`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/images/get"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "names": names,
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
async def image_load(
    docker_credentials: "DockerCredentials",
    images_tarball: str = None,
    quiet: bool = False,
) -> Dict[str, Any]:
    """
    Load a set of images and tags into a repository.  For details on the format, see
    the [export image endpoint](
    operation/ImageGet).

    Args:
        docker_credentials:
            Credentials to use for authentication with Docker.
        images_tarball:
            Tar archive containing images.
        quiet:
            Suppress progress details during load.

    Returns:
        A dict of the response.

    <h4>API Endpoint:</h4>
    `/images/load`

    <h4>API Responses:</h4>
    | Response | Description |
    | --- | --- |
    | 200 | no error. |
    | 500 | server error. |
    """  # noqa
    endpoint = "/images/load"  # noqa

    responses = {
        200: "no error.",  # noqa
        500: "server error.",  # noqa
    }

    params = {
        "images_tarball": images_tarball,
        "quiet": quiet,
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
