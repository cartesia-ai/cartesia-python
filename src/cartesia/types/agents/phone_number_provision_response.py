# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["PhoneNumberProvisionResponse", "Agent"]


class Agent(BaseModel):
    """The agent that answers inbound calls to this number, or `null` if unassigned"""

    id: str

    name: str


class PhoneNumberProvisionResponse(BaseModel):
    """Common phone number fields."""

    id: str
    """Unique identifier for the phone number."""

    agent: Optional[Agent] = None
    """The agent that answers inbound calls to this number, or `null` if unassigned"""

    created_at: datetime
    """UTC timestamp when the phone number was created."""

    number: str
    """The phone number in E.164 format (e.g. +14155551234)."""

    updated_at: datetime
    """UTC timestamp when the phone number was last updated."""

    label: Optional[str] = None
    """A human-readable name for the phone number."""
