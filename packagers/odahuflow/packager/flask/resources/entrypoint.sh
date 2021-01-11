#!/usr/bin/env bash

# Starting of Gunicorn server with Odahu's HTTP handler

MODEL_LOCATION={{ model_location }} \
    gunicorn \
    --pythonpath /app/ \
    --timeout {{ timeout }} \
    -b {{ host }}:{{ port }} \
    -w {{ workers }} \
    --threads {{ threads }} \
    {{ wsgi_handler }}
