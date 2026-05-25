# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["MP3OutputFormatParam"]


class MP3OutputFormatParam(TypedDict, total=False):
    bit_rate: Required[Literal[32000, 64000, 96000, 128000, 192000]]

    container: Required[Literal["mp3"]]

    sample_rate: Required[Literal[8000, 16000, 22050, 24000, 44100, 48000]]
