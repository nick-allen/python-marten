import os
import sys
from unittest import TestCase
from nose.tools import assert_dict_equal

from marten.conf import Configuration, ModuleConfiguration, JSONConfiguration, parse_directory

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


# Add test fixtures to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'fixtures'))


class ReusableTestCaseMetaclass(type):
	"""Force-sets __test__ = True if not supplied"""

	def __new__(mcs, name, parents, dict_):
		dict_.setdefault('__test__', True)
		return super(ReusableTestCaseMetaclass, mcs).__new__(mcs, name, parents, dict_)


class BaseConfigurationTestCase(TestCase):
	"""Base TestCase class for Configuration classes"""

	__test__ = False
	__metaclass__ = ReusableTestCaseMetaclass

	# Fixture files should evaluate to the same dict
	sample_source_dict = {
		'SHOULD_EXIST': 1,
		'_SHOULD_NOT_EXIST': 2,
		'SHOULD_NOT_Exist': 3,
		'shouldNotExist': 4,
		'should_not_exist': 5
	}

	def setUp(self):
		self.configuration = self.get_configuration()

	def get_configuration(self):
		"""Return configuration instance to be used in all generic tests"""
		raise NotImplementedError()

	def test_lazyload_config(self):
		"""Test that the config is lot loaded and parsed until the first request for a configuration"""

		self.assertIsNone(self.configuration._Configuration__config)
		self.assertDictEqual(self.configuration.config, {'SHOULD_EXIST': 1})
		self.assertDictEqual(self.configuration._Configuration__config, {'SHOULD_EXIST': 1})

	def test_getitem(self):
		"""Test that configurations can be accessed like dicts"""
		self.assertEqual(self.configuration['SHOULD_EXIST'], 1)

		with self.assertRaises(KeyError):
			self.configuration['_SHOULD_NOT_EXIST']

	def test_final_config(self):
		"""Test that the configuration matches the parsed sample"""
		self.assertDictEqual(self.configuration.config, {'SHOULD_EXIST': 1})


class ConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the base Configuration class"""

	def get_configuration(self):
		return Configuration(self.sample_source_dict)

	def test_parse_source_as_dict(self):
		"""Test that Configuration.parse_source() returns the initial source"""
		self.assertDictEqual(self.configuration.parse_source(), self.sample_source_dict)

	def test_filter_config(self):
		"""Test that Configuration._get_config_keys() only returns uppercase attributes not starting with underscore"""
		self.assertDictEqual(Configuration._filter_config(self.sample_source_dict), {'SHOULD_EXIST': 1})


class ModuleImportedConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the ModuleConfiguration class"""

	def get_configuration(self):
		return ModuleConfiguration(__import__('module_config'))


class ModuleFSPathStringConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the ModuleConfiguration class"""

	def get_configuration(self):
		return ModuleConfiguration(os.path.join(os.path.dirname(__file__), 'fixtures/module_config.py'))


class ModulePackageStringConfigurationTestCase(BaseConfigurationTestCase):

	def get_configuration(self):
		return ModuleConfiguration('package.config')


class JSONConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the JSONConfiguration class"""

	def get_configuration(self):
		return JSONConfiguration(os.path.join(os.path.dirname(__file__), 'fixtures/static/config.json'))



def test_parse_directory():
	"""Test that the parse_directory function properly merges multiple configuration files"""
	config = parse_directory(os.path.join(os.path.dirname(__file__), 'fixtures/parse_directory'), 'test')

	assert_dict_equal(config.config, {
		"JSON": True,
		"PYTHON": True,
		"DUPLICATE": 'python'
	})
