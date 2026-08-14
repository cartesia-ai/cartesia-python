# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import FileTypes
from .voice_accent import VoiceAccent
from .supported_language import SupportedLanguage

__all__ = ["VoiceCloneParams"]


class VoiceCloneParams(TypedDict, total=False):
    clip: Required[FileTypes]

    language: Required[SupportedLanguage]
    """The language of the voice."""

    name: Required[str]
    """The name of the voice."""

    accent: Optional[VoiceAccent]
    """Catalog accent id from GET /accents (for example `southern-us` or `parisian`).

    Display names are rejected on this API version.
    """

    base_voice_id: Optional[str]
    """Optional base voice ID that the cloned voice is derived from."""

    description: Optional[str]
    """A description for the voice."""
