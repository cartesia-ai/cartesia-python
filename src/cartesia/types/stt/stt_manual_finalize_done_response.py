# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from ..stt_language_confidence import STTLanguageConfidence

__all__ = ["STTManualFinalizeDoneResponse"]


class STTManualFinalizeDoneResponse(BaseModel):
    """
    Acknowledgment for the `close` command, sent after all buffered audio has been processed and before the connection closes.
    """

    request_id: str
    """Unique identifier for this WebSocket connection."""

    type: Literal["done"]
    """Event type identifier."""

    languages: Optional[List[STTLanguageConfidence]] = None
    """Languages detected in the audio since the last `finalize`"""
