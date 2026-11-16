# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["CallCancelResponse"]


class CallCancelResponse(BaseModel):
    cancelled: bool
    """Always `true` when the cancel is confirmed."""
