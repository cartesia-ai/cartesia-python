# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeWebsocketRequest"]


class STTAutoFinalizeWebsocketRequest(BaseModel):
    """Sent as a JSON-encoded WebSocket text frame to close the session cleanly.

    All buffered audio will be processed by the model into events before the connection closes.
    """

    type: Literal["close"]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to close the session.
    """
