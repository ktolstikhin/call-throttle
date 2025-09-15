import asyncio
from datetime import timedelta
from functools import wraps
from typing import Any, Callable, TypeVar, Coroutine

from .throttle import Throttle, AsyncThrottle


T = TypeVar('T')


def throttle(calls: int, period: int | float | timedelta, raise_on_throttle: bool = False) -> Callable:
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
        >>> @throttle(calls=10, period=0.1)
        >>> async def coro():
        ...     pass
    """
    if isinstance(period, timedelta):
        period = period.total_seconds()

    def decorator(func: Callable[..., T]) -> Callable[..., T | Coroutine]:
        if asyncio.iscoroutinefunction(func):
            thr = AsyncThrottle(calls, period, raise_on_throttle)

            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Coroutine:
                await thr.wait()
                return await func(*args, **kwargs)

            return async_wrapper

        thr = Throttle(calls, period, raise_on_throttle)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            thr.wait()
            return func(*args, **kwargs)

        return wrapper

    return decorator
