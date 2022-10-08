"""This is an example flows module"""
from prefect import flow

from prefect_docker.blocks import DockerBlock
from prefect_docker.tasks import goodbye_prefect_docker, hello_prefect_docker


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    DockerBlock.seed_value_for_example()
    block = DockerBlock.load("sample-block")

    print(hello_prefect_docker())
    print(f"The block's value: {block.value}")
    print(goodbye_prefect_docker())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
