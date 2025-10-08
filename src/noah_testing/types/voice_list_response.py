# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .voice import Voice
from .._models import BaseModel

__all__ = ["VoiceListResponse"]


class VoiceListResponse(BaseModel):
    data: List[Voice]
    """The paginated list of Voices."""

    has_more: bool
    """
    Whether there are more Voices to fetch (using `starting_after=id`, where id is
    the ID of the last Voice in the current response).
    """

    next_page: Optional[str] = None
    """
    (Deprecated - use the id of the last Voice in the current response instead.) An
    ID that can be passed as `starting_after` to get the next page of Voices.
    """
