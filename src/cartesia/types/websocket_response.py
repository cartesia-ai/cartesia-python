# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import base64
from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "WebsocketResponse",
    "Chunk",
    "FlushDone",
    "Done",
    "Timestamps",
    "TimestampsWordTimestamps",
    "Error",
    "PhonemeTimestamps",
    "PhonemeTimestampsPhonemeTimestamps",
]


class Chunk(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    data: str
    """Base64-encoded audio data."""

    done: bool

    status_code: int

    step_time: float

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

    flush_done: bool

    flush_id: int
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    status_code: int

    type: Literal["flush_done"]


class Done(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool

    status_code: int

    type: Literal["done"]


class TimestampsWordTimestamps(BaseModel):
    end: List[float]

    start: List[float]

    words: List[str]


class Timestamps(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool

    status_code: int

    type: Literal["timestamps"]

    flush_id: Optional[int] = None
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    word_timestamps: Optional[TimestampsWordTimestamps] = None


class Error(BaseModel):
    done: bool

    type: Literal["error"]

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    doc_url: Optional[str] = None

    error_code: Optional[str] = None

    message: Optional[str] = None

    request_id: Optional[str] = None
    """A unique identifier for the network connection."""

    status_code: Optional[int] = None

    title: Optional[str] = None


class PhonemeTimestampsPhonemeTimestamps(BaseModel):
    end: List[float]

    phonemes: List[str]

    start: List[float]


class PhonemeTimestamps(BaseModel):
    context_id: str
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.
    """

    done: bool

    status_code: int

    type: Literal["phoneme_timestamps"]

    flush_id: Optional[int] = None
    """
    An identifier corresponding to the number of flush commands that have been sent
    for this context. Starts at 1.

    This can be used to map chunks of audio to certain transcript submissions.
    """

    phoneme_timestamps: Optional[PhonemeTimestampsPhonemeTimestamps] = None


WebsocketResponse: TypeAlias = Annotated[
    Union[Chunk, FlushDone, Done, Timestamps, Error, PhonemeTimestamps], PropertyInfo(discriminator="type")
]
