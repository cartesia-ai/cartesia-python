# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel
from .voice_accent import VoiceAccent
from .voice_locale import VoiceLocale
from .supported_language import SupportedLanguage
from .gender_presentation import GenderPresentation

__all__ = ["Voice"]


class Voice(BaseModel):
    id: str
    """The ID of the voice."""

    created_at: datetime
    """The date and time the voice was created."""

    description: str
    """The description of the voice."""

    is_owner: bool
    """Whether your organization owns the voice."""

    is_public: bool
    """Whether the voice is publicly accessible."""

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
    """The name of the voice."""

    accent: Optional[VoiceAccent] = None
    """
    Canonical accent display name for the voice (for example `British English` or
    `General American English`).
    """

    country: Optional[str] = None
    """
    The country associated with the voice, as an ISO 3166-1 alpha-2 code when
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
