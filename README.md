# prefect-docker

<a href="https://pypi.python.org/pypi/prefect-docker/" alt="PyPI Version">
    <img src="https://badge.fury.io/py/prefect-docker.svg" /></a>
<a href="https://github.com/PrefectHQ/prefect-docker/" alt="Stars">
    <img src="https://img.shields.io/github/stars/PrefectHQ/prefect-docker" /></a>
<a href="https://pepy.tech/badge/prefect-docker/" alt="Downloads">
    <img src="https://pepy.tech/badge/prefect-docker" /></a>
<a href="https://github.com/PrefectHQ/prefect-docker/pulse" alt="Activity">
    <img src="https://img.shields.io/github/commit-activity/m/PrefectHQ/prefect-docker" /></a>
<a href="https://github.com/PrefectHQ/prefect-docker/graphs/contributors" alt="Contributors">
    <img src="https://img.shields.io/github/contributors/PrefectHQ/prefect-docker" /></a>
<br>
<a href="https://prefect-community.slack.com" alt="Slack">
    <img src="https://img.shields.io/badge/slack-join_community-red.svg?logo=slack" /></a>
<a href="https://discourse.prefect.io/" alt="Discourse">
    <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?logo=discourse" /></a>

## Welcome!

Prefect integrations for interacting with Docker.

The tasks within this collection were created by a code generator using the service's OpenAPI spec.

The service's REST API documentation can be found [here](https://docs.docker.com/engine/api/v1.41/).

## Getting Started

### Python setup

Requires an installation of Python 3.7+.

We recommend using a Python virtual environment manager such as pipenv, conda or virtualenv.

These tasks are designed to work with Prefect 2.0. For more information about how to use Prefect, please refer to the [Prefect documentation](https://orion-docs.prefect.io/).

### Installation

Install `prefect-docker` with `pip`:

```bash
pip install prefect-docker
```

### List containers

```python
from prefect import flow
from prefect_docker import DockerCredentials
from prefect_docker.containers import container_list

@flow
def list_containers_flow():
    credentials = DockerCredentials()
    return container_list(credentials)

list_containers_flow()
```

## Resources

If you encounter any bugs while using `prefect-docker`, feel free to open an issue in the [prefect-docker](https://github.com/PrefectHQ/prefect-docker) repository.

If you have any questions or issues while using `prefect-docker`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

## Development

If you'd like to install a version of `prefect-docker` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-docker.git

cd prefect-docker/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
