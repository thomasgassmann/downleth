import heapq
import asyncio

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'pragma': 'no-cache',
    'accept-encoding': 'gzip, deflate, br',
    'accept': '*/*'
}


class OrderedDownloadQueue:

    def __init__(self):
        self._q = []
        self._added = asyncio.Event()
        self._last_returned = None
        self._stream_running = True

    def push(self, order: int, item):
        heapq.heappush(self._q, (order, item))
        self._added.set()

    def end_stream(self):
        self._stream_running = False

    async def stream(self):
        while self._stream_running or len(self._q) > 0:
            if len(self._q) == 0 or (self._last_returned is not None and self._q[0][0] != self._last_returned + 1):
                await self._added.wait()
                self._added.clear()
                continue

            res = heapq.heappop(self._q)
            self._last_returned = res[0]
            yield res[1]



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
