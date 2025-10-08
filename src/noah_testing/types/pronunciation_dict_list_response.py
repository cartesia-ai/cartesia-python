# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .pronunciation_dict import PronunciationDict

__all__ = ["PronunciationDictListResponse"]


class PronunciationDictListResponse(BaseModel):
    data: List[PronunciationDict]
    """List of pronunciation dictionary objects"""

    has_more: bool
    """Whether there are more dictionaries available"""
