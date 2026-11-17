# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ...._types import SequenceNotStr

__all__ = [
    "ProviderCreateParams",
    "CreateTwilioProviderBody",
    "CreateSipProviderBody",
    "CreateSipProviderBodyInbound",
    "CreateSipProviderBodyInboundCredentials",
    "CreateSipProviderBodyOutbound",
    "CreateSipProviderBodyOutboundCredentials",
]


class CreateTwilioProviderBody(TypedDict, total=False):
    account_sid: Required[str]
    """Your Twilio account SID."""

    api_key_secret: Required[str]
    """The corresponding API key secret."""

    api_key_sid: Required[str]
    """A Twilio API key SID."""

    type: Required[Literal["twilio"]]
    """Must be `"twilio"`."""

    label: str
    """An optional human-readable label for the provider."""

    region: Literal["us1", "ie1", "au1"]
    """The Twilio region the phone number and API key are configured for.

    `us1` (US), `ie1` (Ireland), `au1` (Australia). Default is `us1`.
    """


class CreateSipProviderBody(TypedDict, total=False):
    label: Required[str]
    """A human-readable label for the provider."""

    type: Required[Literal["sip_trunk"]]
    """Must be `"sip_trunk"`."""

    inbound: CreateSipProviderBodyInbound
    """Inbound SIP configuration for creating a trunk."""

    outbound: CreateSipProviderBodyOutbound
    """Outbound SIP configuration for creating a trunk."""


class CreateSipProviderBodyInboundCredentials(TypedDict, total=False):
    """SIP digest authentication credentials."""

    password: Required[str]

    username: Required[str]


class CreateSipProviderBodyInbound(TypedDict, total=False):
    """Inbound SIP configuration for creating a trunk."""

    allowed_addresses: SequenceNotStr[str]
    """Source IP addresses or CIDR ranges allowed to send SIP traffic."""

    allowed_numbers: SequenceNotStr[str]
    """Caller numbers allowed on inbound calls."""

    credentials: CreateSipProviderBodyInboundCredentials
    """SIP digest authentication credentials."""

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """


class CreateSipProviderBodyOutboundCredentials(TypedDict, total=False):
    """SIP digest authentication credentials."""

    password: Required[str]

    username: Required[str]


class CreateSipProviderBodyOutbound(TypedDict, total=False):
    """Outbound SIP configuration for creating a trunk."""

    address: Required[str]
    """
    Carrier host that receives Cartesia's SIP INVITE, as `host` or `host:port`,
    without a `sip:` prefix. When the port is omitted, Cartesia uses 5060 for `tcp`
    and 5061 for `tls`. Set `host:port` if your carrier listens elsewhere, for
    example `sip.example.com:5067`.
    """

    transport: Required[Literal["tcp", "tls"]]
    """Transport for outbound SIP signaling."""

    credentials: CreateSipProviderBodyOutboundCredentials
    """SIP digest authentication credentials."""

    destination_country: str
    """Two-letter country code for the country the call terminates in (e.g.

    `US`, `GB`, `DE`). See
    [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    """

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """


ProviderCreateParams: TypeAlias = Union[CreateTwilioProviderBody, CreateSipProviderBody]
