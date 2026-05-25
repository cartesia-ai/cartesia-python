# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .stt import (
    STTResource,
    AsyncSTTResource,
    STTResourceWithRawResponse,
    AsyncSTTResourceWithRawResponse,
    STTResourceWithStreamingResponse,
    AsyncSTTResourceWithStreamingResponse,
)
from .external_vad import ExternalVADResource, AsyncExternalVADResource
from .turn_detecting import TurnDetectingResource, AsyncTurnDetectingResource

__all__ = [
    "TurnDetectingResource",
    "AsyncTurnDetectingResource",
    "ExternalVADResource",
    "AsyncExternalVADResource",
    "STTResource",
    "AsyncSTTResource",
    "STTResourceWithRawResponse",
    "AsyncSTTResourceWithRawResponse",
    "STTResourceWithStreamingResponse",
    "AsyncSTTResourceWithStreamingResponse",
    "SttResource",
    "AsyncSttResource",
    "SttResourceWithRawResponse",
    "AsyncSttResourceWithRawResponse",
    "SttResourceWithStreamingResponse",
    "AsyncSttResourceWithStreamingResponse",
]

# Aliases for backward compatibility
SttResource = STTResource
AsyncSttResource = AsyncSTTResource
SttResourceWithRawResponse = STTResourceWithRawResponse
AsyncSttResourceWithRawResponse = AsyncSTTResourceWithRawResponse
SttResourceWithStreamingResponse = STTResourceWithStreamingResponse
AsyncSttResourceWithStreamingResponse = AsyncSTTResourceWithStreamingResponse
