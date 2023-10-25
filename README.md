# Sphinx HTML Multiple Versions

This is a simple Python module and layout template for Sphinx to enable multiple versions
browsing of a documentation tree.

## Folder structure

Assuming the following folder structure (see the `example/src/` directory for a real example):

```
.
├── 1.0
│   ├── conf.py -> ../conf.py
│   ├── index.rst
│   ├── _static -> ../_static
│   └── _templates -> ../_templates
├── 2.0
│   ├── conf.py -> ../conf.py
│   ├── index.rst
│   ├── _static -> ../_static
│   └── _templates -> ../_templates
├── conf.py
├── sphinx_html_multi_versions.py
├── _static
└── _templates
    └── layout.html
```

In the above, `1.0/conf.py` is a symlink to `conf.py`, `1.0/_templates/` is a symlink to `_templates/`, and
`1.0/_static/` is a symlink to `_static/`.

Your configuration file remains `conf.py` in the root of the project. Make sure you add the
`sphinx_html_multi_versions.py` and `_templates/layout.html` files to your project.

## Configuration

Add the following at the end of your `conf.py` file:

```python
import os, sys
sys.path.append(os.path.dirname(__file__) + "/..")
import sphinx_html_multi_versions
html_context = sphinx_html_multi_versions.html_context
```

## Building

Each version is built separately, and should be outputted to its own directory matching the tree
structure of the source files.

Per example:

```
sphinx-build -b html example/src/2.0 example/dist/2.0
sphinx-build -b html example/src/1.0 example/dist/1.0
```

A drop-down menu will be available in each build to switch between versions.

## Example

You can find a working example in `example/src/` and its generated output in `example/dist/`.

Happy versioning!

