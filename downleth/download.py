import aiofiles
from downleth.mpeg import SegmentDownload
from downleth.stream import generate_segments

class Downloader:

    def __init__(self, room_id: str):
        self._room_id = room_id

    async def start(self):
        async with aiofiles.open('test.mp4', 'wb') as f:
            async for seg in generate_segments(self._room_id):
                d = SegmentDownload(seg)
                await d.write_to(f)
                await f.flush()

    async def stop(self):
        pass
