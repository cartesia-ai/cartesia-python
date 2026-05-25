# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["WordTimestamps"]


class WordTimestamps(BaseModel):
    """Word-level timing information."""

    end: List[float]
    """End times in seconds for each word."""

    start: List[float]
    """Start times in seconds for each word."""

    words: List[str]
    """List of words in order."""
