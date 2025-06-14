# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class DoneMessage(UniversalBaseModel):
    """
    Acknowledgment message sent in response to a `done` command, indicating that the session is complete and the WebSocket will close.
    """

    request_id: str = pydantic.Field()
    """
    Unique identifier for this transcription session.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
