"""Stupid simple Python configuration environments"""

from __future__ import absolute_import

from marten import loaded_configs

import os as _os

__version__ = '0.6.1'



_os.environ.setdefault('MARTEN_ENV', 'default')

try:
	from .util import get_config_from_env as _get_config
except ImportError:
	config = None
else:
	config = _get_config()
