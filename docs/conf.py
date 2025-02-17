# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime as dt
import sys
from pathlib import Path

import data_morph

sys.path.insert(0, str(Path().absolute()))
from post_build import determine_versions

project = 'Data Morph'
current_year = dt.date.today().year
copyright = f'2023{f"-{current_year}" if current_year != 2023 else ""}, Stefanie Molin'
author = 'Stefanie Molin'
release = data_morph.__version__
version_match, _ = determine_versions()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# nitpicky = True
nitpick_ignore_regex = [('py:class', r'(optional|default.*)')]

# default language for code-highlighting (requires specific declarations to highlight)
highlight_language = 'output'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
    'sphinx_argparse_cli',
    'matplotlib.sphinxext.plot_directive',
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_show_sourcelink = False

# -- autosectionlabel ---------------------------------------------------------

# Make sure the target is unique
autosectionlabel_prefix_document = True


# -- intersphinx -------------------------------------------------------------

intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable', None),
    'Pillow': ('https://pillow.readthedocs.io/en/stable', None),
    'pytest': ('https://pytest.org/en/stable', None),
    'python': ('https://docs.python.org/3', None),
    'rich': ('https://rich.readthedocs.io/en/stable', None),
}


# -- autosummary -------------------------------------------------------------

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'special-members': False,
    'show-inheritance': True,
    'inherited-members': True,
}


# -- Internationalization ----------------------------------------------------

# specifying the natural language populates some key tags
language = 'en'


# -- copybutton config -------------------------------------------------------
copybutton_prompt_text = r'>>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: |>'
copybutton_prompt_is_regexp = True


# -- matplotlib plot directive config ----------------------------------------
plot_html_show_source_link = False
plot_html_show_formats = False


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = f'https://stefaniemolin.com/data-morph/{version_match}/'
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['tutorials/style.css']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

html_theme_options = {
    'github_url': 'https://github.com/stefmolin/data-morph',
    'twitter_url': 'https://twitter.com/StefanieMolin',
    'show_toc_level': 1,
    'navbar_align': 'left',
    'navbar_end': ['version-switcher', 'theme-switcher', 'navbar-icon-links'],
    'switcher': {
        'json_url': 'https://raw.githubusercontent.com/stefmolin/data-morph/main/docs/_static/switcher.json',
        'version_match': version_match,
    },
    'external_links': [
        {
            'name': 'Article about Data Morph',
            'url': 'https://stefaniemolin.com/articles/data-science/introducing-data-morph/',
        },
        {
            'name': 'Conference Talk Slides on Data Morph',
            'url': 'https://stefaniemolin.com/data-morph-talk/#/',
        },
        {
            'name': "Stefanie Molin's Website",
            'url': 'https://stefaniemolin.com',
        },
    ],
    'analytics': {
        'google_analytics_id': 'G-FMNM78QSKK',
    },
    'show_prev_next': False,
}

html_context = {
    'github_user': 'stefmolin',
    'github_repo': 'data-morph',
    'github_version': 'main',
    'doc_path': 'docs',
}

# Workaround for removing the left sidebar on pages without TOC
# A better solution would be to follow the merge of:
# https://github.com/pydata/pydata-sphinx-theme/pull/1682
html_sidebars = {
    'cli': [],
    'quickstart': [],
    'release-notes': [],
    'tutorials/*': [],
}


# -- sphinx adjustments --------------------------------------------------
def skip(app, what, name, obj, would_skip, options):
    if name.startswith('_'):
        return True
    return would_skip


def docstring_strip(app, what, name, obj, options, lines):
    if what == 'module' and name == 'data_morph' and lines[0] == 'Data Morph.':
        # Tweak the package docstring for the docs
        _ = lines.pop(0)
        _ = lines.pop(0)
        extended_summary = lines[0].split()
        extended_summary[0] = 'Data Morph allows you to morph'
        lines[0] = ' '.join(extended_summary)


def setup(app):
    app.connect('autodoc-skip-member', skip)
    app.connect('autodoc-process-docstring', docstring_strip)
