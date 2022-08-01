import memcache
import time


class MemLock:

    def __init__(self, exp=10):
        self.client = memcache.Client(['127.0.0.1:11211'], debug=0)
        self.time = {}
        self.exp = int(exp)

    def __del__(self):
        self.client.disconnect_all()

    def acquire_lock(self, key):
        while True:
            value = self.client.get(key)
            if value is None:
                # not find lock key
                if 0 != self.client.add(key, f'lock_{key}', time=self.exp):
                    # Nonzero on success, get the lock
                    self.time[key] = int(time.time())
                    break
            time.sleep(0.001)

    def release_lock(self, key):
        if int(time.time()) - self.time[key] < (self.exp - 1):
            self.time.pop(key)
            self.client.delete(key)
            
