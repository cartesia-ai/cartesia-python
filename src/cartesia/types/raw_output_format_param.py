# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .raw_encoding import RawEncoding

__all__ = ["RawOutputFormatParam"]


class RawOutputFormatParam(TypedDict, total=False):
    encoding: Required[RawEncoding]

    sample_rate: Required[int]
