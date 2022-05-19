import asyncio
from downleth.download import Downloader

def run_schedule(config):
    d = Downloader('hg-f-7')
    asyncio.get_event_loop().run_until_complete(d.start())
    # d.stop()
