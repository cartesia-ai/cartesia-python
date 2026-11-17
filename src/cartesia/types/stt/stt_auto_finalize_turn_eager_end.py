# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..stt_word import STTWord
from ..stt_language_confidence import STTLanguageConfidence

__all__ = ["STTAutoFinalizeTurnEagerEnd"]


class STTAutoFinalizeTurnEagerEnd(BaseModel):
    """[PREVIEW] Fires when the model predicts that the user might be done speaking."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    transcript: str
    """Cumulative text for the current turn."""

    type: Literal["turn.eager_end"]
    """Event type identifier."""

    languages: Optional[List[STTLanguageConfidence]] = None
    """Languages detected in this turn so far"""

    turn_id: Optional[str] = None
    """Identifies the turn this event belongs to.

    Unique within this connection and the same on every event in the turn.
    """

    words: Optional[List[STTWord]] = None
    """Words transcribed so far in this turn, with timings"""
