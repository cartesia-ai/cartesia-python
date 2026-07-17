# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "STTAutoFinalizeWebsocketRequest",
    "STTAutoFinalizeCloseCommand",
    "STTAutoFinalizeConfigCommand",
    "STTAutoFinalizeConfigCommandTurn",
]


class STTAutoFinalizeCloseCommand(BaseModel):
    """Sent as a JSON-encoded WebSocket text frame to close the session cleanly.

    All buffered audio will be processed by the model into events before the connection closes.
    """

    type: Literal["close"]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to close the session.
    """


class STTAutoFinalizeConfigCommandTurn(BaseModel):
    """Turn detection settings."""

    eager_end_threshold: Optional[float] = None
    """Threshold below which to eager end the turn.

    Default: 0.4. Range: 0.3-0.6. Must stay between the end and start thresholds.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    end_threshold: Optional[float] = None
    """Threshold below which to end the turn.

    Default: 0.2. Range: 0.05-0.5. Must stay below the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    end_timeout_ms: Optional[float] = None
    """
    Maximum amount of time in milliseconds that the model will wait after the user
    stops speaking before ending the turn. Default: 5600. Range: 640-11200.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """

    start_threshold: Optional[float] = None
    """Threshold above which to start the turn.

    Default: 0.8. Range: 0.5-0.9. Must stay above the eager end threshold.

    See
    [Configuring turn detection](https://docs.cartesia.ai/use-the-api/stt/turns#configuring-turn-detection)
    for details.
    """


class STTAutoFinalizeConfigCommand(BaseModel):
    """
    Sent as a JSON-encoded WebSocket text frame to update model settings mid-session.
    """

    type: Literal["config"]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to update model settings.
    """

    turn: Optional[STTAutoFinalizeConfigCommandTurn] = None
    """Turn detection settings."""


STTAutoFinalizeWebsocketRequest: TypeAlias = Union[STTAutoFinalizeCloseCommand, STTAutoFinalizeConfigCommand]
