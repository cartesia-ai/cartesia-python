# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..stt_word import STTWord

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

    turn_id: Optional[str] = None
    """Identifies the turn this event belongs to.

    Unique within this connection and the same on every event in the turn.
    """

    words: Optional[List[STTWord]] = None
    """Words transcribed so far in this turn, with timings.

    Cumulative like `transcript`.
    """
