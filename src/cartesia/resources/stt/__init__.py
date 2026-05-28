# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .stt import (
    STTResource,
    AsyncSTTResource,
    STTResourceWithRawResponse,
    AsyncSTTResourceWithRawResponse,
    STTResourceWithStreamingResponse,
    AsyncSTTResourceWithStreamingResponse,
)
from .auto_finalize import AutoFinalizeResource, AsyncAutoFinalizeResource
from .manual_finalize import ManualFinalizeResource, AsyncManualFinalizeResource

__all__ = [
    "AutoFinalizeResource",
    "AsyncAutoFinalizeResource",
    "ManualFinalizeResource",
    "AsyncManualFinalizeResource",
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
