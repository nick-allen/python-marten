from __future__ import absolute_import

import os as _os

__version__ = '0.4.0'



# Attempt to auto-load a default configuration from files in <cwd>/.marten/ based on the MARTEN_ENV env variable
# MARTEN_ENV defaults to 'default'
config = None
_marten_dir = _os.path.join(_os.getcwd(), '.marten')
_os.environ.setdefault('MARTEN_ENV', 'default')

if _os.path.isdir(_marten_dir):
	from .configurations import parse_directory as _parse_directory
	config = _parse_directory(_marten_dir, _os.environ['MARTEN_ENV'])
