# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from ..._models import BaseModel

__all__ = ["CallLogsResponse"]


class CallLogsResponse(BaseModel):
    """The runtime logs associated with a specific agent call."""

    call_id: str
    """The ID of the call."""

    logs: List[str]
    """Runtime log lines recorded during the call."""

    updated_at: datetime
    """The date and time when the logs were last updated."""
