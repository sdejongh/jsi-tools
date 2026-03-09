"""Decorator that logs function return values with type information."""

from __future__ import annotations

import functools
import inspect
import logging
from typing import TYPE_CHECKING, ParamSpec, TypeVar, overload

if TYPE_CHECKING:
    from collections.abc import Callable

__all__ = ["log_return"]

P = ParamSpec("P")
R = TypeVar("R")


def _format_type_info(value: object) -> str:
    """Format type information string for a value."""
    if value is None:
        return "None"

    type_name = type(value).__name__

    # Generators and coroutines — no len
    if inspect.isgenerator(value):
        return "generator"
    if inspect.isasyncgen(value):
        return "async_generator"
    if inspect.iscoroutine(value):
        return "coroutine"

    # Types that support len
    if isinstance(value, (str, bytes, bytearray, list, tuple, set, frozenset, dict)):
        return f"{type_name}[len={len(value)}]"

    # Other objects with __len__
    if hasattr(value, "__len__"):
        try:
            return f"{type_name}[len={len(value)}]"
        except TypeError:
            pass

    return type_name


def _format_return_log(
    func_name: str, value: object, max_length: int | None
) -> str:
    """Format the complete log message."""
    type_info = _format_type_info(value)
    value_repr = repr(value)
    if max_length is not None and len(value_repr) > max_length:
        value_repr = value_repr[:max_length] if max_length <= 3 else value_repr[: max_length - 3] + "..."
    return f"{func_name} returned {type_info}: {value_repr}"


@overload
def log_return(func: Callable[P, R], /) -> Callable[P, R]: ...


@overload
def log_return(
    *,
    level: int = logging.DEBUG,
    logger: logging.Logger | None = None,
    max_length: int | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def log_return(
    func: Callable[P, R] | None = None,
    /,
    *,
    level: int = logging.DEBUG,
    logger: logging.Logger | None = None,
    max_length: int | None = None,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """Log the return value of a decorated function.

    Can be used with or without parentheses::

        @log_return
        def my_func(): ...

        @log_return(level=logging.INFO)
        def my_func(): ...

    Args:
        level: Logging level (default ``logging.DEBUG``).
        logger: Logger instance to use. When ``None``, a logger derived from
            the decorated function's module is used.
        max_length: If set, truncate the ``repr`` of the return value to
            this length.
    """

    def decorator(fn: Callable[P, R]) -> Callable[P, R]:
        _logger = logger or logging.getLogger(fn.__module__)

        if inspect.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                result = await fn(*args, **kwargs)
                _logger.log(
                    level,
                    _format_return_log(fn.__qualname__, result, max_length),
                )
                return result  # type: ignore[no-any-return]

            return async_wrapper  # type: ignore[return-value]

        if inspect.isgeneratorfunction(fn):

            @functools.wraps(fn)
            def gen_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                gen = fn(*args, **kwargs)
                _logger.log(
                    level,
                    _format_return_log(fn.__qualname__, gen, max_length),
                )
                return gen  # type: ignore[return-value]

            return gen_wrapper

        @functools.wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = fn(*args, **kwargs)
            _logger.log(
                level,
                _format_return_log(fn.__qualname__, result, max_length),
            )
            return result

        return wrapper

    if func is not None:
        return decorator(func)

    return decorator
