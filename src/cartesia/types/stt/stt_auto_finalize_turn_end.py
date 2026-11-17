# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..stt_word import STTWord
from ..stt_language_confidence import STTLanguageConfidence

__all__ = ["STTAutoFinalizeTurnEnd"]


class STTAutoFinalizeTurnEnd(BaseModel):
    """Marks the end of a user turn."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    transcript: str
    """Definitive transcript for the completed turn."""

    type: Literal["turn.end"]
    """Event type identifier."""

    languages: Optional[List[STTLanguageConfidence]] = None
    """Languages detected in the completed turn"""

    turn_id: Optional[str] = None
    """Identifies the turn this event belongs to.

    Unique within this connection and the same on every event in the turn.
    """

    words: Optional[List[STTWord]] = None
    """Words in the completed turn, with timings"""
