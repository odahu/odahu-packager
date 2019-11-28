import pydantic
from odahuflow.packager.helpers.constants import DEFAULT_IMAGE_NAME_TEMPLATE


class PackagingResourceArguments(pydantic.BaseModel):
    """
    Odahu Packaging Resource Arguments
    """

    dockerfilePush: bool = True
    dockerfileAddCondaInstallation: bool = True
    dockerfileBaseImage: str = 'python:3.6'
    dockerfileCondaEnvsLocation: str = '/opt/conda/envs/'
    host: str = '0.0.0.0'
    port: int = 5000
    timeout: int = 60
    workers: int = 1
    threads: int = 4
    # Full name or Jinja template
    imageName: str = DEFAULT_IMAGE_NAME_TEMPLATE


class DockerTemplateContext(pydantic.BaseModel):
    """
    Main Docker template context
    """

    model_name: str
    model_version: str
    odahuflow_version: str
    packager_version: str
    path: str
    path_docker: str
    conda_env_name: str
    gunicorn_bin: str
    gunicorn_bin_docker: str
    timeout: str
    host: str
    port: str
    workers: str
    threads: str
    pythonpath: str
    wsgi_handler: str
    model_location: str
    entrypoint_target: str
    handler_file: str
    base_image: str
    conda_installation_content: str
    conda_file_name: str
    entrypoint_docker: str
