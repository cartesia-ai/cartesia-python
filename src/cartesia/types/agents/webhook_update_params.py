# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    url: Required[str]
    """The HTTPS endpoint Cartesia POSTs call events to."""

    display_name: str
    """An optional name to identify the webhook."""

    secret: str
    """A new shared secret. Omit to leave the existing secret unchanged."""
