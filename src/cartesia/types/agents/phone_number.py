# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel

__all__ = [
    "PhoneNumber",
    "Agent",
    "Provider",
    "ProviderTwilioProviderResponse",
    "ProviderCartesiaProviderResponse",
    "ProviderSipTrunkEmbeddedResponse",
]


class Agent(BaseModel):
    """The agent that answers inbound calls to this number, or `null` if unassigned"""

    id: str

    name: str


class ProviderTwilioProviderResponse(BaseModel):
    """A linked Twilio account.

    The `api_key_sid` field is partially masked in responses.
    """

    id: str
    """Unique identifier for the provider."""

    account_sid: str
    """The Twilio account SID."""

    api_key_sid: str
    """The Twilio API key SID (partially masked)."""

    region: Literal["us1", "ie1", "au1"]
    """The Twilio region the phone number and API key are configured for.

    `us1` (US), `ie1` (Ireland), `au1` (Australia). Default is `us1`.
    """

    type: Literal["twilio"]
    """Always `"twilio"`."""

    label: Optional[str] = None
    """A human-readable label for the provider."""


class ProviderCartesiaProviderResponse(BaseModel):
    """A Cartesia-managed provider. US phone numbers only."""

    type: Literal["cartesia"]
    """Always `"cartesia"`."""


class ProviderSipTrunkEmbeddedResponse(BaseModel):
    """A linked SIP trunk provider."""

    id: str
    """Unique identifier for the provider."""

    type: Literal["sip_trunk"]
    """Always `"sip_trunk"`."""

    label: Optional[str] = None
    """A human-readable label for the provider."""


Provider: TypeAlias = Annotated[
    Union[ProviderTwilioProviderResponse, ProviderCartesiaProviderResponse, ProviderSipTrunkEmbeddedResponse],
    PropertyInfo(discriminator="type"),
]


class PhoneNumber(BaseModel):
    """A phone number with its provider and agent assignment details."""

    id: str
    """Unique identifier for the phone number."""

    agent: Optional[Agent] = None
    """The agent that answers inbound calls to this number, or `null` if unassigned"""

    created_at: datetime
    """UTC timestamp when the phone number was created."""

    number: str
    """The phone number in E.164 format (e.g. +14155551234)."""

    provider: Provider
    """The telephony provider associated with a phone number.

    One of `Twilio`, `Cartesia`, or `SIP Trunk`, determined by the `type` field. For
    SIP trunk numbers, `inbound` and `outbound` are not returned here — use
    `GET /agents/phone-numbers/providers/{id}` to retrieve them.
    """

    updated_at: datetime
    """UTC timestamp when the phone number was last updated."""

    label: Optional[str] = None
    """A human-readable name for the phone number."""
