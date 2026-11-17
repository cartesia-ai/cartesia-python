# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .stt_language import STTLanguage

__all__ = ["STTLanguageConfidence"]


class STTLanguageConfidence(BaseModel):
    """A language detected in the audio, with the model's confidence"""

    confidence: float
    """
    Confidence that the audio contains this language, from 0 (not confident) to 1
    (very confident)
    """

    language: STTLanguage
    """Speech-to-text languages.

    See [the docs](https://docs.cartesia.ai/build-with-cartesia/stt-models/latest)
    for current language support.
    """
