# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Required, TypedDict

__all__ = ["CallCreateParams", "OutboundCall"]


class CallCreateParams(TypedDict, total=False):
    agent_id: Required[str]
    """Agent that handles the outbound calls."""

    from_number_id: Required[str]
    """Phone number ID to place calls from.

    The attached provider handles outbound calling for this number.
    """

    outbound_calls: Required[Iterable[OutboundCall]]
    """Destinations and optional per-call dynamic variables"""

    max_call_duration_minutes: int
    """Optional maximum call duration in minutes."""

    ringing_timeout_seconds: int
    """Seconds to wait for the callee to answer before giving up.

    Omit to use the default (60 seconds).
    """


class OutboundCall(TypedDict, total=False):
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
