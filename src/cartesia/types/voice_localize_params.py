# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .gender import Gender
from .localize_dialect import LocalizeDialect
from .localize_target_language import LocalizeTargetLanguage

__all__ = ["VoiceLocalizeParams"]


class VoiceLocalizeParams(TypedDict, total=False):
    description: Required[str]
    """The description of the new localized voice."""

    language: Required[LocalizeTargetLanguage]
    """Target language to localize the voice to.

    Options: English (en), German (de), Spanish (es), French (fr), Japanese (ja),
    Portuguese (pt), Chinese (zh), Hindi (hi), Italian (it), Korean (ko), Dutch
    (nl), Polish (pl), Russian (ru), Swedish (sv), Turkish (tr), Arabic (ar),
    Hebrew (he), Tamil (ta), Telugu (te), Thai (th).
    """

    name: Required[str]
    """The name of the new localized voice."""

    original_speaker_gender: Required[Gender]

    voice_id: Required[str]
    """The ID of the voice to localize."""

    dialect: Optional[LocalizeDialect]
    """The dialect to localize to.

    Only supported for English (`en`), Spanish (`es`), Portuguese (`pt`), and French
    (`fr`).
    """
