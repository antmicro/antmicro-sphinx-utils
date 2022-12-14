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

# Add any Sphinx extension module names here, as strings.
# They can be extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.

from pathlib import Path
from os import environ
from inspect import stack

from antmicro_sphinx_utils import assets

extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinxcontrib.internal',
    'myst_parser',
    'sphinx_immaterial',
]

myst_enable_extensions = [
    'substitution'
]

def relative_to_git(loc: Path = None) -> Path:
    for item in loc.parents:
        if (item / '.git').is_dir():
            return loc.relative_to(item)
    return loc.name

def default_antmicro_html_theme_options(
    gh_slug = None, # Provide for repos also on GitHub
    pdf_url = None,
):
    conf_py_path = relative_to_git(Path(stack()[1].filename).parent)

    options = {
        "social": [
            {
                "icon": "fontawesome/brands/github",
                "link": "https://github.com/antmicro",
            },
            {
                "icon": "fontawesome/brands/twitter",
                "link": "https://twitter.com/antmicro",
            },
        ],
        "palette": [
            {
                "media": "(prefers-color-scheme: light)",
                "scheme": "default",
                "primary": "teal",
                "accent": "deep-orange",
                "toggle": {
                    "icon": "material/weather-night",
                    "name": "Switch to dark mode",
                },
            },
            {
                "media": "(prefers-color-scheme: dark)",
                "scheme": "slate",
                "primary": "teal",
                "accent": "deep-orange",
                "toggle": {
                    "icon": "material/weather-sunny",
                    "name": "Switch to light mode",
                },
            },
        ],
        "features": [
            "toc.integrate",
        ],
    }

    project_url = environ.get('CI_FULL_PROJECT_URL')

    if project_url is not None:
        options.update({
            "edit_uri": f"blob/{environ.get('CI_BUILD_REF_NAME', 'main')}/{conf_py_path}",
            "repo_url": project_url,
            "repo_name": project_url.split('/')[-1],
            "repo_type": "gitlab",
            "icon": {
                "repo": "fontawesome/brands/git-alt",
            }
        })
        if pdf_url is not None:
            options.update({
                "pdf_url": pdf_url,
            })
    elif gh_slug is not None:
        options.update({
            "repo_url": f"https://github.com/{gh_slug}",
            "repo_name": gh_slug,
            "edit_uri": f"blob/{environ.get('GITHUB_REF_NAME', 'main')}/{conf_py_path}",
            "repo_type": "github",
            "icon": {
                "repo": "fontawesome/brands/github",
            }
        })

    return options

def default_antmicro_latex_elements(basic_filename, project, authors, latex_logo=None):
    if latex_logo is None:
        latex_logo = str(assets.logo('latex'))

    # Grouping the document tree into LaTeX files. List of tuples
    # (source start file, target name, title, author, documentclass [howto/manual]).
    latex_documents = [
        ('index', basic_filename+'.tex', project,
        authors, 'manual'),
    ]

    latex_additional_files = [str(assets.latex_sty()),latex_logo]

    return ({
        'papersize': 'a4paper',
        'pointsize': '11pt',
        'fontpkg': r'''
            \usepackage{charter}
            \usepackage[defaultsans]{lato}
            \usepackage{inconsolata}
            \usepackage{lscape}
        ''',
        'preamble': r'''
              \usepackage{sphinx_antmicro}
              \usepackage{multicol}
        ''',
        'maketitle': f'''
            \\renewcommand{{\\releasename}}{{}}
            \\renewcommand{{\sphinxlogo}}{{\includegraphics[height=75pt]{{{latex_logo}}}\par}}
            \sphinxmaketitle
        ''',
        'classoptions':',openany,oneside',
        'babel': r'''
              \usepackage[english]{babel}
              \makeatletter
              \@namedef{ver@color.sty}{}
              \makeatother
              \usepackage{silence}
              \WarningFilter{Fancyhdr}{\fancyfoot's `E' option without twoside}
        '''
    }, latex_documents, latex_logo, latex_additional_files)
