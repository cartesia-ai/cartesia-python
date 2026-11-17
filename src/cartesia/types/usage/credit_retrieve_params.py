# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["CreditRetrieveParams"]


class CreditRetrieveParams(TypedDict, total=False):
    api_key_id: Optional[str]
    """Filter usage to a single API key.

    When set, only credits attributable to that key are returned. Can be combined
    with `group_by` for other dimensions (`capability`, `model`, `voice`), but not
    with `group_by=api_key`.
    """

    end_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """End of the time window, as an RFC 3339 datetime (with timezone).

    Rounded up to the start of the next UTC day, unless already at midnight.
    `start_ts` to `end_ts` cannot span more than a year.
    """

    group_by: Optional[Literal["capability", "model", "voice", "api_key"]]
    """Break down credit usage by capability, model, voice, or API key.

    When `interval` is set it must be `day`. Cannot be combined with `api_key_id`
    when `group_by=api_key`.
    """

    interval: Optional[Literal["day", "week", "month"]]
    """Omit to receive a single bucket spanning from `start_ts` to `end_ts`.

    When `group_by` is set, must be `day` if provided.
    """

    start_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]
    """Start of the time window, as an RFC 3339 datetime (with timezone).

    Rounded down to the start of the UTC day. `start_ts` to `end_ts` cannot span
    more than a year.
    """
