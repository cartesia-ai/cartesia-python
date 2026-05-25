# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..stt_error_response import STTErrorResponse
from .stt_external_vad_done_response import STTExternalVADDoneResponse
from .stt_external_vad_flush_done_response import STTExternalVADFlushDoneResponse
from .stt_external_vad_transcript_response import STTExternalVADTranscriptResponse

__all__ = ["STTExternalVADWebsocketResponse"]

STTExternalVADWebsocketResponse: TypeAlias = Annotated[
    Union[
        STTExternalVADTranscriptResponse, STTExternalVADFlushDoneResponse, STTExternalVADDoneResponse, STTErrorResponse
    ],
    PropertyInfo(discriminator="type"),
]
