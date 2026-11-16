# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ProviderListParams"]


class ProviderListParams(TypedDict, total=False):
    account_sid: str
    """Filter by account SID (Twilio providers only)."""

    type: Literal["twilio", "sip_trunk"]
    """Filter by provider type."""
