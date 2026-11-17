# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..stt_language_confidence import STTLanguageConfidence

__all__ = ["STTManualFinalizeFlushDoneResponse"]


class STTManualFinalizeFlushDoneResponse(BaseModel):
    """
    Acknowledgment that buffered audio has been processed in response to a `finalize` command.
    """

    request_id: str
    """Unique identifier for this WebSocket connection."""

    type: Literal["flush_done"]
    """Event type identifier."""

    languages: Optional[List[STTLanguageConfidence]] = None
    """Languages detected in the audio since the previous `finalize`"""
