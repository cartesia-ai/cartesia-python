# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["WebhookListResponse"]


class WebhookListResponse(BaseModel):
    """A webhook without its secret, as returned by list and get."""

    id: str
    """The ID of the webhook."""

    created_at: datetime
    """When the webhook was created."""

    updated_at: datetime
    """When the webhook was last updated."""

    url: str
    """The HTTPS endpoint call events are delivered to."""

    display_name: Optional[str] = None
    """The webhook's display name, or `null` if unset."""
