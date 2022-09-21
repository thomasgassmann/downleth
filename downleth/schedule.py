import asyncio
import pytz
import datetime
import logging
from copy import deepcopy
from math import ceil, floor
from downleth.download import Downloader

async def download_room(room_id: str, download_duration: int, output_file: str, cache_dir: str | None):
    d = Downloader(room_id, cache_dir)
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

PERIOD_WEEKLY = 'weekly'
PERIOD_ONCE = 'once'

class NoFurtherExecutionException(Exception):
    def __init__(self, name) -> None:
        self.name = name

class ScheduleWhen:

    def __init__(self, when_config, friendly_name_fn):
        self._config = when_config
        self._schedule = when_config['schedule'] # 'weekly'
        self._start = self._tz_aware_now()
        self._friendly_name_fn = friendly_name_fn

    def reached(self):
        if self._tz_aware_now() >= self._get_next_from() and self._tz_aware_now() <= self._get_next_to():
            return True # lecture is happening now, TODO: it is probably not

        if self._get_next_from() >= self._get_next_to():
            return True # lecture is really happening now

        # yes, the below comment is useless actually
        return False # not sure what is going on, will figure it out, actually no i just figured it out, see above

    async def wait(self):
        if self.reached():
            return # no need to wait

        wait_delta = floor((self._get_next_from() - self._tz_aware_now()).total_seconds())
        if wait_delta < -1:
            raise NoFurtherExecutionException(self._friendly_name_fn(self))

        wait_until = self._tz_aware_now() + datetime.timedelta(seconds=wait_delta)
        logging.info(f'Waiting for {self._friendly_name_fn(self)} until {wait_until}')

        await asyncio.sleep(wait_delta)

    def next_name(self):
        if self._schedule == PERIOD_WEEKLY:
            week = self.timeframe_from().isocalendar().week
            year = self.timeframe_from().isocalendar().year
            return f'{year}-{week}'
        if self._schedule == PERIOD_ONCE:
            return ''
        raise ValueError(self._schedule)

    def next_duration(self):
        start = self._get_next_from()
        if self._tz_aware_now() <= self._get_next_to() and self._tz_aware_now() >= self._get_next_from():
            start = self._tz_aware_now()
        if self._get_next_from() >= self._get_next_to():
            start = self._tz_aware_now()

        return ceil((self._get_next_to() - start).total_seconds())

    def timeframe_from(self):
        return self._parse_date(self._config['timeframe']['from'], self._config['timeframe']['timezone'])

    def timeframe_to(self):
        return self._parse_date(self._config['timeframe']['to'], self._config['timeframe']['timezone'])

    def _get_next_from(self):
        return self._get_next_offset(self.timeframe_from())

    def _get_next_to(self):
        return self._get_next_offset(self.timeframe_to())

    def _get_next_offset(self, d):
        if self._schedule == PERIOD_ONCE:
            return d

        # relative to self._start
        offset = self._get_offset_delta()
        offset_seconds = floor(offset.total_seconds())
        seconds = floor((d - self._start).total_seconds()) % offset_seconds
        return self._start + datetime.timedelta(seconds=seconds)

    def _get_offset_delta(self):
        if self._schedule == PERIOD_WEEKLY:
            return datetime.timedelta(days=7)
        if self._schedule == PERIOD_ONCE:
            return datetime.timedelta.max
        raise ValueError(self._schedule)

    def _parse_date(self, date_str, timezone):
        return pytz.timezone(timezone).localize(datetime.datetime.fromisoformat(date_str)).astimezone(pytz.utc)

    def _tz_aware_now(self):
        return datetime.datetime.now(pytz.utc)

class Schedule:
    
    def __init__(self, config, cache_dir):
        self._config = config
        self._cache_dir = cache_dir

    async def run_schedule(self):
        while True:
            try:
                (stream_name, duration) = await self._await_next_execution()
                await download_room(self.where(), duration, stream_name, self._cache_dir)
            except NoFurtherExecutionException as e:
                logging.info(f'No further execution for schedule {e.name}')
                return

    def where(self):
        return self._config['where']

    def name_template(self):
        return self._config['name']

    def name(self, sw):
        return self.name_template().format(self._details(sw))

    def _details(self, sw):
        if 'detail' in self._config and self._config['detail']:
            detail = self._config['detail']
            return f'{detail}-{sw.next_name()}'

        return sw.next_name()

    async def _await_next_execution(self):
        sw = ScheduleWhen(self._config['when'], self.name)
        logging.info(f'{self.name(sw)} is waiting for next execution...')
        while not sw.reached():
            await sw.wait()
        logging.info(f'{self.name(sw)} is starting execution')
        return (self.name(sw), sw.next_duration())


def flatten_schedule(config):
    flattened_streams = []

    for stream in config['streams']:
        if isinstance(stream['where'], list):
            for location in stream['where']:           
                copy = deepcopy(stream)
                copy['where'] = location
                existing_detail = None if 'detail' not in copy else copy['detail']
                copy['detail'] = f'{location}-{existing_detail}' if existing_detail else location
                flattened_streams.append(copy)
        else:
            flattened_streams.append(stream)

    config['streams'] = flattened_streams
    return config


async def run_all_schedules(config):
    flattened = flatten_schedule(config)
    streams = [Schedule(item, flattened['cache_location']) for item in flattened['streams']]
    logging.info(f'Running {len(streams)} schedules...')
    if len(streams) == 0:
        logging.info('Nothing to do. Exiting...')
        return

    await asyncio.wait([
        stream.run_schedule() for stream in streams
    ])
