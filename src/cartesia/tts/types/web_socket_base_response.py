# This file was auto-generated by Fern from our API Definition.

from ...core.pydantic_utilities import UniversalBaseModel
import typing
from .context_id import ContextId
from ...core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class WebSocketBaseResponse(UniversalBaseModel):
    context_id: typing.Optional[ContextId] = None
    status_code: int
    done: bool

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow", frozen=True)  # type: ignore # Pydantic v2
    else:

        class Config:
            frozen = True
            smart_union = True
            extra = pydantic.Extra.allow
