# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..stt_encoding import STTEncoding
from .stt_auto_finalize_model import STTAutoFinalizeModel

__all__ = ["AutoFinalizeWebsocketParams"]


class AutoFinalizeWebsocketParams(TypedDict, total=False):
    encoding: Required[STTEncoding]
    """The encoding format for audio data sent to the STT WebSocket."""

    model: Required[STTAutoFinalizeModel]
    """
    Models that support realtime speech-to-text (auto finalize). This mode detects
    when the user is speaking and emits turn events. See
    [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest) for
    all options.
    """

    sample_rate: Required[int]
    """Sample rate in Hz."""
