# Base image name
FROM {{ base_image }}

# Copy model GPPI
COPY {{ gppi_location }} /app/{{ gppi_location }}

# Creation of conda's envinroment named model
RUN conda env update --name=${ODAHU_CONDA_ENV_NAME} --file={{ gppi_location }}/{{ conda_file_name }}

# Copy model GPPI
COPY {{ gppi_location }} /app/{{ gppi_location }}

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
