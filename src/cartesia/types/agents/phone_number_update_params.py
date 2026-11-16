# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["PhoneNumberUpdateParams", "Provider", "ProviderByID", "ProviderByTwilioAccount"]


class PhoneNumberUpdateParams(TypedDict, total=False):
    agent_id: Optional[str]
    """Assign an agent to answer inbound calls to this number, or `null` to unassign."""

    label: str
    """A new human-readable name."""

    provider: Provider
    """Change the provider.

    Pass `{ "id": "..." }` for an existing provider, or pass Twilio account fields
    for lookup convenience. For Twilio, the phone number must exist in the target
    provider account. For SIP trunk providers, Cartesia handles reassignment between
    SIP providers. Switching between provider types is not supported; delete and
    re-import the number instead.
    """


class ProviderByID(TypedDict, total=False):
    id: Required[str]


class ProviderByTwilioAccount(TypedDict, total=False):
    account_sid: Required[str]

    type: Required[Literal["twilio"]]

    region: Literal["us1", "ie1", "au1"]
    """The Twilio region the phone number and API key are configured for.

    `us1` (US), `ie1` (Ireland), `au1` (Australia). Default is `us1`.
    """


Provider: TypeAlias = Union[ProviderByID, ProviderByTwilioAccount]
