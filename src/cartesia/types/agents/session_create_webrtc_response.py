# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["SessionCreateWebrtcResponse"]


class SessionCreateWebrtcResponse(BaseModel):
    token: str
    """Short-lived LiveKit participant token for the browser connection.

    Do not log it.
    """

    call_id: str
    """ID of the pre-created call."""

    expires_at: datetime
    """Connection deadline.

    Create a new session if the browser does not join before this time.
    """

    room: str
    """LiveKit room the browser joins."""

    url: str
    """LiveKit server URL the browser connects to."""
