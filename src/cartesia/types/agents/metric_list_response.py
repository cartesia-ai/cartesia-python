# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .metric import Metric
from ..._models import BaseModel

__all__ = ["MetricListResponse"]


class MetricListResponse(BaseModel):
    data: List[Metric]
    """List of metrics."""

    has_more: bool
    """Whether there are more pages of metrics."""

    next_page: Optional[str] = None
    """
    An ID that can be passed as `starting_after` or `ending_before` to get the next
    page of metrics. Used by the next page function.
    """
