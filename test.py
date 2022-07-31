import MemLock
import threading
import time
import random
import memcache

MC = memcache.Client(['127.0.0.1:11211'], debug=0)
MEMLOCK = MemLock.MemLock()


def bk_thread(fn):
    def call_fn(*arg):
        t = threading.Thread(target=fn, args=arg)
        t.start()
        return

    return call_fn


@bk_thread
def test(i):
    MEMLOCK.acquire_lock('0')
    time.sleep(random.random())
    a = MC.get('test')
    a = a - 1
    MC.set('test', a)
    print('a = %r' % a)
    MEMLOCK.release_lock('0')
    return


def main(cnt):
    i = cnt
    while i > 0:
        test(i)
        i = i - 1
    time.sleep(100)


if __name__ == "__main__":
    share = 100
    MC.delete("test")
    MC.add('test', share)
    main(share)
    print("result = %s" % MC.get('test'))
