# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["Webhook"]


class Webhook(BaseModel):
    """A webhook including its secret.

    The secret is only returned when the webhook is created.
    """

    id: str
    """The ID of the webhook."""

    created_at: datetime
    """When the webhook was created."""

    secret: str
    """The shared secret. Returned only on creation."""

    updated_at: datetime
    """When the webhook was last updated."""

    url: str
    """The HTTPS endpoint call events are delivered to."""

    display_name: Optional[str] = None
    """The webhook's display name, or `null` if unset."""
