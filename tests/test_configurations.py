import os
import sys
from unittest import TestCase

from six import with_metaclass
import mock

from marten.configurations import Configuration, PythonConfiguration, JSONConfiguration, YAMLConfiguration

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


TEST_DIR = os.path.dirname(__file__)

os.environ['MARTEN_TEST_VAR'] = 'test_value'

# Add test fixtures to path
sys.path.append(os.path.join(TEST_DIR, 'fixtures'))


class ReusableTestCaseMetaclass(type):
	"""Force-sets __test__ = True if not supplied"""

	def __new__(mcs, name, parents, dict_):
		dict_.setdefault('__test__', True)
		return super(ReusableTestCaseMetaclass, mcs).__new__(mcs, name, parents, dict_)


class BaseConfigurationTestCase(with_metaclass(ReusableTestCaseMetaclass, TestCase)):
	"""Base TestCase class for Configuration classes"""

	__test__ = False

	# Fixture files should evaluate to the same dict
	sample_source_dict = {
		'SHOULD_EXIST': 1,
		'_SHOULD_NOT_EXIST': 2,
		'SHOULD_NOT_Exist': 3,
		'shouldNotExist': 4,
		'NESTED': {
			'MARTEN_TEST_VAR': 'Value: ${MARTEN_TEST_VAR}'
		}
	}

	def setUp(self):
		self.configuration = self.get_configuration()

	def get_configuration(self):
		"""Return configuration instance to be used in all generic tests"""
		raise NotImplementedError()


	def test_lazyload_config(self):
		"""Test that the config is lot loaded and parsed until the first request for a configuration"""
		self.assertIsNone(self.configuration._Configuration__config)
		self.assertEqual(self.configuration.config, {
			'SHOULD_EXIST': 1,
			'NESTED': {
				'MARTEN_TEST_VAR': 'Value: test_value'
			}
		})
		self.assertEqual(self.configuration._Configuration__config, self.configuration.config)

	def test_getitem(self):
		"""Test that configurations can be accessed like dicts"""
		self.assertEqual(self.configuration['SHOULD_EXIST'], 1)

		with self.assertRaises(KeyError):
			self.configuration['_SHOULD_NOT_EXIST']


class ConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the base Configuration class"""

	def get_configuration(self):
		return Configuration(self.sample_source_dict)

	def test_parse_source_as_dict(self):
		"""Test that Configuration.parse_source() returns the initial source"""
		self.assertEqual(self.configuration.parse_source(), self.sample_source_dict)

	def test_filter_config(self):
		"""Test that Configuration._filter_config() only returns uppercase attributes not starting with underscore"""
		self.assertEqual(
			sorted(Configuration._filter_config(self.sample_source_dict).keys()),
			sorted(['SHOULD_EXIST', 'NESTED'])
		)

	def test_replace_env(self):
		"""Test that Configuration._replace_env() correctly replaces $VAR entries"""
		input_dict = {
			'REPLACE': '$VAR',
			'EMPTY': '$EMPTY',
			'KEEP': 'VAR',
			'INTERLACED': '_ $VAR with other content'
		}
		output_dict = {
			'REPLACE': 'value',
			'EMPTY': '$EMPTY',
			'KEEP': 'VAR',
			'INTERLACED': '_ value with other content'
		}
		with mock.patch('os.environ', {'VAR': 'value'}):
			self.assertEqual(Configuration._replace_env(input_dict), output_dict)

	def test_repr(self):
		"""Test the repr() can be used to reconstruct a Configuration instance"""
		new_config = eval(repr(self.configuration))

		self.assertIsNot(new_config, self.configuration)
		self.assertEqual(new_config.config, self.configuration.config)

	def test_str(self):
		"""Test the str() returns expected output"""
		self.assertEqual(str(self.configuration), str(self.configuration.config))

	def test_keys(self):
		"""Test that keys() returns config.keys()"""
		self.assertEqual(self.configuration.keys(), self.configuration.config.keys())

	def test_values(self):
		"""Test that values() returns config.values()"""
		self.assertEqual(list(self.configuration.values()), list(self.configuration.config.values()))

	def test_copy(self):
		"""Test that copy() returns config.copy()"""
		self.assertEqual(self.configuration.copy(), self.configuration.config.copy())

	def test_items(self):
		"""Test that items() returns config.items()"""
		self.assertEqual(dict(self.configuration.items()), dict(self.configuration.config.items()))
			
	def test_get(self):
		"""Test that get() returns config.get()"""
		self.assertEqual(self.configuration.get('SHOULD_EXIST'), 1)
		self.assertEqual(self.configuration.get('NESTED'), self.configuration.config.get('NESTED'))
	


class ModuleImportedConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the PythonConfiguration class"""

	def get_configuration(self):
		return PythonConfiguration(__import__('module_config'))


class ModuleFSPathStringConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the PythonConfiguration class"""

	def get_configuration(self):
		return PythonConfiguration(os.path.join(TEST_DIR, 'fixtures/module_config.py'))


class ModulePackageStringConfigurationTestCase(BaseConfigurationTestCase):

	def get_configuration(self):
		return PythonConfiguration('package.config')


class JSONConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the JSONConfiguration class"""

	def get_configuration(self):
		return JSONConfiguration(os.path.join(TEST_DIR, 'fixtures/static/config.json'))


class YAMLConfigurationTestCase(BaseConfigurationTestCase):
	"""Tests for the YAMLConfiguration class"""

	def get_configuration(self):
		return YAMLConfiguration(os.path.join(TEST_DIR, 'fixtures/static/config.yaml'))