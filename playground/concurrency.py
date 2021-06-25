import asyncio
import functools
from typing import Any, Callable, TypeVar

T = TypeVar("T")


async def run_in_threadpool(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = asyncio.get_event_loop()
    # loop.run_in_executor doesn't accept 'kwargs', so bind them in here
    func = functools.partial(func, **kwargs)
    return await loop.run_in_executor(None, func, *args)
