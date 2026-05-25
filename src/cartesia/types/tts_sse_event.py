# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel
from .shared.word_timestamps import WordTimestamps
from .shared.phoneme_timestamps import PhonemeTimestamps

__all__ = [
    "TTSSSEEvent",
    "TTSSSEChunkEvent",
    "TTSSSETimestampsEvent",
    "TTSSSEPhonemeTimestampsEvent",
    "TTSSSEDoneEvent",
    "TTSSSEErrorEvent",
]


class TTSSSEChunkEvent(BaseModel):
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


class TTSSSETimestampsEvent(BaseModel):
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


class TTSSSEPhonemeTimestampsEvent(BaseModel):
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


class TTSSSEDoneEvent(BaseModel):
    """Generation completion signal. Final event in the stream."""

    done: Literal[True]
    """Whether generation is complete. Always `true` for done events."""

    status_code: int
    """HTTP-style status code."""

    type: Literal["done"]
    """Event type identifier."""

    context_id: Optional[str] = None
    """The context ID echoed back from the request, if one was provided."""


class TTSSSEErrorEvent(BaseModel):
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


TTSSSEEvent: TypeAlias = Annotated[
    Union[TTSSSEChunkEvent, TTSSSETimestampsEvent, TTSSSEPhonemeTimestampsEvent, TTSSSEDoneEvent, TTSSSEErrorEvent],
    PropertyInfo(discriminator="type"),
]
