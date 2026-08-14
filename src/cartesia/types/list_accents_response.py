# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .accent import Accent
from .._models import BaseModel

__all__ = ["ListAccentsResponse"]


class ListAccentsResponse(BaseModel):
    accents: List[Accent]
    """Official accents, sorted by id."""
