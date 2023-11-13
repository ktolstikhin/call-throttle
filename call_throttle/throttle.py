import time
import asyncio
import threading
from abc import ABC, abstractmethod

from .exceptions import ThrottleException


class ThrottleBase(ABC):
    def __init__(self, calls, period, raise_on_throttle=False):
        self._throttle_calls = calls
        self._throttle_period = period
        self._last_call_time = 0
        self._raise_on_throttle = raise_on_throttle
        self._calls = 0

    def __enter__(self):
        elapsed_time = time.perf_counter() - self._last_call_time
        self._calls += 1
        sleep_time = 0

        if elapsed_time < self._throttle_period:
            if self._calls >= self._throttle_calls:
                if self._raise_on_throttle:
                    raise ThrottleException("too many calls")

                sleep_time = self._throttle_period - elapsed_time
                self._calls = 0

        else:
            self._calls = 0

        return sleep_time

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._last_call_time = time.perf_counter()

    @abstractmethod
    def wait(self):
        ...


class Throttle(ThrottleBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = threading.RLock()

    def wait(self):
        with self._lock:
            with self as throttle:
                time.sleep(throttle)


class AsyncThrottle(ThrottleBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lock = asyncio.Lock()

    async def wait(self):
        async with self._lock:
            with self as throttle:
                await asyncio.sleep(throttle)
