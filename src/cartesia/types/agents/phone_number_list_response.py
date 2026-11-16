# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .phone_number import PhoneNumber

__all__ = ["PhoneNumberListResponse"]


class PhoneNumberListResponse(BaseModel):
    data: List[PhoneNumber]

    has_more: bool
