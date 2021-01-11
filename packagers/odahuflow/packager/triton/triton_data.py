#  Copyright 2020 EPAM Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import enum


class TritonBackends(enum.Enum):
    """This enum contains all supported Triton Backends
    and their corresponding expected names of model file
    """
    Python = 'model.py'
    TensorRT = 'model.plan'
    TensorFlow_SavedModel = 'model.savedmodel'
    TensorFlow_GraphDef = 'model.graphdef'
    ONNX = 'model.onnx'
    TorchScript = 'model.pt'
    Caffe2 = 'model.netdef'


# Set of backends that don't require Triton config file
# https://docs.nvidia.com/deeplearning/triton-inference-server/master-user-guide/docs/model_configuration.html#generated-model-configuration
optional_config_backends = {TritonBackends.TensorRT, TritonBackends.TensorFlow_SavedModel, TritonBackends.ONNX}
