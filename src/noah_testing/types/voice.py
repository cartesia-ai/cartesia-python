# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel
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
    """Whether the current user is the owner of the voice."""

    is_public: bool
    """Whether the voice is publicly accessible."""

    language: SupportedLanguage
    """The language that the given voice should speak the transcript in.

    Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
    Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
    Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).
    """

    name: str
    """The name of the voice."""

    gender: Optional[GenderPresentation] = None
    """The gender of the voice, if specified."""

    is_starred: Optional[bool] = None
    """Whether the current user has starred the voice.

    Only included when `expand` includes `is_starred`.
    """
