import asyncio
from downleth.stream import generate_segments

class Downloader:

    def __init__(self, room_id: str):
        self._room_id = room_id
    
    async def start(self):
        async for seg in generate_segments(self._room_id):
            print(seg)
            # download, merge segments

    async def stop(self):
        pass
