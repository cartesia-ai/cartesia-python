# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .metric import Metric
from ..._models import BaseModel

__all__ = ["MetricListResponse"]


class MetricListResponse(BaseModel):
    data: List[Metric]
    """List of metrics."""

    has_more: bool
    """
    Whether there are more metrics to fetch (using `starting_after=id`, where id is
    the ID of the last Metric in the current response).
    """

    next_page: Optional[str] = None
    """
    Use the last ID from `data` instead. An ID that can be passed as
    `starting_after` to get the next page of metrics.
    """
