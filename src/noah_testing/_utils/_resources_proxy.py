from __future__ import annotations

from typing import Any
from typing_extensions import override

from ._proxy import LazyProxy


class ResourcesProxy(LazyProxy[Any]):
    """A proxy for the `noah_testing.resources` module.

    This is used so that we can lazily import `noah_testing.resources` only when
    needed *and* so that users can just import `noah_testing` and reference `noah_testing.resources`
    """

    @override
    def __load__(self) -> Any:
        import importlib

        mod = importlib.import_module("noah_testing.resources")
        return mod


resources = ResourcesProxy().__as_proxied__()
