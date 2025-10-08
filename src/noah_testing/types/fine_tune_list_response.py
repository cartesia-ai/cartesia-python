# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .fine_tune import FineTune

__all__ = ["FineTuneListResponse"]


class FineTuneListResponse(BaseModel):
    data: List[FineTune]
    """List of fine-tune objects"""

    has_more: bool
    """Whether there are more fine-tunes available"""
