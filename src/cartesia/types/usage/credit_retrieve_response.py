# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel

__all__ = [
    "CreditRetrieveResponse",
    "Data",
    "DataUsageCreditsBucket",
    "DataUsageCreditsBreakdownSeries",
    "DataUsageCreditsBreakdownSeriesBucket",
]


class DataUsageCreditsBucket(BaseModel):
    """A single bucket of credit usage within a time window."""

    credits: int
    """Total credits consumed within the bucket."""

    end_ts: datetime
    """RFC 3339 timestamp for the end of the usage bucket."""

    start_ts: datetime
    """RFC 3339 timestamp for the start of the usage bucket."""


class DataUsageCreditsBreakdownSeriesBucket(BaseModel):
    """A single bucket of credit usage within a time window."""

    credits: int
    """Total credits consumed within the bucket."""

    end_ts: datetime
    """RFC 3339 timestamp for the end of the usage bucket."""

    start_ts: datetime
    """RFC 3339 timestamp for the start of the usage bucket."""


class DataUsageCreditsBreakdownSeries(BaseModel):
    """Credit usage for one value of the requested group-by dimension."""

    id: str
    """
    Identifier for the dimension value (capability id, model id, voice id, or API
    key id / sentinel such as `playground` or `unnamed_key`).
    """

    buckets: List[DataUsageCreditsBreakdownSeriesBucket]
    """Daily credit buckets for this dimension value."""

    label: Optional[str] = None
    """Human-readable label when available (voice name, API key description, etc.)."""


Data: TypeAlias = Union[DataUsageCreditsBucket, DataUsageCreditsBreakdownSeries]


class CreditRetrieveResponse(BaseModel):
    data: List[Data]
    """Without `group_by`, flat credit usage buckets in chronological order.

    With `group_by`, one entry per dimension value; each item includes `id`,
    optional `label`, and nested daily `buckets`. Empty usage periods are returned
    with `credits: 0`.
    """

    group_by: Optional[Literal["capability", "model", "voice", "api_key"]] = None
    """Present when the request included `group_by`."""
