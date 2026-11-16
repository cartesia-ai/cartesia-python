# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel

__all__ = [
    "ProviderListResponse",
    "ProviderListResponseItem",
    "ProviderListResponseItemTwilioProviderResponse",
    "ProviderListResponseItemSipTrunkProviderResponse",
    "ProviderListResponseItemSipTrunkProviderResponseInbound",
    "ProviderListResponseItemSipTrunkProviderResponseOutbound",
]


class ProviderListResponseItemTwilioProviderResponse(BaseModel):
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


class ProviderListResponseItemSipTrunkProviderResponseInbound(BaseModel):
    """Inbound SIP configuration.

    Passwords are never returned; only the configured username is exposed as `auth_username`.
    """

    allowed_addresses: List[str]
    """Source IP addresses or CIDR ranges allowed to send SIP traffic."""

    allowed_numbers: List[str]
    """Caller numbers allowed on inbound calls."""

    auth_username: str
    """SIP username returned without the password."""

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """


class ProviderListResponseItemSipTrunkProviderResponseOutbound(BaseModel):
    """Outbound SIP configuration.

    Passwords are never returned; only the configured username is exposed as `auth_username`.
    """

    address: str
    """
    Carrier host that receives Cartesia's SIP INVITE, as `host` or `host:port`. When
    the port is omitted, Cartesia uses 5060 for `tcp` and 5061 for `tls`.
    """

    auth_username: str
    """SIP username returned without the password."""

    media_encryption: Literal["disabled", "allowed", "required"]
    """SRTP policy for call audio.

    `disabled` does not negotiate encryption, `allowed` uses encryption when
    available, and `required` rejects calls that cannot use encryption.
    """

    transport: Literal["tcp", "tls"]
    """Transport for outbound SIP signaling."""

    destination_country: Optional[str] = None
    """
    Two-letter ISO 3166-1 alpha-2 destination country code, or an empty string if
    not set.
    """


class ProviderListResponseItemSipTrunkProviderResponse(BaseModel):
    """A linked SIP trunk provider."""

    id: str
    """Unique identifier for the provider."""

    type: Literal["sip_trunk"]
    """Always `"sip_trunk"`."""

    inbound: Optional[ProviderListResponseItemSipTrunkProviderResponseInbound] = None
    """Inbound SIP configuration.

    Passwords are never returned; only the configured username is exposed as
    `auth_username`.
    """

    label: Optional[str] = None
    """A human-readable label for the provider."""

    outbound: Optional[ProviderListResponseItemSipTrunkProviderResponseOutbound] = None
    """Outbound SIP configuration.

    Passwords are never returned; only the configured username is exposed as
    `auth_username`.
    """


ProviderListResponseItem: TypeAlias = Annotated[
    Union[ProviderListResponseItemTwilioProviderResponse, ProviderListResponseItemSipTrunkProviderResponse],
    PropertyInfo(discriminator="type"),
]

ProviderListResponse: TypeAlias = List[ProviderListResponseItem]
