# Base image name
ARG base_image=python:3.6
FROM ${base_image}

# TODO: insert command to add and install a model

WORKDIR /app
COPY ./ /app/
RUN pip install -e .

