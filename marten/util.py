import os

from marten.configurations import Configuration

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'



def get_supported_extensions():
	"""Returns a dict mapping file extension string to Configuration class that can handle it"""
	supported_extensions = {}

	for cls in Configuration.__subclasses__():
		for ext in cls.file_extensions:
			supported_extensions[ext] = cls

	return supported_extensions


def parse_directory(path, name):
	"""
	Parse path for all supported config file types beginning with name

	Merges multiple configs with the same name into a single Configuration instance, overriding duplicate attributes in
	order files were loaded

	Ignores files with unsupported extensions
	"""
	merged_raw_configs = {}

	supported_extensions = get_supported_extensions()

	for filename in os.listdir(path):
		if filename.startswith(name):
			ext = filename.split(name, 1)[1]
			if ext in supported_extensions:
				config = supported_extensions[ext](os.path.join(path, filename))
				merged_raw_configs.update(config.raw_config)

	return Configuration(merged_raw_configs)


def get_config_from_env():
	"""
	Attempt to build and return a Configuration instance based on the files found in the .marten directory matching the
	MARTEN_ENV environment variable
	"""
	marten_dir = os.path.join(os.getcwd(), '.marten')

	if os.path.isdir(marten_dir):
		config = parse_directory(marten_dir, os.environ['MARTEN_ENV'])
	else:
		config = Configuration({})

	return config

