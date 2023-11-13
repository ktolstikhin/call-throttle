import asyncio
from datetime import timedelta
from functools import wraps

from .throttle import Throttle, AsyncThrottle


def throttle(calls, period, raise_on_throttle=False):
    """A throttle decorator factory used to limit function or asyncio coroutine
    calls during the defined time period.

    Args:
        calls (int): The maximum number of function calls within a time period
            before throttling.
        period (int, float, datetime.timedelta): A time period within which the
            throttling applies to function calls. Seconds or timedelta.
        raise_on_throttle (bool): A flag indicating whether to raise an
            exception when throttling.

    Returns:
        A decorator suited for functions and asyncio coroutines.

    Raises:
        ThrottleException (when raise_on_throttle is True and throttle occurs)

    Usage:
        >>> from datetime import timedelta
        >>> from call_throttle import throttle
        >>>
        >>> @throttle(calls=1, period=timedelata(seconds=1))
        >>> def func():
        ...     pass
        >>>
        >>> @throttle(calls=10, period=timedelata(milliseconds=100))
        >>> async def coro():
        ...     pass
    """

    if isinstance(period, timedelta):
        period = period.total_seconds()

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            thr = AsyncThrottle(calls, period, raise_on_throttle)

            @wraps(func)
            async def wrapper(*args, **kwargs):
                await thr.wait()
                return await func(*args, **kwargs)

        else:
            thr = Throttle(calls, period, raise_on_throttle)

            @wraps(func)
            def wrapper(*args, **kwargs):
                thr.wait()
                return func(*args, **kwargs)

        return wrapper

    return decorator
