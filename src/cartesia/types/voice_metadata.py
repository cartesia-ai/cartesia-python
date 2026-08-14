# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .supported_language import SupportedLanguage

__all__ = ["VoiceMetadata"]


class VoiceMetadata(BaseModel):
    id: str
    """The ID of the voice."""

    access: Literal["private", "public"]
    """Who can use the resource.

    `private` means only the owner can use the resource. `public` means everyone can
    use the resource.
    """

    created_at: datetime
    """The date and time the voice was created."""

    description: str
    """
    A description for the voice, typically longer than the tagline if both are
    provided.
    """

    language: SupportedLanguage
    """The language that the given voice should speak the transcript in.

    For valid options, see
    [Models](https://docs.cartesia.ai/build-with-cartesia/tts-models).
    """

    name: str
    """The name of the voice."""

    tagline: str
    """A few words describing the voice."""

    user_id: str
    """The ID of the user who owns the voice."""

    visibility: Literal["owner", "all"]
    """When the resource is returned by the list endpoint.

    `owner` means the resource appears for the owner only. `all` means the resource
    appears for all users.
    """
