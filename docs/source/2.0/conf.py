# ../conf.py
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from conf_common import *

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The full version path, including alpha/beta/rc tags.
release = os.path.basename(os.path.dirname(__file__))
# The short X.Y version.
version = release
