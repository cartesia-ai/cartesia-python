# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel

__all__ = ["VoiceChangerSSEEvent", "VoiceChangerSSEChunk", "VoiceChangerSSEDone", "VoiceChangerSSEError"]


class VoiceChangerSSEChunk(BaseModel):
    """Audio data chunk."""

    data: str
    """Base64-encoded audio data."""

    done: Literal[False]
    """Whether this is the final event for the request.

    Always `false` for chunk events.
    """

    sample_rate: int
    """The sample rate of the audio in Hz."""

    status_code: Literal[206]
    """HTTP-style status code. Always `206` for chunk events."""

    step_time: float
    """Server-side processing time for this chunk in milliseconds."""


class VoiceChangerSSEDone(BaseModel):
    """Generation completion signal. Final event in the stream."""

    done: Literal[True]
    """Whether generation is complete. Always `true` for done events."""

    status_code: Literal[200]
    """HTTP-style status code. Always `200` for done events."""


class VoiceChangerSSEError(BaseModel):
    """Error information for the Voice Changer SSE request."""

    done: Literal[True]
    """Whether generation is complete. Always `true` for error events."""

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


VoiceChangerSSEEvent: TypeAlias = Union[VoiceChangerSSEChunk, VoiceChangerSSEDone, VoiceChangerSSEError]
