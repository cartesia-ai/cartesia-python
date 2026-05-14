# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import base64
from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .word_timestamps import WordTimestamps
from .phoneme_timestamps import PhonemeTimestamps

__all__ = [
    "TTSSSEEvent",
    "TTSSSEChunkEvent",
    "TTSSSETimestampsEvent",
    "TTSSSEPhonemeTimestampsEvent",
    "TTSSSEDoneEvent",
    "TTSSSEErrorEvent",
]


class _TTSSSEEventBase(BaseModel):
    """Used for backward compatibility with v3.0.2"""

    id: None = None
    """Not used. Included for backward compatibility with v3.0.2"""

    retry: None = None
    """Not used. Included for backward compatibility with v3.0.2"""


class TTSSSEChunkEvent(_TTSSSEEventBase):
    """Audio data chunk."""

    data: str
    """Base64-encoded audio data."""

    done: Literal[False]
    """Whether this is the final event for the request.

    Always `false` for chunk events.
    """

    status_code: int
    """HTTP-style status code."""

    step_time: float
    """Server-side processing time for this chunk in milliseconds."""

    type: Literal["chunk"]
    """Event type identifier."""

    context_id: Optional[str] = None
    """The context ID echoed back from the request, if one was provided."""

    @property
    def audio(self) -> Optional[bytes]:
        """
        Decoded audio data as bytes.

        This property automatically base64-decodes the data field for convenience.
        Returns None if data is None or empty.
        """
        if not self.data:
            return None
        try:
            return base64.b64decode(self.data)
        except Exception:
            return None


class TTSSSETimestampsEvent(_TTSSSEEventBase):
    """Word-level timing information."""

    done: Literal[False]
    """Whether this is the final event for the request.

    Always `false` for timestamps events.
    """

    status_code: int
    """HTTP-style status code."""

    type: Literal["timestamps"]
    """Event type identifier."""

    word_timestamps: WordTimestamps
    """Word-level timing information."""

    context_id: Optional[str] = None
    """The context ID echoed back from the request, if one was provided."""

    @property
    def timestamps(self) -> Optional[WordTimestamps]:
        """Alias for word_timestamps for convenience"""
        return self.word_timestamps


class TTSSSEPhonemeTimestampsEvent(_TTSSSEEventBase):
    """Phoneme-level timing information."""

    done: Literal[False]
    """Whether this is the final event for the request.

    Always `false` for phoneme_timestamps events.
    """

    phoneme_timestamps: PhonemeTimestamps
    """Phoneme-level timing information."""

    status_code: int
    """HTTP-style status code."""

    type: Literal["phoneme_timestamps"]
    """Event type identifier."""

    context_id: Optional[str] = None
    """The context ID echoed back from the request, if one was provided."""

    @property
    def timestamps(self) -> Optional[PhonemeTimestamps]:
        """Alias for phoneme_timestamps for convenience"""
        return self.phoneme_timestamps


class TTSSSEDoneEvent(_TTSSSEEventBase):
    """Generation completion signal. Final event in the stream."""

    done: Literal[True]
    """Whether generation is complete. Always `true` for done events."""

    status_code: int
    """HTTP-style status code."""

    type: Literal["done"]
    """Event type identifier."""

    context_id: Optional[str] = None
    """The context ID echoed back from the request, if one was provided."""


class TTSSSEErrorEvent(_TTSSSEEventBase):
    """Error information for the TTS SSE request."""

    done: bool
    """Whether generation is complete."""

    message: str
    """Human-readable error message."""

    request_id: str
    """Unique identifier for this request."""

    status_code: int
    """An HTTP response status code."""

    title: str
    """Human-readable error title."""

    type: Literal["error"]
    """Event type identifier."""

    doc_url: Optional[str] = None
    """URL to relevant documentation."""

    error_code: Optional[str] = None
    """Machine-readable error code."""

    @property
    def error(self) -> str:
        """
        Human-readable error message.

        This property exists for backward compatibility
        since previous versions of the SDK incorrectly included it.
        """

        return f"{self.title}: {self.message}"


TTSSSEEvent: TypeAlias = Annotated[
    Union[TTSSSEChunkEvent, TTSSSETimestampsEvent, TTSSSEPhonemeTimestampsEvent, TTSSSEDoneEvent, TTSSSEErrorEvent],
    PropertyInfo(discriminator="type"),
]
