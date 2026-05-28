# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeConnected"]


class STTAutoFinalizeConnected(BaseModel):
    """Fires once when the WebSocket connection is established.

    You do not need to wait for this event before sending audio.
    """

    request_id: str
    """Unique identifier for this connection."""

    type: Literal["connected"]
    """Event type identifier."""
