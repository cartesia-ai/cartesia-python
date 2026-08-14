# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

__all__ = ["VoiceSpecifierParam", "TTSRequestVoiceObject"]


class TTSRequestVoiceObject(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """Voice object.

    `id` is required; other fields may be added in future API versions.
    """

    id: Required[str]
    """The ID of the voice."""


VoiceSpecifierParam: TypeAlias = Union[str, TTSRequestVoiceObject]
