# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime

from ..._models import BaseModel

__all__ = ["AgentRetrieveResponse", "Data"]


class Data(BaseModel):
    """A single bucket of agent usage within a time window."""

    calls: int
    """Number of agent calls that started within the bucket."""

    cents: int
    """Total cost in US cents accrued within the bucket."""

    end_ts: datetime
    """RFC 3339 timestamp for the end of the usage bucket."""

    minutes: float
    """Total minutes of agent runtime within the bucket."""

    start_ts: datetime
    """RFC 3339 timestamp for the start of the usage bucket."""


class AgentRetrieveResponse(BaseModel):
    data: List[Data]
    """Agent usage buckets in chronological order.

    Buckets with no recorded activity are returned with zero values.
    """
