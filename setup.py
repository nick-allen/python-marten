#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from marten import __version__, __doc__

def parse_requirements(requirements):
	with open(requirements) as f:
		return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

try:
	from StringIO import StringIO
except ImportError:
	from io import StringIO

import sys
stderr = sys.stderr
sys.stderr = StringIO()

try:
	from pypandoc import convert
	long_description = convert('README.md', 'rst')
except (ImportError, OSError):
	long_description = __doc__

sys.stderr = stderr

test_requirements = parse_requirements('test-requirements.txt')

setup(
	name='marten',
	version=__version__,
	packages=find_packages(exclude=('tests.*', 'tests',)),
	url='https://github.com/nick-allen/python-marten',
	license='MIT',
	author='Nick Allen',
	author_email='nick.allen.cse@gmail.com',
	description=__doc__,
	long_description=long_description,
	include_package_data=True,
	zip_safe=False,
	install_requires=parse_requirements('requirements.txt'),
	extras_require={
		'test': test_requirements
	},
	entry_points={
		'console_scripts': [
			'marten = marten.cli:marten_cli'
		]
	},
	test_suite='nose.collector',
	tests_require=test_requirements
)
