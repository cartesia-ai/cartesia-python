# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._types import FileTypes
from .supported_language import SupportedLanguage

__all__ = ["VoiceCloneParams"]


class VoiceCloneParams(TypedDict, total=False):
    base_voice_id: Optional[str]
    """Optional base voice ID that the cloned voice is derived from."""

    clip: FileTypes

    description: Optional[str]
    """A description for the voice."""

    enhance: Optional[bool]
    """Whether to apply AI enhancements to the clip to reduce background noise.

    This is not recommended unless the source clip is extremely low quality.
    """

    language: SupportedLanguage
    """The language of the voice."""

    name: str
    """The name of the voice."""
