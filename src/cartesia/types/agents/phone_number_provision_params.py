# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["PhoneNumberProvisionParams"]


class PhoneNumberProvisionParams(TypedDict, total=False):
    label: Required[str]
    """A human-readable name for the phone number."""

    agent_id: str
    """Optionally assign an agent to answer inbound calls to this number.

    Omit to keep the number outbound-only.
    """
