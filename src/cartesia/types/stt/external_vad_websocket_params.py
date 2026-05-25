# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..stt_encoding import STTEncoding
from .stt_realtime_external_vad_model import STTRealtimeExternalVADModel

__all__ = ["ExternalVADWebsocketParams"]


class ExternalVADWebsocketParams(TypedDict, total=False):
    encoding: Required[STTEncoding]
    """The encoding format for audio data sent to the STT WebSocket."""

    model: Required[STTRealtimeExternalVADModel]
    """
    Models that support realtime speech-to-text using in external
    voice-activity-detection mode. This mode expects you to send the `finalize`
    command to trigger transcription. See
    [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest) for
    all options.
    """

    sample_rate: Required[int]
    """Sample rate in Hz."""

    language: Literal["en"]
    """The language of the input audio in ISO-639-1 format.

    Defaults to `en`. See
    [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest) for
    current language support.
    """

    max_silence_duration_secs: float
    """Used by `ink-whisper` models only.

    Maximum duration of silence (in seconds) before the API automatically finalizes
    the transcript. Lower values finalize more aggressively; higher values allow
    longer pauses within utterances.
    """

    min_volume: float
    """Used by `ink-whisper` models only.

    Controls what is considered silence for automatic transcript finalization. Lower
    values pick up quiet audio; higher values filter noisy audio more aggressively.
    """
