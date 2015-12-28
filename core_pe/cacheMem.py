# Created By: Virgil Dupras
# Created On: 2006/09/14
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import logging

from ._cache import string_to_colors
from .cache import Cache as CacheSql

import threading
tloc = threading.local()
tloc.cache_sql = None

class ReadonlyError(Exception):
    pass

class Borg(object):
    __shared_state = {}
    _initialized = False

    def __init__(self):
        self.__dict__ = self.__shared_state

class CacheMem(Borg):
    """A class to cache picture blocks.
    """
    def __init__(self, db=':memory:'):
        Borg.__init__(self)
        some_rlock = threading.RLock()
        with some_rlock:
            if self._initialized:
                logging.debug("We are the Borg")
                self.using_collective = True
            else:
                logging.debug("Initializing Collective")
                self.__load(db)
                self.using_collective = False

    def load(self, db):
        logging.debug('Forced reload of Collective cache')
        self.__load(db)

    def __load(self, db):
        logging.debug('Instantiating a cache object. Borg state: %s' % repr(self._initialized))
        tloc.cache_sql = CacheSql(db)
        logging.debug('cacheMem loading complete picture cache from %s' % db)
        sql = "select rowid, path, blocks from pictures"
        cur = tloc.cache_sql.con.execute(sql)
        self._c = {}
        self._c = {path: (rowid, string_to_colors(blocks)) for rowid, path, blocks in cur}
        self._i = {v[0]: v[1] for v in self._c.values()}
        tloc.cache_sql.close()
        tloc.cache_sql = None
        logging.debug('cacheMem loaded %d items' % len(self._c))
        # flush the iterators
        import sys
        logging.debug('Cache object size: %s %s %s' % (
            sys.getsizeof(self),
            sys.getsizeof(self._c),
            sys.getsizeof(self._i)))
        self._initialized = True

    def __contains__(self, key):
        return key in self._c

    def __delitem__(self, key):
        raise ReadonlyError('This cache object is read only')

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._i[key] #return blocks only
        else:
            return self._c[key][1]

    def __iter__(self):
        return iter(self._c.keys())

    def __len__(self):
        return len(self._c.keys())

    def __setitem__(self, path_str, blocks):
        raise ReadonlyError('This cache object is read only')

    def clear(self):
        raise ReadonlyError('This cache object is read only')

    def close(self):
        if tloc.cache_sql is not None:
            tloc.cache_sql.close()
        tloc.cache_sql = None

    def filter(self, func):
        raise ReadonlyError('This cache object is read only')

    def get_id(self, path):
        return self._c[path][0]

    def get_multiple(self, rowids):
        return [(e[0], e[1]) for e in self._c.values() if e[0] in rowids]

    def purge_outdated(self):
        raise ReadonlyError('This cache object is read only')
