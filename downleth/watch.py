import asyncio
import subprocess
from downleth.download import Downloader


async def watch(room_id: str):
    d = Downloader(room_id, None)
    await asyncio.wait([
        d.start(),
        _open(d)
    ])

async def _open(d: Downloader):
    await asyncio.sleep(10)
    subprocess.call(('xdg-open', d._temp_file))
