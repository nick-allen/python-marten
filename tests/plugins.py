# Nose plugins for testing marten

import sys 

from nose.plugins import Plugin

class ResetMartenPythonCachePlugin(Plugin):
	name = 'martencachereset'

	def configure(self, options, conf):
		super(ResetMartenPythonCachePlugin, self).configure(options, conf)
		self.enabled = True

	def reset_loaded_configs(self):
		"""Clears out any module cache on loaded python modules used as dynamically imported modules"""
		for mod in list(sys.modules.keys()):
			if mod.startswith('marten.loaded_configs.'):
				sys.modules.pop(mod)

	def afterTest(self, test):
		self.reset_loaded_configs()
