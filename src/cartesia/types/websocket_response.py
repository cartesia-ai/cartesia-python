# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import base64
from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from . import phoneme_timestamps as _phoneme_timestamps
from .._utils import PropertyInfo
from .._models import BaseModel
from .word_timestamps import WordTimestamps

__all__ = [
    "WebsocketResponse",
    "Chunk",
    "FlushDone",
    "Done",
    "Timestamps",
    "Error",
    "PhonemeTimestamps",
    "TimestampsWordTimestamps",
    "PhonemeTimestampsPhonemeTimestamps",
]


class Chunk(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    data: str
    """Base64-encoded audio data"""

    done: bool
    """Whether this is the final chunk for this context"""

    status_code: int
    """HTTP-style status code"""

    step_time: float
    """Server-side processing time for this chunk in milliseconds"""

    type: Literal["chunk"]

    flush_id: Optional[int] = None
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    @property
    def audio(self) -> Optional[bytes]:
        """
        Decoded audio data as bytes.

        This property automatically base64-decodes the data field for convenience.
        Returns None if data is None or empty.
        """
        if not self.data:
            return None
        return base64.b64decode(self.data)


class FlushDone(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool
    """Whether generation is complete"""

    flush_done: bool
    """Whether the flush is complete"""

    flush_id: int
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    status_code: int
    """HTTP-style status code"""

    type: Literal["flush_done"]


class Done(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: Literal[True]
    """Whether generation is complete. Always `true` for done events."""

    status_code: int
    """HTTP-style status code"""

    type: Literal["done"]


class Timestamps(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool
    """Whether generation is complete"""

    status_code: int
    """HTTP-style status code"""

    type: Literal["timestamps"]

    flush_id: Optional[int] = None
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    word_timestamps: Optional[WordTimestamps] = None
    """Word-level timing information."""


class Error(BaseModel):
    done: bool
    """Whether generation is complete"""

    type: Literal["error"]

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    doc_url: Optional[str] = None
    """URL to relevant documentation"""

    error_code: Optional[str] = None
    """Machine-readable error code."""

    message: Optional[str] = None
    """Human-readable error message."""

    request_id: Optional[str] = None
    """A unique identifier for the network connection."""

    status_code: Optional[int] = None
    """An HTTP response status code."""

    title: Optional[str] = None
    """Human-readable error title."""


class PhonemeTimestamps(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool
    """Whether generation is complete"""

    status_code: int
    """HTTP-style status code"""

    type: Literal["phoneme_timestamps"]

    flush_id: Optional[int] = None
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    phoneme_timestamps: Optional[_phoneme_timestamps.PhonemeTimestamps] = None
    """Phoneme-level timing information."""


WebsocketResponse: TypeAlias = Annotated[
    Union[Chunk, FlushDone, Done, Timestamps, Error, PhonemeTimestamps], PropertyInfo(discriminator="type")
]

# Alias for backward compatibility
TimestampsWordTimestamps = WordTimestamps

# Alias for backward compatibility
PhonemeTimestampsPhonemeTimestamps = PhonemeTimestamps
