# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .voice_accent import VoiceAccent

__all__ = ["Accent"]


class Accent(BaseModel):
    """One accent in the public catalog returned by GET /accents."""

    id: VoiceAccent
    """Catalog accent id from GET /accents (for example `southern-us` or `parisian`).

    Display names are rejected on this API version.
    """

    is_locale_default: bool
    """Whether this accent is the default for its `locale`."""

    is_localizable: bool
    """Whether POST /voices/localize can target this accent."""

    language: str
    """ISO 639-1 language subtag (for example `en`)."""

    locale: str
    """Canonical locale for this accent (BCP-47, for example `en-US`)."""

    name: str
    """Human-readable display name (for example `General American English`)."""
