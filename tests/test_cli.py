from __future__ import print_function

from mock import patch

from marten.cli import marten_cli
from marten.conf import Configuration

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'



def test_marten_cli():
	"""Test the output of marten cli command"""
	d = {'TEST': 1}

	with patch('__builtin__.print') as mock:
		with patch('marten.config', Configuration(d)):
			marten_cli()

		mock.assert_called_once_with('{\n    "TEST": 1\n}')