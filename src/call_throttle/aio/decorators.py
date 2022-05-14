from asyncio import Lock
from functools import wraps

from .throttle import Throttle


def throttle(calls, period, raise_on_throttle=False):
    '''
    A throttle decorator factory used to limit asyncio coroutine calls during
    the defined time period.

    Args:
        calls (int): The maximum number of function calls within a time period
            before throttling.
        period (datetime.timedelta): A time period within which the throttling
            applies to function calls.
        raise_on_throttle (bool): A flag indicating whether to raise an
            exception when throttling.

    Usage:
        >>> import datetime
        >>> from call_throttle.aio import throttle
        >>> @throttle(calls=1, period=datetime.timedelata(seconds=1))
        >>> async def coro():
        ...     pass

    Raises:
        ThrottleException (when raise_on_throttle is True and throttle occurs)
    '''

    def decorator(coro):
        thr = Throttle(calls, period, raise_on_throttle)
        lock = Lock()

        @wraps(coro)
        async def wrapper(*args, **kwargs):

            async with lock:
                await thr.call()

            return await coro(*args, **kwargs)

        return wrapper

    return decorator
