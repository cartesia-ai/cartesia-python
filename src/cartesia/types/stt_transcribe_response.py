# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["STTTranscribeResponse", "Word"]


class Word(BaseModel):
    end: float
    """End time of the word in seconds."""

    start: float
    """Start time of the word in seconds."""

    word: str
    """The transcribed word."""


class STTTranscribeResponse(BaseModel):
    text: str
    """The transcribed text."""

    type: Literal["transcript"]
    """The message type. Always `transcript` for a batch transcription response."""

    duration: Optional[float] = None
    """The duration of the input audio in seconds."""

    is_final: Optional[bool] = None
    """Not used for batch transcription."""

    language: Optional[str] = None
    """The specified language of the input audio."""

    request_id: Optional[str] = None
    """Unique identifier for this transcription request."""

    words: Optional[List[Word]] = None
    """Word-level timestamps showing the start and end time of each word.

    Only included when `[word]` is passed into `timestamp_granularities[]`.
    """
