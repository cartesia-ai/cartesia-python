# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["BatchListParams"]


class BatchListParams(TypedDict, total=False):
    agent_id: Optional[str]
    """Filter to batches for this agent."""

    ending_before: Optional[str]
    """(Pagination option) The ID of the batch to end before."""

    limit: Optional[int]
    """
    (Pagination option) The number of batches to return per page, ranging between 1
    and 100.
    """

    starting_after: Optional[str]
    """(Pagination option) The ID of the batch to start after."""
