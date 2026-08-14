# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .voice_accent import VoiceAccent
from .fine_tune_base_model import FineTuneBaseModel

__all__ = ["FineTuneCreateParams"]


class FineTuneCreateParams(TypedDict, total=False):
    dataset: Required[str]
    """Dataset ID containing training files"""

    description: Required[str]
    """Description for the fine-tune"""

    language: Required[str]
    """Language code for the fine-tune"""

    model_id: Required[FineTuneBaseModel]
    """Base model for a fine-tune.

    See
    [the docs](https://docs.cartesia.ai/api-reference/fine-tunes/create#body-model-id)
    for all options.
    """

    name: Required[str]
    """Name for the new fine-tune"""

    accent: Optional[VoiceAccent]
    """Catalog accent id from GET /accents (for example `southern-us` or `parisian`).

    Display names are rejected on this API version.
    """
