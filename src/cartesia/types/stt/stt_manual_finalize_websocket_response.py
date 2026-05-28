# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..stt_error_response import STTErrorResponse
from .stt_manual_finalize_done_response import STTManualFinalizeDoneResponse
from .stt_manual_finalize_flush_done_response import STTManualFinalizeFlushDoneResponse
from .stt_manual_finalize_transcript_response import STTManualFinalizeTranscriptResponse

__all__ = ["STTManualFinalizeWebsocketResponse"]

STTManualFinalizeWebsocketResponse: TypeAlias = Annotated[
    Union[
        STTManualFinalizeTranscriptResponse,
        STTManualFinalizeFlushDoneResponse,
        STTManualFinalizeDoneResponse,
        STTErrorResponse,
    ],
    PropertyInfo(discriminator="type"),
]
