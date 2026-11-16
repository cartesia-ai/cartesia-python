# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["AgentSummary"]


class AgentSummary(BaseModel):
    id: str
    """Unique identifier for the agent."""

    created_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
    """

    description: Optional[str] = None
    """Description of the agent."""

    name: str
    """Name shown for the agent."""

    updated_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
    """

    version_id: str
    """Unique identifier for an immutable agent configuration version."""
