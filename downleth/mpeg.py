import logging
import aiohttp
import asyncio
from downleth.common import HEADERS
from downleth.stream import StreamSegment

CHUNK_SIZE = 1024
RETRY_COUNT = 5

class SegmentDownload:
    
    def __init__(self, seg: StreamSegment):
        self._seg = seg

    async def write_to(self, stream: asyncio.StreamWriter):
        logging.debug(f'Writing segment {self._seg.seg_id} to stream...')
        async for chunk in self.fetch_mpeg_content():
            await stream.write(chunk)

    async def fetch_mpeg_content(self):
        retries = RETRY_COUNT
        while retries > 0:
            try:
                content = []
                async with aiohttp.ClientSession() as session:
                    async with session.get(self._seg.url, headers=HEADERS, verify_ssl=True) as response:
                        while True:
                            res = await response.content.read(CHUNK_SIZE)
                            if res == b'':
                                break
                            content.append(res)
                
                for item in content:
                    yield item
                break
            except:
                logging.error('Could not fetch mpeg content. Retrying...')
                retries -= 1
