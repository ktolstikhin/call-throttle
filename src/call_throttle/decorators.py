from functools import wraps
from threading import RLock

from .throttle import Throttle


def throttle(calls, period, raise_on_throttle=False):
    '''
    A throttle decorator factory used to limit function calls during the
    defined time period.

    Args:
        calls (int): The maximum number of function calls within a time period
            before throttling.
        period (datetime.timedelta): A time period within which the throttling
            applies to function calls.
        raise_on_throttle (bool): A flag indicating whether to raise an
            exception when throttling.

    Usage:
        >>> import datetime
        >>> from call_throttle import throttle
        >>> @throttle(calls=1, period=datetime.timedelata(seconds=1))
        >>> def func():
        ...     pass

    Raises:
        ThrottleException (when raise_on_throttle is True and throttle occurs)
    '''

    def decorator(func):
        thr = Throttle(calls, period, raise_on_throttle)
        lock = RLock()

        @wraps(func)
        def wrapper(*args, **kwargs):

            with lock:
                thr.call()

            return func(*args, **kwargs)

        return wrapper

    return decorator
