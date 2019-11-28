# Base image name
FROM {{ base_image }}

WORKDIR /app

# Copy model GPPI
COPY {{ model_location }} /app/{{ model_location }}

# Install deps from GPPI to specific conda env
RUN conda create -vv --name {{ conda_env_name }} --yes && \
    conda env update --name={{ conda_env_name }} --file={{ model_location }}/{{ conda_file_name }}

# Metadata
ENV LEGION_MODEL_NAME {{ model_name }}
ENV LEGION_MODEL_VERSION {{ model_version }}

# Gppi location
ENV ODAHUFLOW_GPPI_MODEL_PATH /app/{{ model_location }}
# Conda env that should be used for GPPI invoking
ENV ODAHUFLOW_CONDA {{ conda_env_name }}

# Setting cmd
CMD [ "/bin/bash" ]
