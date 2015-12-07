#!/usr/bin/env python
from __future__ import absolute_import

import nose
from tests.plugins import ResetMartenPythonCachePlugin 

if __name__ == '__main__': 
	nose.main(addplugins=[ResetMartenPythonCachePlugin()])
