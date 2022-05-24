import asyncio
import pytz
import datetime
import logging
from math import ceil, floor
from downleth.download import Downloader

async def download_room(room_id: str, download_duration: int, output_file: str):
    d = Downloader(room_id)
    logging.info(f'Downloading stream for room {room_id} for {str(download_duration)} seconds')
    await asyncio.wait(
        {
            d.start(),
            asyncio.sleep(download_duration)
        },
        return_when=asyncio.FIRST_COMPLETED
    )

    logging.info(f'Done downloading {room_id}. Writing file...')
    await d.stop(output_file)

class ScheduleWhen:

    def __init__(self, when_config):
        self._config = when_config
        self._schedule = when_config['schedule'] # 'weekly'
        self._start = datetime.datetime.utcnow()

    def reached(self):
        return datetime.datetime.utcnow() >= self._get_next_weekly_from()

    async def wait(self):
        wait_delta = floor((self._get_next_weekly_from() - datetime.datetime.utcnow()).total_seconds())
        await asyncio.sleep(wait_delta)

    def next_name(self):
        if self._schedule == 'weekly':
            week = self.timeframe_from().isocalendar().week
            year = self.timeframe_from().isocalendar().year
            return f'{year}-{week}'
        raise ValueError(self._schedule)

    def next_duration(self):
        return ceil((self.timeframe_to() - self.timeframe_from()).total_seconds())

    def timeframe_from(self):
        return self._parse_date(self._config['timeframe']['from'], self._config['timeframe']['timezone'])

    def timeframe_to(self):
        return self._parse_date(self._config['timeframe']['to'], self._config['timeframe']['timezone'])

    def _get_next_weekly_from(self):
        # relative to self._start
        # TODO: 
        pass

    def _parse_date(self, date_str, timezone):
        return pytz.timezone(timezone).localize(datetime.datetime.fromisoformat(date_str)).astimezone(pytz.utc)

class Schedule:
    
    def __init__(self, config):
        self._config = config

    async def run_schedule(self):
        while True:
            logging.info(f'{self.name()} is waiting for next execution...')
            (name_format, duration) = await self._await_next_execution()
            logging.info(f'{self.name()} is starting execution')
            stream_name = self.name().format(name_format)
            await download_room(self.where(), duration, stream_name)

    def where(self):
        return self._config['where']

    def name(self):
        return self._config['name']

    async def _await_next_execution(self):
        sw = ScheduleWhen(self._config['when'])

        while not sw.reached():
            await sw.wait()

        return (sw.next_name(), sw.next_duration())


async def run_all_schedules(config):
    streams = [Schedule(item) for item in config['streams']]
    logging.info(f'Running {len(streams)} schedules...')
    await asyncio.wait([
        stream.run_schedule() for stream in streams
    ])
