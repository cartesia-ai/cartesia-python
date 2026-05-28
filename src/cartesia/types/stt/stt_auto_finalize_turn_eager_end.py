# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["STTAutoFinalizeTurnEagerEnd"]


class STTAutoFinalizeTurnEagerEnd(BaseModel):
    """[PREVIEW] Fires when the model predicts that the user might be done speaking."""

    request_id: str
    """Unique identifier for this connection. Does not change between turns."""

    transcript: str
    """Cumulative text for the current turn."""

    type: Literal["turn.eager_end"]
    """Event type identifier."""
