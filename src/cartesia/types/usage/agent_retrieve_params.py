# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AgentRetrieveParams"]


class AgentRetrieveParams(TypedDict, total=False):
    end_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """End of the time window, as an RFC 3339 datetime (with timezone).

    Rounded up to the start of the next UTC day, unless already at midnight.
    `start_ts` to `end_ts` cannot span more than a year. Must be strictly after
    `start_ts`.
    """

    interval: Optional[Literal["day", "week", "month"]]
    """Omit to receive a single bucket spanning from `start_ts` to `end_ts`."""

    start_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Start of the time window, as an RFC 3339 datetime (with timezone).

    Rounded down to the start of the UTC day. `start_ts` to `end_ts` cannot span
    more than a year.
    """
