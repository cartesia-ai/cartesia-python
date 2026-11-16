# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = ["ProviderCreateParams", "CreateTwilioProviderBody", "Variant1"]


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


class Variant1(TypedDict, total=False):
    body: Required[object]


ProviderCreateParams: TypeAlias = Union[CreateTwilioProviderBody, Variant1]
