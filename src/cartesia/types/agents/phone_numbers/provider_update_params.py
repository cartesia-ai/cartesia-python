# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ...._types import SequenceNotStr

__all__ = [
    "ProviderUpdateParams",
    "UpdateTwilioProviderBody",
    "UpdateSipTrunkProviderBody",
    "UpdateSipTrunkProviderBodyInbound",
    "UpdateSipTrunkProviderBodyInboundCredentials",
    "UpdateSipTrunkProviderBodyOutbound",
    "UpdateSipTrunkProviderBodyOutboundCredentials",
]


class UpdateTwilioProviderBody(TypedDict, total=False):
    api_key_secret: Required[str]
    """New API key secret."""

    api_key_sid: Required[str]
    """New Twilio API key SID."""

    type: Required[Literal["twilio"]]
    """Must be `"twilio"`."""

    region: Literal["us1", "ie1", "au1"]
    """The Twilio region the phone number and API key are configured for.

    `us1` (US), `ie1` (Ireland), `au1` (Australia). Default is `us1`.
    """


class UpdateSipTrunkProviderBody(TypedDict, total=False):
    type: Required[Literal["sip_trunk"]]
    """Must be `"sip_trunk"`."""

    inbound: UpdateSipTrunkProviderBodyInbound
    """Inbound SIP configuration for updating a trunk.

    Omitted fields remain unchanged. Send `[]` to clear an allowlist.
    """

    label: str
    """A new human-readable label for the provider. Omit to leave unchanged."""

    outbound: UpdateSipTrunkProviderBodyOutbound
    """Outbound SIP configuration for updating a trunk.

    `address` and `transport` are immutable on an existing outbound trunk, but
    required when adding outbound to an inbound-only provider.
    """


class UpdateSipTrunkProviderBodyInboundCredentials(TypedDict, total=False):
    """SIP digest authentication credentials for an update.

    The username is required when credentials are provided. Omit the password to keep the stored secret, or send `null` to clear the credentials.
    """

    username: Required[str]

    password: str


class UpdateSipTrunkProviderBodyInbound(TypedDict, total=False):
    """Inbound SIP configuration for updating a trunk.

    Omitted fields remain unchanged. Send `[]` to clear an allowlist.
    """

    allowed_addresses: SequenceNotStr[str]
    """Source IP addresses or CIDR ranges allowed to send SIP traffic."""

    allowed_numbers: SequenceNotStr[str]
    """Caller numbers allowed on inbound calls."""

    credentials: Optional[UpdateSipTrunkProviderBodyInboundCredentials]
    """SIP digest authentication credentials for an update.

    The username is required when credentials are provided. Omit the password to
    keep the stored secret, or send `null` to clear the credentials.
    """

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """


class UpdateSipTrunkProviderBodyOutboundCredentials(TypedDict, total=False):
    """SIP digest authentication credentials for an update.

    The username is required when credentials are provided. Omit the password to keep the stored secret, or send `null` to clear the credentials.
    """

    username: Required[str]

    password: str


class UpdateSipTrunkProviderBodyOutbound(TypedDict, total=False):
    """Outbound SIP configuration for updating a trunk.

    `address` and `transport` are immutable on an existing outbound trunk, but required when adding outbound to an inbound-only provider.
    """

    address: str
    """Required only when adding outbound to an inbound-only provider."""

    credentials: Optional[UpdateSipTrunkProviderBodyOutboundCredentials]
    """SIP digest authentication credentials for an update.

    The username is required when credentials are provided. Omit the password to
    keep the stored secret, or send `null` to clear the credentials.
    """

    destination_country: Optional[str]
    """Send `null` to clear."""

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """

    transport: Literal["tcp", "tls"]
    """Transport for outbound SIP signaling."""


ProviderUpdateParams: TypeAlias = Union[UpdateTwilioProviderBody, UpdateSipTrunkProviderBody]
