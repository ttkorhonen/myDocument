# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'EPICS pvAccess and Channel Access Documentation'
copyright = '2019, Timo Korhonen'
author = 'Timo Korhonen'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "hoverxref.extension",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.graphviz",
    "sphinx_copybutton",
    "sphinx.ext.intersphinx",
]
intersphinx_mapping = {
    'how-tos': ('https://docs.epics-controls.org/projects/how-tos/en/latest', None),
    'epics': ('https://docs.epics-controls.org/en/latest/', None),
    'mydocs' : ('https://ca-security-spec.readthedocs.io/en/latest/',None),
}
hoverxref_role_types = {
    'hoverxref': 'tooltip',
    'ref': 'modal',
    'confval': 'tooltip',
    'mod': 'modal',
    'class': 'modal',
    'obj': 'tooltip',
}

hoverxref_intersphinx_types = {
    'readthedocs': 'modal',
    'sphinx': 'tooltip',
}

hoverxref_domains = [
    'std',
    'py',
]
hoverxref_intersphinx = [
    'how-tos',
    'epics',
    'mydocs',
]
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'friendly'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

master_doc = 'index'

html_theme_options = {
    'logo_only': False,
    'body_max_width': '90%',
}
html_logo = "EPICS_logo_svg.svg"
html_css_files = [
    'custom.css',
]
#def setup(app):
#   app.add_stylesheet('mycustom.css')

