import threading
import time
import random
import memcache
from MemLock import dist_lock

MC = memcache.Client(['127.0.0.1:11211'], debug=0)

def bk_thread(fn):
    def call_fn(*arg):
        t = threading.Thread(target=fn, args=arg)
        t.start()
        return
    return call_fn


@bk_thread
def test(i):
    with dist_lock(f'test_lock_{i}'):
        MC.set(f'test_{i}', i)
        a = MC.get(f'test_{i}')
        print('a = %r' % a)


def main(cnt):
    i = cnt
    while i > 0:
        test(i)
        i = i - 1
    time.sleep(100) 

if __name__ == "__main__":
    share = 10000
    main(share)
