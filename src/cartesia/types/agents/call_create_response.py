# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from ..._models import BaseModel

__all__ = ["CallCreateResponse", "Call"]


class Call(BaseModel):
    number: str
    """
    Destination phone number for this outbound call, in E.164 format (e.g.,
    `+14155559876`).
    """

    agent_call_id: Optional[str] = None
    """Agent call ID for tracking per-call information.

    This is absent when the request fails before Cartesia creates the call record.
    """

    error: Optional[Dict[str, object]] = None
    """Validation or dialing error for this destination.

    Other valid calls still proceed.
    """


class CallCreateResponse(BaseModel):
    calls: List[Call]
