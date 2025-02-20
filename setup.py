#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 Antmicro.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup as setuptools_setup


setuptools_setup(
    name='antmicro_sphinx_utils',
    version="0.0.0",
    license="Apache-2.0",
    author="Antmicro",
    description="Antmicro Sphinx Utils.",
    url="https://github.com/antmicro/antmicro-sphinx-utils",
    packages=["antmicro_sphinx_utils"],
    package_dir={"antmicro_sphinx_utils": "."},
    package_data={
        "antmicro_sphinx_utils": [
            "*.sty",
            "logo/*.png",
            "logo/*.svg",
        ],
    },
    install_requires=[
        'myst-parser',
        'sphinx',
        'sphinxcontrib-mermaid',
        'sphinx-immaterial @ https://github.com/antmicro/sphinx-immaterial/releases/download/tip/sphinx_immaterial-0.0.post1-py3-none-any.whl',  # noqa: E501
        'sphinx_tabs',
    ],
    classifiers=[],
    python_requires=">=3.6",
)
