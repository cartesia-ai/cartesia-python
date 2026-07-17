# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .stt_auto_finalize_config_command_param import STTAutoFinalizeConfigCommandParam

__all__ = ["STTAutoFinalizeWebsocketRequestParam", "STTAutoFinalizeCloseCommand"]


class STTAutoFinalizeCloseCommand(TypedDict, total=False):
    """Sent as a JSON-encoded WebSocket text frame to close the session cleanly.

    All buffered audio will be processed by the model into events before the connection closes.
    """

    type: Required[Literal["close"]]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to close the session.
    """


STTAutoFinalizeWebsocketRequestParam: TypeAlias = Union[STTAutoFinalizeCloseCommand, STTAutoFinalizeConfigCommandParam]
