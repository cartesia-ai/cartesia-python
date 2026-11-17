# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from ..stt_encoding import STTEncoding
from ..stt_language_param import STTLanguageParam
from .stt_manual_finalize_model import STTManualFinalizeModel

__all__ = ["ManualFinalizeWebsocketParams"]


class ManualFinalizeWebsocketParams(TypedDict, total=False):
    encoding: Required[STTEncoding]
    """The encoding format for audio data sent to the STT WebSocket."""

    model: Required[STTManualFinalizeModel]
    """
    Models that support realtime speech-to-text (manual finalize). This mode expects
    you to send the `finalize` command to trigger transcription. See
    [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest) for
    all options.
    """

    sample_rate: Required[int]
    """Sample rate in Hz."""

    keyterm: SequenceNotStr[str]
    """Key terms to improve the recall of specific words and phrases.

    Pass multiple values to boost multiple terms. To boost one multi-word phrase,
    join the words with a space. Accepts up to 500 keyterms totaling 5000
    characters.

    See [Keyterm prompting](https://docs.cartesia.ai/use-the-api/stt/keyterms) for
    details.
    """

    language: Literal["en"]
    """The language of the input audio in ISO-639-1 format.

    Defaults to `en`. See
    [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest) for
    current language support.
    """

    language_hint: List[STTLanguageParam]
    """Languages expected in the audio, up to 6 at a time.

    Transcription accuracy improves when language hints match the audio. Hinting
    more languages reduces efficacy.
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
