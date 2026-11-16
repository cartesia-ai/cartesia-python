# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["DocumentDeleteParams"]


class DocumentDeleteParams(TypedDict, total=False):
    force: Literal["true", "false"]
    """Delete the document even if agents can search it.

    Agents linked to it stop using it.
    """
