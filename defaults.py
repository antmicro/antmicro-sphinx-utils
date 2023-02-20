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


ROOT = Path(__file__).resolve().parent

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


def antmicro_html(
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
                "scheme": "slate",
                "primary": "teal",
                "accent": "deep-orange",
                "toggle": {
                    "icon": "material/weather-sunny",
                    "name": "Switch to light mode",
                },
            },
            {
                "scheme": "default",
                "primary": "teal",
                "accent": "deep-orange",
                "toggle": {
                    "icon": "material/weather-night",
                    "name": "Switch to dark mode",
                },
            },
        ],
        "features": [
            "toc.integrate",
        ],
    }

    project_url = environ.get('CI_FULL_PROJECT_URL')
    html_context = {}

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
        html_context.update({
            'commit': environ.get('CI_BUILD_REF'),
            'build_id': environ.get('CI_BUILD_REF_NAME'),
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

        if environ.get('READTHEDOCS') == 'True':
            build_id = environ.get('READTHEDOCS_VERSION_NAME')
            isExternal = environ.get('READTHEDOCS_VERSION_TYPE') == 'external'
            html_context.update({
                'build_id': f"#{build_id}" if isExternal else build_id,
                'build_url': (
                    options['repo_url'] if build_id == 'latest' else
                    f"{options['repo_url']}/{'pull' if isExternal else 'tree'}/{build_id}"
                )
            })
        else:
            html_context.update({
                'commit': environ.get('GITHUB_SHA'),
                'build_id': environ.get('GITHUB_REF_NAME'),
            })

    if 'commit' in html_context:
        if 'commit_url' not in html_context:
            html_context['commit_url'] = f"{options['repo_url']}/tree/{html_context['commit']}"
        html_context['commit'] = html_context['commit'][0:8]

    if ('build_id' in html_context) and ('build_url' not in html_context):
        html_context['build_url'] = f"{options['repo_url']}/tree/{html_context['build_id']}"

    if pdf_url is not None:
        options.update({
            "pdf_url": pdf_url,
        })

    return (str(ROOT / 'logo/white.svg'), options, html_context)


def antmicro_latex(basic_filename, project, authors, latex_logo=None):
    if latex_logo is None:
        latex_logo = str(ROOT / 'logo/latex.png')

    return (
        # latex_elements
        {
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
        },
        # latex_documents
        [
            ('index', basic_filename+'.tex', project,
            authors, 'manual'),
        ],
        # latex_logo
        latex_logo,
        # latex_additional_files
        [str(ROOT / 'sphinx_antmicro.sty'), latex_logo]
    )
