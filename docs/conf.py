# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime as dt

import data_morph

project = 'Data Morph'
current_year = dt.date.today().year
copyright = (
    f'2023{f"-{current_year}" if current_year != 2023 else ""}, ' 'Stefanie Molin'
)
author = 'Stefanie Molin'
release = data_morph.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_copybutton',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- intersphinx -------------------------------------------------------------

intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'pytest': ('https://pytest.org/en/stable/', None),
    'python': ('https://docs.python.org/3/', None),
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
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_theme_options = {
    "github_url": "https://github.com/stefmolin/data-morph",
    "twitter_url": "https://twitter.com/StefanieMolin",
    # "header_links_before_dropdown": 4,
    # "use_edit_page_button": True,
    "show_toc_level": 1,
    "navbar_align": "left",  # [left, content, right] For testing that the navbar items align properly
    # "navbar_center": ["version-switcher", "navbar-nav"],
    # "announcement": "https://raw.githubusercontent.com/pydata/pydata-sphinx-theme/main/docs/_templates/custom-template.html",
    # "show_nav_level": 2,
    # "navbar_start": ["navbar-logo"],
    # "navbar_end": ["theme-switcher", "navbar-icon-links"],
    # "navbar_persistent": ["search-button"],
    # "primary_sidebar_end": ["custom-template.html", "sidebar-ethical-ads.html"],
    # "footer_start": ["test.html", "test.html"],
    # "secondary_sidebar_items": ["page-toc.html"],  # Remove the source buttons
    # "switcher": {
    #     "json_url": json_url,
    #     "version_match": version_match,
    # },
    # "search_bar_position": "navbar",  # TODO: Deprecated - remove in future version
}

# html_sidebars = {
#     "community/index": [
#         "sidebar-nav-bs",
#         "custom-template",
#     ],  # This ensures we test for custom sidebars
#     "examples/no-sidebar": [],  # Test what page looks like with no sidebar items
#     "examples/persistent-search-field": ["search-field"],
#     # Blog sidebars
#     # ref: https://ablog.readthedocs.io/manual/ablog-configuration-options/#blog-sidebars
#     "examples/blog/*": [
#         "ablog/postcard.html",
#         "ablog/recentposts.html",
#         "ablog/tagcloud.html",
#         "ablog/categories.html",
#         "ablog/authors.html",
#         "ablog/languages.html",
#         "ablog/locations.html",
#         "ablog/archives.html",
#     ],
# }

html_context = {
    "github_user": "stefmolin",
    "github_repo": "data-morph",
    "github_version": "main",
    "doc_path": "docs",
}
