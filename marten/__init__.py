from __future__ import absolute_import

import os as _os
from .conf import parse_directory as _parse_directory

__version__ = '0.1.0'



# Attempt to auto-load a default configuration from files in <cwd>/.marten/ based on the MARTEN_ENV env variable
# MARTEN_ENV defaults to 'default'
config = _parse_directory(_os.path.join(_os.getcwd(), '.marten'), _os.environ.get('MARTEN_ENV', 'default'))
