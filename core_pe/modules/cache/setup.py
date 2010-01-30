# Created By: Virgil Dupras
# Created On: 2009-04-23
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from distutils.core import setup
from distutils.extension import Extension

setup(
    ext_modules = [Extension("_cache", ["cache.c"])]
)