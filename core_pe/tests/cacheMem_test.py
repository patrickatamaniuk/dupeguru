# Created By: Patrick Atamaniuk
# Created On: 2015/12/28
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import logging, sys

from pytest import raises, skip
from hscommon.testutil import eq_

try:
    from ..cache import Cache as CacheSql, colors_to_string, string_to_colors
except ImportError:
    skip("Can't import the cache module, probably hasn't been compiled.")
from ..cacheMem import CacheMem as Cache

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

class TestBorg:
    def test_rmdb(self):
        #os.unlink('test.db')
        c0 = CacheSql('test.db')
        c0.clear()
        c = Cache('test.db')
        c.load('test.db')
        eq_(len(c0), 0)

    def test_is_borg(self):
        c1 = Cache('test.db')
        c2 = Cache('test.db')
        assert c1 is not c2 #borg, not singleton
        assert c1._c is c2._c
#        assert c1.con is c2.con
        #assert c1._c['cache'] is c2._c['cache']

    def test_set_then_retrieve_blocks(self):
        c0 = CacheSql('test.db')
        c0.clear()
        eq_(len(c0), 0)
        c1 = Cache('test.db')
        c2 = Cache('test.db')
        eq_(len(c1), 0)
        eq_(len(c2), 0)

        b = [(0,0,0),(1,2,3)]
        c0['foo'] = b
        c1.load('test.db')
        c2.load('test.db')
        eq_(len(c0), 1)
        eq_(len(c1), 1)
        eq_(len(c2), 1)
        assert c1['foo'] is c2['foo']

        c3 = Cache()
        eq_(len(c3), 1)
        eq_(b,c3['foo'])

    def test_clear(self):
        """last test clears cache as next test would fail"""
        c = CacheSql()
        c.clear()

class TestCaseCache:
    def test_rmdb(self):
        #os.unlink('test.db')
        c0 = CacheSql('test.db')
        c0.clear()
        c = Cache('test.db')
        c.load('test.db')
        eq_(len(c0), 0)

    def test_empty(self):
        c = Cache('test.db')
        c.load('test.db')
        eq_(0, len(c))
        with raises(KeyError):
            c['foo']

    def test_set_then_retrieve_blocks(self):
        c = CacheSql('test.db')
        b = [(0,0,0),(1,2,3)]
        c['foo'] = b
        c = Cache('test.db')
        c.load('test.db')
        eq_(b,c['foo'])

    def test_by_id(self):
        # it's possible to use the cache by referring to the files by their row_id
        c = CacheSql('test.db')
        b = [(0,0,0),(1,2,3)]
        c['foo'] = b
        c = Cache('test.db')
        c.load('test.db')
        foo_id = c.get_id('foo')
        eq_(c[foo_id], b)

