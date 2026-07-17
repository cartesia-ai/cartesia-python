# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["STTErrorResponse"]


class STTErrorResponse(BaseModel):
    """Error information for STT WebSocket connections."""

    message: str
    """Human-readable error message."""

    status_code: int
    """An HTTP response status code."""

    title: str
    """Human-readable error title."""

    type: Literal["error"]
    """Event type identifier."""

    doc_url: Optional[str] = None
    """URL to relevant documentation."""

    error_code: Optional[str] = None
    """Machine-readable error code."""

    request_id: Optional[str] = None
    """Unique identifier for this WebSocket connection."""
