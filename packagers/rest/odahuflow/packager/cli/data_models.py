import pydantic

DEFAULT_IMAGE_NAME_TEMPLATE = "{{ Name }}-{{ Version }}:{{ RandomUUID }}"


class PackagingResourceArguments(pydantic.BaseModel):
    """
    Legion Packaging Resource Arguments
    """

    dockerfilePush: bool = True
    dockerfileAddCondaInstallation: bool = True
    dockerfileBaseImage: str = 'nexus.ailifecycle.org:443/odahu/odahu-flow-cli:1.0.0-dev1575045866018'
    dockerfileCondaEnvsLocation: str = '/opt/conda/envs/'
    # Full name or Jinja template
    imageName: str = DEFAULT_IMAGE_NAME_TEMPLATE


class DockerTemplateContext(pydantic.BaseModel):
    """
    Main Docker template context
    """

    base_image: str
    conda_file_name: str
    conda_env_name: str
    model_name: str
    model_version: str
    model_location: str