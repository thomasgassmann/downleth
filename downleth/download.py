import asyncio
from downleth.stream import generate_segments

class Downloader:
    
    async def exec(self):
        async for seg in generate_segments('hg-f-7'):
            print(seg)
            # download, merge segments

    def __init__(self, config):
        asyncio.get_event_loop().run_until_complete(self.exec())

