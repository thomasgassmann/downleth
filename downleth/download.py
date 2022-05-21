import aiofiles
from downleth.mpeg import SegmentDownload
from downleth.stream import generate_segments

class Downloader:

    def __init__(self, room_id: str):
        self._room_id = room_id

    async def start(self):
        async for seg in generate_segments(self._room_id):
            async with aiofiles.open(f'out/{seg.seg_id}.ts', 'wb') as f:
                d = SegmentDownload(seg)
                await d.write_to(f)

    async def stop(self):
        pass
