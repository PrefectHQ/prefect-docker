"""
Used for generating the repository from scratch.
"""
from pathlib import Path
from typing import Any, Dict

from prefect_collection_generator.rest import populate_collection_repo

THIS_DIRECTORY = Path(__file__).parent.absolute()
REPO_DIRECTORY = THIS_DIRECTORY.parent

# # USE THIS IF NEED TO REGENERATE FROM SCRATCH; IF NOT SKIP TO NEXT SECTION
# from cookiecutter.main import cookiecutter

# extra_context = {
#     "full_name":  "Prefect Technologies Inc.",  # e.g. "Prefect Technologies, Inc.",
#     "email": "help@prefect.io",  # e.g. "help@prefect.io",
#     "github_organization": "PrefectHQ",  # e.g. "PrefectHQ",
#     "collection_name": "prefect-docker",
#     "collection_short_description": "Prefect integrations for Docker",  # noqa
# }

# collection_template_url = "https://github.com/PrefectHQ/prefect-collection-template"
# cookiecutter(
#     collection_template_url,
#     no_input=True,
#     checkout="generated_rest",
#     extra_context=extra_context,
#     overwrite_if_exists=True
# )
# REPO_DIRECTORY = THIS_DIRECTORY / "prefect-docker"  # redirects repo_directory

# UPDATE THESE AS DESIRED
service_name = "Docker"
urls = ["https://docs.docker.com/engine/api/v1.41.yaml"]
routes = None
overwrite = True


def preprocess_fn(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess the schema so it adheres to datamodel_code_generator
    standards; if not, pydantic models will not be auto-generated.
    """
    return schema


populate_collection_repo(
    service_name,
    urls,
    routes=routes,
    overwrite=overwrite,
    preprocess_fn=preprocess_fn,
    repo_directory=REPO_DIRECTORY,
    base_url="http://docker",
    regenerate_module_files=False,
    regenerate_test_files=False,
)
