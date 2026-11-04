# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ModelListParams"]


class ModelListParams(TypedDict, total=False):
    capability: Literal["tts", "stt"]
    """Filter to `tts` or `stt`. Omit to return both."""
