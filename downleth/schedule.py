import aiofiles
import asyncio
from downleth.download import Downloader

async def run_schedule(config):
    d = Downloader('hg-e-5')
    await asyncio.wait(
        {
            d.start(),
            asyncio.sleep(10)
        },
        return_when=asyncio.FIRST_COMPLETED
    )

    await d.stop('out.mp4')
