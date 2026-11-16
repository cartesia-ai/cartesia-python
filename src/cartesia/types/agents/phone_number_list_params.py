# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["PhoneNumberListParams"]


class PhoneNumberListParams(TypedDict, total=False):
    agent_id: str
    """Filter by assigned agent ID."""

    ending_before: Optional[str]
    """A cursor to use in pagination.

    `ending_before` is a phone number ID that defines your place in the list. For
    example, if you make a `/agents/phone-numbers` request and receive 20 objects,
    starting with `pn_abc123`, your subsequent call can include
    `ending_before=pn_abc123` to fetch the previous page of the list.
    """

    limit: Optional[int]
    """
    (Pagination option) The number of phone numbers to return per page, ranging
    between 1 and 100. The default page limit is 10.
    """

    provider_id: str
    """Filter by provider ID."""

    q: str
    """Search by phone number, label, or agent name."""

    starting_after: Optional[str]
    """A cursor to use in pagination.

    `starting_after` is a phone number ID that defines your place in the list. For
    example, if you make a `/agents/phone-numbers` request and receive 20 objects,
    ending with `pn_abc123`, your subsequent call can include
    `starting_after=pn_abc123` to fetch the next page of the list.
    """

    type: Literal["twilio", "cartesia", "sip_trunk"]
    """Filter by provider type."""
