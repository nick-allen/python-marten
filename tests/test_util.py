import os

from mock import patch
from nose.tools import assert_equal, assert_raises

from marten.util import parse_directory, get_config_from_env

__author__ = 'Nick Allen <nick.allen.cse@gmail.com>'


TEST_DIR = os.path.dirname(__file__)

def test_parse_directory():
	"""Test that the parse_directory function properly merges multiple configuration files"""
	config = parse_directory(os.path.join(TEST_DIR, 'fixtures/parse_directory'), 'test')

	assert_equal(config.config, {
		"JSON": True,
		"PYTHON": True,
		"DUPLICATE": 'python'
	})

	with assert_raises(OSError):
		parse_directory('/Not/a/real/path', 'test')


def test_missing_marten_dir():
	"""Test that the get_config_from_env() function returns an empty Configuration instance if the <cwd>/.marten directory is missing"""
	with patch('marten.util.os.getcwd', return_value='/Not/a/real/path'):
		config = get_config_from_env()

	assert_equal(config.config, {})


def test_existing_marten_dir():
	"""
	Test that the get_config_from_env() function returns a Configuration instance using files matching the MARTEN_ENV
	environment variable if the <cwd>/.marten directory exists
	"""
	with patch('marten.util.os.getcwd', return_value=os.path.join(TEST_DIR, 'fixtures')):
		default_config = get_config_from_env()

		assert_equal(default_config.config, {'MARTEN_FIXTURE': True})

		with patch('marten.util.os.environ', {'MARTEN_ENV': 'manual'}):
			manual_config = get_config_from_env()

			assert_equal(manual_config.config, {'MARTEN_FIXTURE': False})

