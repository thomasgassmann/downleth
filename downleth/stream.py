import aiohttp
import m3u8
import random
import asyncio

CACHE_BUST = random.randint(10 ** 9, 10 ** 10)
SERVER = random.randint(1, 2)
INDEX_TEMPLATE = 'https://oc-vp-livestreaming0{0}.ethz.ch/hls/{1}/index.m3u8?cache={2}'
PURGED_SET_SIZE = 5000
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    'pragma': 'no-cache',
    'accept-encoding': 'gzip, deflate, br',
    'accept': '*/*'
}

def get_index_url(room_id: str):
    return INDEX_TEMPLATE.format(SERVER, room_id, CACHE_BUST)

async def get_index(room_id: str) -> m3u8.M3U8:
    url = get_index_url(room_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS, verify_ssl=True) as response:
            text = await response.text()
            res = m3u8.M3U8(text, base_uri=str(response.url))
            return res

class PurgedSet:
    
    # TODO: yeah, so this doesn't work
    def __init__(self, bound: int):
        self._bound = bound
        self._mod = 3 * bound
        self._set = [False] * self._mod
        self._markings = 0

    def mark(self, seg: int):
        self._markings += 1
        if self._markings >= self._bound:
            self.clear_from(seg)

        self._set[seg % self._mod] = True

    def has_recently_seen(self, seg: int):
        return self._set[seg % self._mod]

    def clear_from(self, seg: int):
        self._markings = 0
        # clear items in [seg + bound, seg - bound] mod _mod
        from_clear = (seg + self._bound) % self._mod
        to_clear = (seg - self._bound) % self._mod
        while from_clear != to_clear:
            self._set[from_clear] = False
            from_clear = (from_clear + 1) & self._mod


class Segment:
    pass

# generates segments asynchronously, a segment is guaranteed to be returned only once
# however, the segments are not guaranteed to arrive in order, this allows a consumer
# to avoid issues similar to TCP head-of-line blocking
async def generate_segments(room_id: str):
    index = await get_index(room_id)
    wait_time = index.target_duration
    purged_set = PurgedSet(PURGED_SET_SIZE)
    while True:
        for segment in index.segments:
            seg_id = int(segment.uri[:-3])
            if not purged_set.has_recently_seen(seg_id):
                yield segment
                purged_set.mark(seg_id)

        [_, index] = await asyncio.gather(
            asyncio.sleep(wait_time),
            get_index(room_id)
        )
