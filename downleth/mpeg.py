import aiohttp
from downleth.common import HEADERS, get
from downleth.stream import StreamSegment


CHUNK_SIZE = 1024


async def fetch_mpeg(segment: StreamSegment):
    async with aiohttp.ClientSession() as session:
        async with session.get(segment.url, headers=HEADERS, verify_ssl=True) as response:
            while True:
                res = await response.content.read(CHUNK_SIZE)
                if res is None:
                    break
                yield res
