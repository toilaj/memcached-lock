"""
    memcached_lock
    ~~~~~~~~~~~~~~
    Implements a distributed transaction using memcached or
    a memcached compatible storage.
    Example::
        from __future__ import with_statement
        import memcache
        from memcached_lock import dist_lock
        client = memcache.Client(['127.0.0.1:11211'])
        with dist_lock('test', client):
            print 'Is there anybody out there!?'
    :modify from amix the lucky stiff.
    :license: BSD
"""
import time
from contextlib import contextmanager
from random import random
import memcache

DEFAULT_EXPIRES = 15
DEFAULT_RETRIES = 5

client = memcache.Client(['127.0.0.1:11211'], debug=0)

@contextmanager
def dist_lock(key):
    key = '__d_lock_%s' % key

    try:
        _acquire_lock(key, client)
        yield
    finally:
        _release_lock(key, client)

def _acquire_lock(key, client):
    for i in range(0, DEFAULT_RETRIES):
        stored = client.add(key, 1, DEFAULT_EXPIRES)
        if stored:
            return
        sleep_time = (((i+1)*random()) + 2**i) / 2.5
        print('Sleeipng for %s' % (sleep_time))
        time.sleep(sleep_time)
    raise Exception('Could not acquire lock for %s' % key)

def _release_lock(key, client):
    client.delete(key)
