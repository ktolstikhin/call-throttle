import time
import asyncio
from datetime import datetime, timedelta

from .exceptions import ThrottleException


class Throttle:

    def __init__(self, calls=1, period=timedelta(seconds=1), raise_on_throttle=False):
        self._throttle_calls = calls
        self._throttle_period = period
        self._last_call_time = datetime.min
        self._raise_on_throttle = raise_on_throttle
        self._calls = 0

    def _call(self):
        elapsed_time = datetime.now() - self._last_call_time
        self._calls += 1
        sleep_time = 0

        if elapsed_time < self._throttle_period:

            if self._calls >= self._throttle_calls:

                if self._raise_on_throttle:
                    raise ThrottleException('too many calls')

                sleep_time = (self._throttle_period - elapsed_time).total_seconds()
                self._calls = 0

        else:
            self._calls = 0

        return sleep_time

    def call(self):
        sleep_time = self._call()
        time.sleep(sleep_time)
        self._last_call_time = datetime.now()

    async def call_async(self):
        sleep_time = self._call()
        await asyncio.sleep(sleep_time)
        self._last_call_time = datetime.now()
