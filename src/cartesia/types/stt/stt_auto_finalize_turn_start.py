# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeTurnStart"]


class STTAutoFinalizeTurnStart(BaseModel):
    """Marks the start of a user turn.

    Fires quickly after the user begins speaking. This event can be used to interrupt your agent to avoid talking over the user.
    """

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    type: Literal["turn.start"]
    """Event type identifier."""
