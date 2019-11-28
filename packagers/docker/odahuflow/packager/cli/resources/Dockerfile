# Base image name
FROM {{ base_image }}

{{ conda_installation_content }}

WORKDIR /app

# Copy model GPPI
COPY {{ gppi_location }} /app/{{ gppi_location }}

# Install deps from GPPI to specific conda env
RUN conda create -vv --name {{ conda_env_name }} --yes && \
    conda env update --name={{ conda_env_name }} --file={{ gppi_location }}/{{ conda_file_name }}

# Updating PATH for entrypoint
ENV PATH /opt/conda/envs/{{ conda_env_name }}/bin:$PATH

COPY {{ package_name }} /app/{{ package_name }}
COPY setup.py /app/
RUN pip install -e .

# Metadata
ENV ODAHU_MODEL_NAME {{ model_name }}
ENV ODAHU_MODEL_VERSION {{ model_version }}

# Gppi location
ENV MODEL_LOCATION /app/{{ gppi_location }}/{{ model_location }}
ENV MODEL_ENTRYPOINT {{ entrypoint }}

# Setting cmd
ENTRYPOINT ["{{ entrypoint_invoker_cli_name }}"]
