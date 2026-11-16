# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["PhoneNumberImportParams", "Provider", "ProviderByID", "ProviderByTwilioAccount"]


class PhoneNumberImportParams(TypedDict, total=False):
    label: Required[str]
    """A human-readable name for the phone number."""

    number: Required[str]
    """The phone number in E.164 format."""

    provider: Required[Provider]
    """Reference to the provider.

    Pass `{ "id": "..." }` for an existing provider, or
    `{ "type": "twilio", "account_sid": "...", "region": "..." }` to look up by
    account.
    """

    agent_id: str
    """Optionally assign an agent to answer inbound calls to this number.

    Omit to keep the number outbound-only.
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
