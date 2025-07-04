# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import typing


class TranscriptionWord(UniversalBaseModel):
    word: str = pydantic.Field()
    """
    The transcribed word.
    """

    start: float = pydantic.Field()
    """
    Start time of the word in seconds.
    """

    end: float = pydantic.Field()
    """
    End time of the word in seconds.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
