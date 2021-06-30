import asyncio
import functools
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class Runner:
    _event_loop: asyncio.AbstractEventLoop

    def __init__(self, event_loop: asyncio.AbstractEventLoop) -> None:
        self._event_loop = event_loop

    async def __call__(self, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        # loop.run_in_executor doesn't accept 'kwargs', so bind them in here
        func = functools.partial(func, **kwargs)
        return await self._event_loop.run_in_executor(None, func, *args)
