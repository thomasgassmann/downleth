class PurgedSet:
    
    def __init__(self, bound: int):
        self._bound = bound
        self._mod = 2 * bound
        self._set = [False] * self._mod

    def mark(self, seg: int):
        self._set[seg % self._mod] = True
        self._set[(seg - self._bound) % self._mod] = False

    def has_recently_seen(self, seg: int):
        return self._set[seg % self._mod]
