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

from setup import extract_version
from setuptools import find_namespace_packages, setup


setup(
    name='odahu-flow-model-cli',
    version=extract_version(),
    description='Odahu model CLI',
    packages=find_namespace_packages(),
    author='Vlad Tokarev, Vitalik Solodilov',
    author_email='vlad.tokarev.94@gmail.com, mcdkr@yandex.ru',
    license='Apache v2',
    entry_points={
        'console_scripts': ['odahuflowctl=odahuflow.modelcli.main:main'],
    },
)
