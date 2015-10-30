import copy
import json
import imp
import os

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


class Configuration(object):
	"""Base Configuration class"""

	file_extension = None

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
		"""Lazy-load config"""
		if self.__config is None:
			self.__config = self._replace_env(self.raw_config)

		return self.__config

	@property
	def raw_config(self):
		if self.__raw_config is None:
			self.__raw_config = self._filter_config(self.parse_source())
		return self.__raw_config

	@staticmethod
	def _replace_env(config_dict):
		"""
		Replace all $VAR environment variables in dict values

		Treat $$VAR as escaped to actual $VAR
		"""
		d = copy.copy(config_dict)

		for key, val in config_dict.iteritems():
			if isinstance(val, basestring) and val.isupper() and val.startswith('$'):
				new_val = val[1:]
				if new_val.startswith('$'):
					d[key] = new_val
				else:
					d[key] = os.environ.get(new_val, '')

		return d

	@staticmethod
	def _filter_config(config_dict):
		"""Returns keys in iterable that are uppercase and do not start with underscore"""
		return {key: val for key, val in config_dict.iteritems() if key.isupper() and not key.startswith('_')}

	def parse_source(self):
		"""Default no-op returning self._source"""
		return self._source


class ModuleConfiguration(Configuration):
	"""Configuration from an imported python module, dot-string, or full file path to a module"""

	file_extension = '.py'

	def parse_source(self):
		"""Load module if provided a dot-string, then parse config from module"""
		if isinstance(self._source, basestring):
			if os.path.isfile(self._source):
				module = imp.load_source(os.urandom(20).encode('hex'), self._source)
			else:
				module = __import__(self._source, fromlist=['*'])
		else:
			module = self._source

		return {key: getattr(module, key) for key in dir(module)}


class JSONConfiguration(Configuration):
	"""Parse JSON file"""

	file_extension = '.json'

	def parse_source(self):
		"""Read file and run through parse function, returning all uppercase keys and their respective values"""
		with open(self._source) as f:
			return json.load(f)



supported_extensions = {}

for cls in Configuration.__subclasses__():
	if cls.file_extension:
		supported_extensions[cls.file_extension] = cls


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
					configs.update(config.config)

		return Configuration(configs)

	else:
		raise ValueError('`{}` is not a directory'.format(path))