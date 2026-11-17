# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr
from ..stt_encoding import STTEncoding
from ..stt_language_param import STTLanguageParam
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

    keyterm: SequenceNotStr[str]
    """Key terms to improve the recall of specific words and phrases.

    Pass multiple values to boost multiple terms. To boost one multi-word phrase,
    join the words with a space. Accepts up to 500 keyterms totaling 5000
    characters.

    Replace keyterms mid-session with a `config` message.

    See [Keyterm prompting](https://docs.cartesia.ai/use-the-api/stt/keyterms) for
    details.
    """

    language_hint: List[STTLanguageParam]
    """Languages expected in the audio, up to 6 at a time.

    Transcription accuracy improves when language hints match the audio. Hinting
    more languages reduces efficacy.

    Replace language hints mid-session with a `config` message.
    """

    turn_eager_end_threshold: float
    """Threshold below which to eager end the turn.

    Default: 0.4. Range: 0.3-0.6. Must stay between the end and start thresholds.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    turn_end_threshold: float
    """Threshold below which to end the turn.

    Default: 0.2. Range: 0.05-0.5. Must stay below the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    turn_end_timeout_ms: float
    """
    Maximum amount of time in milliseconds that the model will wait after the user
    stops speaking before ending the turn. Default: 5600. Range: 640-11200.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    turn_start_threshold: float
    """Threshold above which to start the turn.

    Default: 0.8. Range: 0.5-0.9. Must stay above the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """
