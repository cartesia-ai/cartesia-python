# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Union, Literal, TypeAlias

__all__ = ["TTSModel"]

_TTSModel = Literal[
    "sonic-3.5", "sonic-3", "sonic-3.5-2026-05-04", "sonic-3-2026-01-12", "sonic-3-2025-10-27", "sonic-latest"
]

TTSModel: TypeAlias = Union[_TTSModel, str]
