# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["FolderCreateParams"]


class FolderCreateParams(TypedDict, total=False):
    name: Required[str]
    """A human-readable name for the folder. Must be unique among siblings."""

    parent_id: Optional[str]
    """ID of the parent folder.

    Omit or pass `null` to create a top-level folder. Folders can be nested at most
    three levels deep.
    """
