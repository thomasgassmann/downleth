import asyncio
import logging
import aiofiles
import aiofiles.os
from ffmpeg import FFmpeg
from downleth.common import OrderedDownloadQueue
from downleth.mpeg import SegmentDownload
from downleth.stream import generate_segments

class Downloader:

    def __init__(self, room_id: str):
        self._room_id = room_id
        self._should_run = True
        self._download_queue = OrderedDownloadQueue()
        self._temp_file = None
        self._download_done = asyncio.Event()

    async def start(self):
        await asyncio.gather(
            self._fill_queue(),
            self._empty_queue()
        )

    async def stop(self, out_path):
        self._should_run = False
        await self._finalize_download(out_path)

    async def _empty_queue(self):
        async with aiofiles.tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            self._temp_file = f.name
            async for d in self._download_queue.stream():
                await d.write_to(f)
        self._download_done.set()
        
    async def _fill_queue(self):
        async for seg in generate_segments(self._room_id):
            if not self._should_run:
                break

            logging.debug(f'Found segment {seg.seg_id} in room {self._room_id}. Adding to download queue...')
            d = SegmentDownload(seg)
            self._download_queue.push(seg.seg_id, d)
        self._download_queue.end_stream()

    async def _finalize_download(self, out_path):
        if self._temp_file is None:
            raise ValueError('something has gone quite wrong')
        
        logging.info(f'Waiting for all downloads to finish in {self._room_id}')
        await self._download_done.wait()

        # TODO: catch errors, see docs to capture progress, etc.
        logging.info(f'Converting file for room {self._room_id} using ffmpeg. Writing to {out_path}')
        await FFmpeg() \
            .option('y') \
            .input(self._temp_file) \
            .output(out_path) \
            .execute()

        logging.debug(f'Removing {self._temp_file}')
        await aiofiles.os.remove(self._temp_file)
