import json

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


class Configuration(object):
	"""Base Configuration class"""

	def __init__(self, config_source):
		"""Expects config_source to be dict-like"""
		self._source = config_source
		self.__config = None

	def __getitem__(self, item):
		"""Lazy-load config using parse_source(), and act like the underlying dict"""
		return self.config[item]

	def __repr__(self):
		return repr(self.config)

	def __str__(self):
		return str(self.config)

	@property
	def config(self):
		"""Lazy-load config"""
		if self.__config is None:
			self.__config = self._filter_config(self.parse_source())
		return self.__config

	@staticmethod
	def _filter_config(config_dict):
		"""Returns keys in iterable that are uppercase and do not start with underscore"""
		return {key: val for key, val in config_dict.iteritems() if key.isupper() and not key.startswith('_')}

	def parse_source(self):
		"""Default no-op returning self._source"""
		return self._source


class ModuleConfiguration(Configuration):
	"""Configuration from an imported python module or dot-string pointing to a module"""

	def parse_source(self):
		"""Load module if provided a dot-string, then parse config from module"""
		if isinstance(self._source, basestring):
			module = __import__(self._source, fromlist=['*'])
		else:
			module = self._source

		return {key: getattr(module, key) for key in dir(module)}


class FileConfiguration(Configuration):
	"""Parse configuration from a static file"""

	def __init__(self, filepath, parse_function):
		"""Expects parse_function(file_content) to return a dict"""
		super(FileConfiguration, self).__init__(filepath)
		self.__parse_function = parse_function

	def parse_source(self):
		"""Read file and run through parse function, returning all uppercase keys and their respective values"""
		with open(self._source) as f:
			content = f.read()

		return self.__parse_function(content)


class JSONConfiguration(FileConfiguration):
	"""Parse JSON file"""

	def __init__(self, filepath):
		super(JSONConfiguration, self).__init__(filepath, json.loads)


