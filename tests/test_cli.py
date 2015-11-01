from __future__ import print_function

try:
	from unittest.mock import patch
except ImportError:
	from mock import patch

import six

from marten.cli import marten_cli
from marten.configurations import Configuration

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'

if six.PY2:
	print_patch = patch('__builtin__.print')
else:
	print_patch = patch('builtins.print')

def test_marten_cli():
	"""Test the output of marten cli command"""
	d = {'TEST': 1}

	with print_patch as mock:
		with patch('marten.config', Configuration(d)):
			marten_cli()

		mock.assert_called_once_with('{\n    "TEST": 1\n}')