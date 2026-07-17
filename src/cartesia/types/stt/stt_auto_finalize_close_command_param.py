# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["STTAutoFinalizeCloseCommandParam"]


class STTAutoFinalizeCloseCommandParam(TypedDict, total=False):
    """Sent as a JSON-encoded WebSocket text frame to close the session cleanly.

    All buffered audio will be processed by the model into events before the connection closes.
    """

    type: Required[Literal["close"]]
    """Command type.

    Send this as a JSON-encoded WebSocket text frame to close the session.
    """
