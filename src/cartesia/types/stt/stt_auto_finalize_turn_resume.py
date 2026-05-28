# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeTurnResume"]


class STTAutoFinalizeTurnResume(BaseModel):
    """[PREVIEW] Fires after `turn.eager_end` if the user turn has not actually ended."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    type: Literal["turn.resume"]
    """Event type identifier."""
