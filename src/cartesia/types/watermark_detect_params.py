# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["WatermarkDetectParams"]


class WatermarkDetectParams(TypedDict, total=False):
    file: Required[FileTypes]
    """Audio file to check, between 5 seconds and 5 minutes long, up to 32 MiB.

    Supported formats are FLAC, M4A, MP3, MP4, MPEG, MPGA, OGA, OGG, WAV, and WebM.
    """
