import aiofiles
import asyncio
from downleth.download import Downloader

async def download_room(room_id: str, until: int):
    d = Downloader('hg-e-5')
    await asyncio.wait(
        {
            d.start(),
            asyncio.sleep(100)
        },
        return_when=asyncio.FIRST_COMPLETED
    )

    await d.stop('out.mp4')

async def run_schedule(config):
    d = Downloader('hg-e-5')
    await asyncio.wait(
        {
            d.start(),
            asyncio.sleep(100)
        },
        return_when=asyncio.FIRST_COMPLETED
    )

    await d.stop('out.mp4')
