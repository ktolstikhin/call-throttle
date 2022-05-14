import asyncio
from datetime import datetime

from ..base import ThrottleBase


class Throttle(ThrottleBase):

    async def call(self):
        sleep_time = self._call()
        await asyncio.sleep(sleep_time)
        self._last_call_time = datetime.now()
