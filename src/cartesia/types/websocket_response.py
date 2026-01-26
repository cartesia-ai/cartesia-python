# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import base64
from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = ["WebsocketResponse", "Chunk", "FlushDone", "Done", "Timestamps", "Error", "PhonemeTimestamps"]


class Chunk(BaseModel):
    data: str
    """Base64-encoded audio data."""

    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["chunk"]] = None

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
    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["flush_done"]] = None


class Done(BaseModel):
    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["done"]] = None


class Timestamps(BaseModel):
    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["timestamps"]] = None


class Error(BaseModel):
    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["error"]] = None


class PhonemeTimestamps(BaseModel):
    done: bool

    status_code: int

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    type: Optional[Literal["phoneme_timestamps"]] = None


WebsocketResponse: TypeAlias = Annotated[
    Union[Chunk, FlushDone, Done, Timestamps, Error, PhonemeTimestamps], PropertyInfo(discriminator="type")
]
