"""
Sphinx HTML Multiple Versions.

Loads the list of versions into the configuration file.
"""

import os

# Get the list of all versions for which a documentation is available
html_context = {"versions": []}
versions_path = os.path.dirname(__file__) + "\\"
# print("========= versions_path: ", versions_path)
for file in os.listdir(versions_path):
    if os.path.isdir(versions_path + file) and file[0] != "_":
        html_context["versions"].append(os.path.basename(file))
