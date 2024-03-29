#
#    Copyright 2019 EPAM Systems
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import json
import os
from typing import List, Dict, Union, Any

from flask import Flask, jsonify, Response, request
import orjson
import numpy as np

import odahuflow_model.entrypoint

MODEL_NAME = 'Model-Name'
MODEL_VERSION = 'Model-Version'

app = Flask(__name__)
SUPPORTED_PREDICTION_MODE = odahuflow_model.entrypoint.init()

ODAHU_MODEL_NAME = "ODAHU_MODEL_NAME"
ODAHU_MODEL_VERSION = "ODAHU_MODEL_VERSION"

model_name = os.getenv(ODAHU_MODEL_NAME)
model_version = os.getenv(ODAHU_MODEL_VERSION)


def build_error_response(message):
    return Response(response=json.dumps({'message': message}), status=500, mimetype='application/json')


@app.route('/api/model/info', methods=['GET'])
def info():
    # Consider, if model does not provide info endpoint
    # TODO: Refactor this
    input_schema, output_schema = odahuflow_model.entrypoint.info()

    input_properties = generate_input_props(input_schema)
    output_properties = generate_output_props(output_schema)
    return jsonify({
        "swagger": "2.0",
        "info": {
            "description": "This is a EDI server.",
            "title": model_name,
            "version": model_version,
            "termsOfService": "http://swagger.io/terms/",
            "contact": {},
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            }
        },
        "schemes": [
            "https"
        ],
        "host": "",
        "basePath": "",
        "paths": {
            "/api/model/info": {
                "get": {
                    "description": "Return a swagger info about model",
                    "consumes": [],
                    "produces": [
                        "application/json"
                    ],
                    "summary": "Info",
                    "responses": {
                        "200": {
                            "description": "Info",
                            "type": "object"
                        }
                    }
                }
            },
            "/api/model/invoke": {
                "post": {
                    "description": "Execute prediction",
                    "consumes": [
                        "application/json"
                    ],
                    "produces": [
                        "application/json"
                    ],
                    "summary": "Prediction",
                    "parameters": [
                        {
                            "in": "body",
                            "name": "PredictionParameters",
                            "required": True,
                            "schema": {
                                "properties": input_properties,
                                "type": "object"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Results of prediction",
                            "name": "PredictionResponse",
                            "properties": output_properties
                        },
                        "type": "object"
                    }
                }
            }
        }
    })



def generate_input_props(input_schema: List[Dict[str, Union[Union[str, None, bool], Any]]]) -> Dict[str, Any]:
    """
    Generate input model properties in OpenAPI format
    :param input_schema: Input schema
    :return:
    """
    examples: List[Any] = []
    columns: List[str] = []
    for prop in input_schema:
        columns.append(prop['name'])
        examples.append(prop['example'])

    return {
        "columns": {
            "example": columns,
            "items": {
                "type": "string"
            },
            "type": "array"
        },
        "data": {
            "items": {
                "items": {
                    "type": "number"
                },
                "type": "array"
            },
            "type": "array",
            "example": [examples],
        }
    }


def generate_output_props(output_schema: List[Dict[str, Union[Union[str, None, bool], Any]]]) -> Dict[str, Any]:
    """
    Generate input model properties in OpenAPI format
    :param output_schema:
    :return:
    """
    examples: List[Any] = []
    columns: List[str] = []
    for prop in output_schema:
        columns.append(prop['name'])
        examples.append(prop['example'])

    return {
        "prediction": {
            "example": [examples],
            "items": {
                "type": "number"
            },
            "type": "array",
        },
        "columns": {
            "example": columns,
            "items": {
                "type": "string"
            },
            "type": "array"
        }
    }


@app.route('/healthcheck', methods=['GET'])
def ping():
    return jsonify({'status': True})


def handle_prediction_on_matrix(parsed_data: dict) -> bytes:
    matrix = parsed_data.get('data')
    columns = parsed_data.get('columns', None)

    if not matrix:
        return build_error_response('Matrix is not provided')

    try:
        prediction: Union[List, np.ndarray]
        columns: Tuple[str, ...]
        prediction, columns = odahuflow_model.entrypoint.predict_on_matrix(matrix, provided_columns_names=columns)
    except Exception as predict_exception:
        return build_error_response(f'Exception during prediction: {predict_exception}')

    response = {
        'prediction': prediction,
        'columns': columns
    }

    try:
        response_json = orjson.dumps(response, option=orjson.OPT_SERIALIZE_NUMPY)
    except TypeError as e:
        # Catches cases when NumPy array has unsupported dtypes
        if not isinstance(response['prediction'], np.ndarray):
            raise e

        response['prediction'] = response['prediction'].tolist()
        response_json = orjson.dumps(response)

    return response_json


def handle_prediction_on_objects(parsed_data):
    return build_error_response('Can not handle this types of requests')


@app.route('/api/model/invoke', methods=['POST'])
def predict():
    if not request.data:
        return build_error_response('Please provide data with this POST request')

    try:
        data = request.data.decode('utf-8')
    except UnicodeDecodeError as decode_error:
        return build_error_response(f'Can not decode POST data using utf-8 charset: {decode_error}')

    try:
        parsed_data = orjson.loads(data)
    except ValueError as value_error:
        return build_error_response(f'Can not parse input as JSON: {value_error}')

    if SUPPORTED_PREDICTION_MODE == 'matrix':
        response_json = handle_prediction_on_matrix(parsed_data)
    elif SUPPORTED_PREDICTION_MODE == 'objects':
        response_json = handle_prediction_on_objects(parsed_data)
    else:
        return build_error_response(f'Unknown model\'s return type: {SUPPORTED_PREDICTION_MODE}')

    # handle_prediction_on_matrix & handle_prediction_on_objects can return Response in case of exception
    if isinstance(response_json, Response):
        return response_json

    resp = Response(response=response_json, status=200, mimetype='application/json')

    resp.headers[MODEL_NAME] = os.getenv(ODAHU_MODEL_NAME)
    resp.headers[MODEL_VERSION] = os.getenv(ODAHU_MODEL_VERSION)

    return resp
