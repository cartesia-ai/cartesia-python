# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .stt_turns_turn_end import STTTurnsTurnEnd
from ..stt_error_response import STTErrorResponse
from .stt_turns_connected import STTTurnsConnected
from .stt_turns_turn_start import STTTurnsTurnStart
from .stt_turns_turn_resume import STTTurnsTurnResume
from .stt_turns_turn_update import STTTurnsTurnUpdate
from .stt_turns_turn_eager_end import STTTurnsTurnEagerEnd

__all__ = ["STTTurnsWebsocketResponse"]

STTTurnsWebsocketResponse: TypeAlias = Annotated[
    Union[
        STTTurnsConnected,
        STTTurnsTurnStart,
        STTTurnsTurnUpdate,
        STTTurnsTurnEagerEnd,
        STTTurnsTurnResume,
        STTTurnsTurnEnd,
        STTErrorResponse,
    ],
    PropertyInfo(discriminator="type"),
]
