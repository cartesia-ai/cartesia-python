# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..stt_error_response import STTErrorResponse
from .stt_auto_finalize_turn_end import STTAutoFinalizeTurnEnd
from .stt_auto_finalize_connected import STTAutoFinalizeConnected
from .stt_auto_finalize_turn_start import STTAutoFinalizeTurnStart
from .stt_auto_finalize_turn_resume import STTAutoFinalizeTurnResume
from .stt_auto_finalize_turn_update import STTAutoFinalizeTurnUpdate
from .stt_auto_finalize_turn_eager_end import STTAutoFinalizeTurnEagerEnd

__all__ = ["STTAutoFinalizeWebsocketResponse"]

STTAutoFinalizeWebsocketResponse: TypeAlias = Annotated[
    Union[
        STTAutoFinalizeConnected,
        STTAutoFinalizeTurnStart,
        STTAutoFinalizeTurnUpdate,
        STTAutoFinalizeTurnEagerEnd,
        STTAutoFinalizeTurnResume,
        STTAutoFinalizeTurnEnd,
        STTErrorResponse,
    ],
    PropertyInfo(discriminator="type"),
]
