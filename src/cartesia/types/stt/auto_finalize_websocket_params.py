# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr
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

    keyterm: SequenceNotStr[str]
    """Key terms to improve the recall of specific words and phrases.

    Pass multiple values to boost multiple terms, up to 100 keyterms totaling 1200
    characters. To boost one multi-word phrase, join the words with a space.

    See [Keyterm prompting](https://docs.cartesia.ai/use-the-api/stt/keyterms) for
    details.
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
