# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["PhonemeTimestamps"]


class PhonemeTimestamps(BaseModel):
    """Phoneme-level timing information."""

    end: List[float]
    """End times in seconds for each phoneme."""

    phonemes: List[str]
    """List of phonemes in order."""

    start: List[float]
    """Start times in seconds for each phoneme."""
