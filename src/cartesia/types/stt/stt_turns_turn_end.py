# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTTurnsTurnEnd"]


class STTTurnsTurnEnd(BaseModel):
    """Marks the end of a user turn."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    transcript: str
    """Definitive transcript for the completed turn."""

    type: Literal["turn.end"]
    """Event type identifier."""
