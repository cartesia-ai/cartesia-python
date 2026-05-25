# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..shared.word_timestamps import WordTimestamps

__all__ = ["STTExternalVADTranscriptResponse"]


class STTExternalVADTranscriptResponse(BaseModel):
    """A transcript chunk."""

    is_final: bool
    """Whether `text` is finalized."""

    request_id: str
    """Unique identifier for this WebSocket connection."""

    text: str
    """Transcribed text.

    This is a delta from the last transcript chunk with `"is_final": true`. To
    assemble the full transcript, concatenate all transcript chunks where
    `"is_final": true`. Do not strip whitespace from `text` or add whitespace
    between chunks as this will produce an incorrect transcript.
    """

    type: Literal["transcript"]
    """Event type identifier."""

    duration: Optional[float] = None
    """Duration of the audio that produced this chunk, in seconds."""

    language: Optional[str] = None
    """Detected language of the audio in ISO-639-1 format."""

    words: Optional[List[WordTimestamps]] = None
    """Word-level timing information for the transcript."""
