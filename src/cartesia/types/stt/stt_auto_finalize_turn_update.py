# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeTurnUpdate"]


class STTAutoFinalizeTurnUpdate(BaseModel):
    """Fires repeatedly as the model transcribes the current user turn."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    transcript: str
    """Cumulative text for the current turn, i.e.

    the full text transcribed so far in this turn, not a delta.
    """

    type: Literal["turn.update"]
    """Event type identifier."""
