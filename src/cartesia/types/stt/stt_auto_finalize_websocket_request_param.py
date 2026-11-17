# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from ..stt_language_param import STTLanguageParam

__all__ = [
    "STTAutoFinalizeWebsocketRequestParam",
    "STTAutoFinalizeCloseCommand",
    "STTAutoFinalizeConfigCommand",
    "STTAutoFinalizeConfigCommandTurn",
]


class STTAutoFinalizeCloseCommand(TypedDict, total=False):
    """Sent as a JSON-encoded WebSocket text frame to close the session cleanly.

    All buffered audio will be processed by the model into events before the connection closes.
    """

    type: Required[Literal["close"]]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to close the session.
    """


class STTAutoFinalizeConfigCommandTurn(TypedDict, total=False):
    """Turn detection settings."""

    eager_end_threshold: float
    """Threshold below which to eager end the turn.

    Default: 0.4. Range: 0.3-0.6. Must stay between the end and start thresholds.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    end_threshold: float
    """Threshold below which to end the turn.

    Default: 0.2. Range: 0.05-0.5. Must stay below the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    end_timeout_ms: float
    """
    Maximum amount of time in milliseconds that the model will wait after the user
    stops speaking before ending the turn. Default: 5600. Range: 640-11200.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    start_threshold: float
    """Threshold above which to start the turn.

    Default: 0.8. Range: 0.5-0.9. Must stay above the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """


class STTAutoFinalizeConfigCommand(TypedDict, total=False):
    """
    Sent as a JSON-encoded WebSocket text frame to update model settings mid-session.
    """

    type: Required[Literal["config"]]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to update model settings.
    """

    keyterms: SequenceNotStr[str]
    """Replaces the session's keyterms.

    Pass an empty list to clear them; omit the field to keep them. Accepts up to 500
    keyterms totaling 5000 characters.

    See [Keyterm prompting](https://docs.cartesia.ai/use-the-api/stt/keyterms) for
    details.
    """

    language_hints: List[STTLanguageParam]
    """Replaces the session's language hints.

    Pass an empty list to clear them; omit the field to keep them. Accepts up to 6
    hints.

    Transcription accuracy improves when language hints match the audio. Hinting
    more languages reduces efficacy.
    """

    turn: STTAutoFinalizeConfigCommandTurn
    """Turn detection settings."""


STTAutoFinalizeWebsocketRequestParam: TypeAlias = Union[STTAutoFinalizeCloseCommand, STTAutoFinalizeConfigCommand]
