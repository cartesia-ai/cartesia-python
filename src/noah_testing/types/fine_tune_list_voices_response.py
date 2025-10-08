# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .voice import Voice
from .._models import BaseModel

__all__ = ["FineTuneListVoicesResponse"]


class FineTuneListVoicesResponse(BaseModel):
    data: List[Voice]
    """List of voice objects"""

    has_more: bool
    """Whether there are more voices available"""
