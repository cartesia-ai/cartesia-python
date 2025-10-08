# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from .agent_call import AgentCall

__all__ = ["CallListResponse"]


class CallListResponse(BaseModel):
    data: List[AgentCall]
    """The list of agent calls."""

    next_page: Optional[str] = None
    """The cursor for the next page of results."""
