# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["STTErrorResponse"]


class STTErrorResponse(BaseModel):
    """Error information for STT WebSocket connections."""

    type: Literal["error"]
    """Event type identifier."""

    doc_url: Optional[str] = None
    """URL to relevant documentation."""

    error_code: Optional[str] = None
    """Machine-readable error code."""

    message: Optional[str] = None
    """Human-readable error message."""

    request_id: Optional[str] = None
    """Unique identifier for this WebSocket connection."""

    status_code: Optional[int] = None
    """An HTTP response status code."""

    title: Optional[str] = None
    """Human-readable error title."""
