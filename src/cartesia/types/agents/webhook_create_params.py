# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["WebhookCreateParams"]


class WebhookCreateParams(TypedDict, total=False):
    secret: Required[str]
    """A shared secret.

    Cartesia returns it in the `X-Webhook-Secret` header on every delivery so your
    endpoint can verify the request.
    """

    url: Required[str]
    """The HTTPS endpoint Cartesia POSTs call events to."""

    display_name: str
    """An optional name to identify the webhook."""
