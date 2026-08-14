# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .voice_accent import VoiceAccent
from .voice_locale import VoiceLocale
from .supported_language import SupportedLanguage
from .gender_presentation import GenderPresentation

__all__ = ["Voice"]


class Voice(BaseModel):
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
    """The description of the voice."""

    is_owner: bool
    """Whether your organization owns the voice."""

    language: SupportedLanguage
    """The language that the given voice should speak the transcript in.

    For valid options, see
    [Models](https://docs.cartesia.ai/build-with-cartesia/tts-models).
    """

    locales: List[VoiceLocale]
    """Locales this voice can speak.

    The native/source locale is first (`is_native: true`), followed by attached
    cross-lingual locales. Locale codes are BCP-47 language-region tags (for example
    `en-US`, `es-MX`).
    """

    name: str
    """The display name of the voice. Does not include the tagline."""

    tagline: str
    """A short descriptor for the voice (at most 32 characters).

    Empty string when unset.
    """

    visibility: Literal["owner", "all"]
    """When the resource is returned by the list endpoint.

    `owner` means the resource appears for the owner only. `all` means the resource
    appears for all users.
    """

    accent: Optional[VoiceAccent] = None
    """Catalog accent id from GET /accents (for example `southern-us` or `parisian`).

    Display names are rejected on this API version.
    """

    country: Optional[str] = None
    """Deprecated.

    Prefer `locales[].locale` (BCP-47). ISO 3166-1 alpha-2 country code when
    available (e.g. `US`, `GB`, `FR`).
    """

    gender: Optional[GenderPresentation] = None
    """The gender of the voice, if specified."""

    preview_file_url: Optional[str] = None
    """A URL to download a preview audio file for this voice.

    Useful to avoid consuming credits when looking for the right voice. The URL
    requires the same Authorization header. Voice previews may be changed, moved, or
    deleted so you should avoid storing the URL permanently. This property will be
    null if there's no preview available. Only included when `expand[]` includes
    `preview_file_url`.
    """
