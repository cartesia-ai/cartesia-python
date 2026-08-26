# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from .attach_voice_accent import AttachVoiceAccent

__all__ = ["VoiceAddAccentsParams"]


class VoiceAddAccentsParams(TypedDict, total=False):
    accents: Required[List[AttachVoiceAccent]]
    """Accents to add.

    A voice can support up to 10 accents in total, including native.
    """
