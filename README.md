# call-throttle

![python](https://img.shields.io/pypi/pyversions/call-throttle.svg)
![version](https://img.shields.io/pypi/v/call-throttle.svg)
![downloads](https://img.shields.io/pypi/dm/call-throttle.svg)
![format](https://img.shields.io/pypi/format/call-throttle.svg)

This package provides decorators which can be used to throttle calls of regular Python functions and asyncio coroutines.

## Install

Use [pip](https://pip.pypa.io/en/stable/) package installer for Python:
```bash
python -m pip install --upgrade call-throttle
```
Make sure you have Python 3.9 or later installed.

## Usage

Here is a basic example for how to use the `throttle` decorator with functions and coroutines:
```python
import time
import asyncio
from datetime import timedelta

from call_throttle import throttle


@throttle(calls=1, period=timedelta(seconds=2))
def func():
    time.sleep(1)


@throttle(calls=2, period=0.2)
async def coro():
    await asyncio.sleep(0.05)
```
If passing `raise_on_throttle=True` to `@throttle(...)`, then a `call_throttle.ThrottleException` is raised when a decorated function or coroutine is called more times than the defined `calls` limit within the specified time `period`.

## License

This is a free software licensed under the terms of the MIT License.
