# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["ToolListParams"]


class ToolListParams(TypedDict, total=False):
    agent_id: str
    """Return only tools used by this agent."""

    ending_before: str
    """A cursor for pagination.

    Pass the ID of the first item from the previous page to fetch the previous page.
    """

    expand: List[Literal["agents"]]
    """Related resources to include in each tool.

    `agents` lists the agents that use it.
    """

    limit: int
    """The maximum number of items to return, ranging between 1 and 100."""

    starting_after: str
    """A cursor for pagination.

    Pass the ID of the last item from the previous page to fetch the next page.
    """

    type: Literal["webhook", "client"]
    """Return only tools of this type."""
