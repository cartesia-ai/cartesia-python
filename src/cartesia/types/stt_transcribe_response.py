# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .stt_word import STTWord

__all__ = ["STTTranscribeResponse", "SttTranscribeResponse", "Word"]

Word = STTWord  # Alias for backward compatibility


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

    words: Optional[List[STTWord]] = None
    """Word-level timestamps showing the start and end time of each word.

    Only included when `[word]` is passed into `timestamp_granularities[]`.
    """


SttTranscribeResponse = STTTranscribeResponse  # Alias for backward compatibility
