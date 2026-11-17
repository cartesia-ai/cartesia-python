# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from ..._models import BaseModel

__all__ = ["SessionCreateWebsocketResponse"]


class SessionCreateWebsocketResponse(BaseModel):
    token: str
    """Opaque, short-lived, single-use session token. Do not inspect or log it."""

    call_id: str
    """ID of the pre-created call. The `session_ready` event returns the same value."""

    expires_at: datetime
    """Connection deadline, currently four minutes after creation.

    Use this timestamp rather than calculating the deadline.
    """

    url: str
    """WebSocket URL for this agent.

    Append the returned session token as the `access_token` query parameter.
    """
