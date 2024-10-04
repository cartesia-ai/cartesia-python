import os
import warnings
from typing import Any, Callable, TypeVar

TCallable = TypeVar("TCallable", bound=Callable[..., Any])

# List of statistics of deprecated functions.
# This should only be used by the test suite to find any deprecated functions
# that should be removed for this version.
_TRACK_DEPRECATED_FUNCTION_STATS = os.environ.get("CARTESIA_TEST_DEPRECATED", "").lower() == "true"
_DEPRECATED_FUNCTION_STATS = []


def deprecated(
    reason=None, vdeprecated=None, vremove=None, replacement=None
) -> Callable[[TCallable], TCallable]:
    local_vars = locals()

    def fn(func: TCallable) -> TCallable:
        if isinstance(func, classmethod):
            func = func.__func__
        msg = _get_deprecated_msg(func, reason, vdeprecated, vremove, replacement)
        warnings.warn(msg, DeprecationWarning)
        return func

    if _TRACK_DEPRECATED_FUNCTION_STATS:  # pragma: no cover
        _DEPRECATED_FUNCTION_STATS.append(local_vars)

    return fn


def _get_deprecated_msg(wrapped, reason, vdeprecated, vremoved, replacement=None):
    fmt = "{name} is deprecated"
    if vdeprecated:
        fmt += " since v{vdeprecated}"
    if vremoved:
        fmt += " and will be removed in v{vremoved}"
    fmt += "."

    if reason:
        fmt += " ({reason})"
    if replacement:
        fmt += " -- Use {replacement} instead."

    return fmt.format(
        name=wrapped.__name__,
        reason=reason or "",
        vdeprecated=vdeprecated or "",
        vremoved=vremoved or "",
        replacement=replacement or "",
    )


# This method is taken from the following source:
# https://github.com/ad12/meddlr/blob/main/meddlr/utils/deprecated.py
