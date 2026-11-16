# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["BatchCreateParams", "Recipient"]


class BatchCreateParams(TypedDict, total=False):
    agent_id: Required[str]
    """The identifier of the agent that handles the batch's calls."""

    from_number_id: Required[str]
    """The identifier of the phone number to place calls from.

    The attached provider handles outbound calling for this number.
    """

    name: Required[str]
    """A label for the batch."""

    recipients: Required[Iterable[Recipient]]
    """Destinations and optional per-call dynamic variables"""

    max_call_duration_minutes: int
    """Maximum call duration in minutes. Omit to use the default (480 minutes)."""

    region: Literal["US", "EU", "APAC"]
    """The region from which the batch's outbound calls are dispatched.

    Valid only when `from_number_id` is a SIP-trunk number; rejected for other
    telephony account types. Omit to derive the region from the telephony account.
    """

    ringing_timeout_seconds: int
    """Seconds to wait for the callee to answer before giving up.

    Omit to use the default (60 seconds).
    """

    scheduled_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """
    When to start dispatching the batch, as an RFC3339 timestamp with a timezone
    offset (e.g. `2026-06-15T16:00:00Z`). Must be in the future and within 30 days.
    Omit to dispatch immediately.
    """

    target_concurrency_limit: int
    """Maximum number of calls from this batch to dial concurrently.

    Must not exceed the organization's concurrency limit. Omit to default to half of
    the organization's agent-call concurrency limit, leaving headroom for other
    calls.
    """


class Recipient(TypedDict, total=False):
    """Destination and dynamic variables for one outbound call"""

    to_number: Required[str]
    """
    Destination phone number for this outbound call, in E.164 format (e.g.,
    `+14155559876`).
    """

    dynamic_variables: Dict[str, Union[str, float, bool]]
    """Custom values for this call.

    Supply values for variables used in the welcome message.

    Names are case-sensitive, up to 64 characters, and use letters, digits, or
    underscores. Start with a letter or underscore; `system__` and `secret__`
    prefixes are reserved. Limited to 16 KiB of UTF-8 JSON.
    """
