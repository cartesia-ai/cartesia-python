# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTExternalVADFlushDoneResponse"]


class STTExternalVADFlushDoneResponse(BaseModel):
    """
    Acknowledgment that buffered audio has been processed in response to a `finalize` command.
    """

    request_id: str
    """Unique identifier for this WebSocket connection."""

    type: Literal["flush_done"]
    """Event type identifier."""
