# Base image name
FROM {{ base_image }}

# Copying of dependencies
COPY {{ conda_file_name }} .

# Creation of conda's envinroment named model
RUN conda env update --name=${ODAHU_CONDA_ENV_NAME} --file={{ conda_file_name }}

# Installing of additional packages inside specified env
COPY {{ conda_server_file_name }} .
RUN conda env update --name=${ODAHU_CONDA_ENV_NAME} --file={{ conda_server_file_name }}

ENV ODAHU_MODEL_NAME {{ model_name }}
ENV ODAHU_MODEL_VERSION {{ model_version }}

# Copy wrappers
COPY {{ entrypoint_target }} \
     {{ entrypoint_docker }} \
     {{ handler_file }} \
     ./

# Copy model only
COPY {{ model_location }} /app/{{ model_location }}

# Exposing HTTP port
EXPOSE {{ port }}

# Change permissions to cmd
RUN chmod +x {{ entrypoint_docker }}

# Setting cmd
ENTRYPOINT ["bash", "-c"]
CMD ["/app/{{ entrypoint_docker }}"]
