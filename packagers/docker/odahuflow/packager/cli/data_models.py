import pydantic
from odahuflow.packager.helpers.constants import DEFAULT_IMAGE_NAME_TEMPLATE


class PackagingResourceArguments(pydantic.BaseModel):
    """
    Odahu Packaging Resource Arguments
    """

    dockerfilePush: bool = True
    dockerfileAddCondaInstallation: bool = True
    dockerfileBaseImage: str = 'odahu/odahu-flow-docker-packager-base:latest'
    dockerfileCondaEnvsLocation: str = '/opt/conda/envs/'
    # Full name or Jinja template
    imageName: str = DEFAULT_IMAGE_NAME_TEMPLATE


class DockerTemplateContext(pydantic.BaseModel):
    """
    Main Docker template context
    """

    base_image: str
    conda_file_name: str
    model_name: str
    model_version: str
    model_location: str
    gppi_location: str
    entrypoint_invoker_script: str  # script that invoke gppi entrypoint
    entrypoint_invoker_cli_name: str  # cli (refers to ::main():: of ::entrypoint_invoker_script::)
    entrypoint: str  # entrypoint that is described in GPPI manifest
    package_name: str  # package name that  will be packed to distro (setuptools)
    distro_name: str  # setuptools distributive name
