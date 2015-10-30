"""Console Entrypoints"""

from __future__ import print_function

import marten
import json

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'



def marten_cli():
	"""Outputs parsed config at martin.config as JSON"""
	if marten.config is not None:
		print(json.dumps(
			marten.config.config,
			sort_keys=True,
			indent=4
		))