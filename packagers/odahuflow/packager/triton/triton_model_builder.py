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

from os import PathLike

import logging
import os
import shutil
from typing import Optional, Iterable

log = logging.getLogger(__name__)


def build_triton_model(model_file_paths: Iterable[PathLike], model_config_path: Optional[PathLike],
                       output_dir: PathLike):
    """
    Collects provided files into file structure expected by Triton server
    :raises OSError: if failed to create needed directories
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError:
        log.error(f'Failed to create a directory for triton model: {output_dir}')
        raise

    model_v1_path = os.path.join(output_dir, '1')
    os.mkdir(model_v1_path)

    if model_config_path is not None:
        shutil.copy(model_config_path, output_dir)

    for path in model_file_paths:
        if os.path.isdir(path):
            dirname = os.path.basename(path)
            shutil.copytree(path, os.path.join(model_v1_path, dirname))
        else:
            shutil.copy(path, output_dir)
