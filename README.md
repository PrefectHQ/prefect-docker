# prefect-docker

<p align="center">
    <a href="https://pypi.python.org/pypi/prefect-docker/" alt="PyPI version">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/prefect-docker?color=0052FF&labelColor=090422"></a>
    <a href="https://github.com/PrefectHQ/prefect-docker/" alt="Stars">
        <img src="https://img.shields.io/github/stars/PrefectHQ/prefect-docker?color=0052FF&labelColor=090422" /></a>
    <a href="https://pepy.tech/badge/prefect-docker/" alt="Downloads">
        <img src="https://img.shields.io/pypi/dm/prefect-docker?color=0052FF&labelColor=090422" /></a>
    <a href="https://github.com/PrefectHQ/prefect-docker/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/PrefectHQ/prefect-docker?color=0052FF&labelColor=090422" /></a>
    <br>
    <a href="https://prefect-community.slack.com" alt="Slack">
        <img src="https://img.shields.io/badge/slack-join_community-red.svg?color=0052FF&labelColor=090422&logo=slack" /></a>
    <a href="https://discourse.prefect.io/" alt="Discourse">
        <img src="https://img.shields.io/badge/discourse-browse_forum-red.svg?color=0052FF&labelColor=090422&logo=discourse" /></a>
</p>

## Welcome!

Prefect integrations for working with Docker.

Note! The `DockerRegistryCredentials` in `prefect-docker` is a unique block, separate from the `DockerRegistry` in `prefect` core. While `DockerRegistry` implements a few functionality from both `DockerHost` and `DockerRegistryCredentials` for convenience, it does not allow much configuration to interact with a Docker host.

Do not use `DockerRegistry` with this collection. Instead, use `DockerHost` and `DockerRegistryCredentials`.

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

Then, register to [view the block](https://orion-docs.prefect.io/ui/blocks/) on Prefect Cloud:

```bash
prefect block register -m prefect_docker
```

Note, to use the `load` method on Blocks, you must already have a block document [saved through code](https://orion-docs.prefect.io/concepts/blocks/#saving-blocks) or [saved through the UI](https://orion-docs.prefect.io/ui/blocks/).

### Write and run a flow

```python
from prefect import flow
from prefect_docker.tasks import (
    goodbye_prefect_docker,
    hello_prefect_docker,
)


@flow
def example_flow():
    hello_prefect_docker
    goodbye_prefect_docker

example_flow()
```

## Resources

If you encounter any bugs while using `prefect-docker`, feel free to open an issue in the [prefect-docker](https://github.com/PrefectHQ/prefect-docker) repository.

If you have any questions or issues while using `prefect-docker`, you can find help in either the [Prefect Discourse forum](https://discourse.prefect.io/) or the [Prefect Slack community](https://prefect.io/slack).

Feel free to ⭐️ or watch [`prefect-docker`](https://github.com/PrefectHQ/prefect-docker) for updates too!

## Development

If you'd like to install a version of `prefect-docker` for development, clone the repository and perform an editable install with `pip`:

```bash
git clone https://github.com/PrefectHQ/prefect-docker.git

cd prefect-docker/

pip install -e ".[dev]"

# Install linting pre-commit hooks
pre-commit install
```
