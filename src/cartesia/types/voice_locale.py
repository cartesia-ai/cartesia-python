# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["VoiceLocale"]


class VoiceLocale(BaseModel):
    """
    One locale a voice can speak, as a BCP-47 language-region tag plus whether it is the voice's native/source locale.
    """

    is_native: bool
    """Whether this is the voice's native/source locale."""

    locale: str
    """The locale's BCP-47 language-region tag (e.g. `en-US`)."""
