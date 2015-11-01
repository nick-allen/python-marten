import json
import imp
import os
import collections

import six
import yaml

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


class Configuration(object):
	"""Base Configuration class"""

	file_extensions = ()

	def __init__(self, config_source):
		"""Expects config_source to be a dict"""
		self._source = config_source
		self.__config = None
		self.__raw_config = None

	def __getitem__(self, item):
		"""Lazy-load config using parse_source(), and act like the underlying dict"""
		return self.config[item]

	@property
	def config(self):
		"""Return dict config parsed for environment variables"""
		if self.__config is None:
			self.__config = self._replace_env(self.raw_config)

		return self.__config

	@property
	def raw_config(self):
		"""Returns raw dict config"""
		if self.__raw_config is None:
			self.__raw_config = self._filter_config(self.parse_source())
		return self.__raw_config

	@staticmethod
	def _replace_env(config_dict):
		"""Use os.path.expandvars to parse all values"""
		d = {}
		for key, value in config_dict.items():
			if isinstance(value, collections.Mapping):
				d[key] = Configuration._replace_env(value)
			elif isinstance(value, six.string_types):
				d[key] = os.path.expandvars(value)
			else:
				d[key] = value
		return d

	@staticmethod
	def _filter_config(config_dict):
		"""Returns keys in iterable that are uppercase and do not start with underscore"""
		return {key: val for key, val in config_dict.items() if key.isupper() and not key.startswith('_')}

	def parse_source(self):
		"""Default no-op returning self._source"""
		return self._source


class ModuleConfiguration(Configuration):
	"""Configuration from an imported python module, dot-string, or full file path to a module"""

	file_extensions = ('.py',)

	def parse_source(self):
		"""Load module if provided a dot-string, then parse config from module"""
		if isinstance(self._source, six.string_types):
			if os.path.isfile(self._source):
				module = imp.load_source(self._source, self._source)
			else:
				module = __import__(self._source, fromlist=['*'])
		else:
			module = self._source

		return {key: getattr(module, key) for key in dir(module)}


class JSONConfiguration(Configuration):
	"""Parse JSON file"""

	file_extensions = ('.json',)

	def parse_source(self):
		"""Read file and parse as JSON"""
		with open(self._source) as f:
			return json.load(f)


class YAMLConfiguration(Configuration):
	"""Parse YAML file"""

	file_extensions = ('.yml', '.yaml')

	def parse_source(self):
		"""Read file and parse as YAML"""
		with open(self._source) as f:
			return yaml.load(f)



supported_extensions = {}

for cls in Configuration.__subclasses__():
	for ext in cls.file_extensions:
		supported_extensions[ext] = cls


def parse_directory(path, name):
	"""
	Parse path for all supported config file types beginning with name

	Merges multiple configs with the same name into a single Configuration instance, overriding duplicate attributes in
	order files were loaded

	Ignores files with unsupported extensions
	"""
	configs = {}

	if os.path.isdir(path):
		for filename in os.listdir(path):
			if filename.startswith(name):
				ext = filename.split(name, 1)[1]
				if ext in supported_extensions:
					config = supported_extensions[ext](os.path.join(path, filename))
					configs.update(config.raw_config)

		return Configuration(configs)

	else:
		raise ValueError('`{}` is not a directory'.format(path))