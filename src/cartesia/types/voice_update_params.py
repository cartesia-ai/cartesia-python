# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .voice_accent import VoiceAccent
from .gender_presentation import GenderPresentation

__all__ = ["VoiceUpdateParams"]


class VoiceUpdateParams(TypedDict, total=False):
    accent: Optional[VoiceAccent]
    """Catalog accent id from GET /accents (for example `southern-us` or `parisian`).

    Display names are rejected on this API version.
    """

    description: str
    """The description of the voice."""

    gender: Optional[GenderPresentation]

    name: str
    """The name of the voice."""
