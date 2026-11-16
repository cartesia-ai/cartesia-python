# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["DocumentUpdateParams"]


class DocumentUpdateParams(TypedDict, total=False):
    content: str
    """New document text.

    Maximum 1 MB. Updating this property triggers re-indexing of the document.
    """

    folder_id: Optional[str]
    """Move the document to a different folder."""

    metadata: Dict[str, str]
    """
    Replacement metadata map. Updating this property triggers re-indexing of the
    document.
    """

    name: Optional[str]
    """New display name. Pass `null` to clear."""
