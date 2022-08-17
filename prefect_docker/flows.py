"""This is an example flows module"""
from prefect import flow

from prefect_docker.tasks import goodbye_prefect_docker, hello_prefect_docker


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    print(hello_prefect_docker)
    print(goodbye_prefect_docker)
    return "Done"
