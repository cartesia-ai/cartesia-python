# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ToolListResponse"]


class ToolListResponse(BaseModel):
    data: List["Tool"]
    """The requested page of results."""

    has_more: bool
    """Whether more results are available after this page."""

    next_page: Optional[str] = None
    """
    An ID that can be passed as `starting_after` or `ending_before` to get the next
    page of data.
    """


from .tool import Tool
