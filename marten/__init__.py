from __future__ import absolute_import

import os as _os
from .conf import parse_directory as _parse_directory

__version__ = '0.1.1'



# Attempt to auto-load a default configuration from files in <cwd>/.marten/ based on the MARTEN_ENV env variable
# MARTEN_ENV defaults to 'default'
config = None
_marten_dir = _os.path.join(_os.getcwd(), '.marten')

if _os.path.isdir(_marten_dir):
	config = _parse_directory(_marten_dir, _os.environ.get('MARTEN_ENV', 'default'))
