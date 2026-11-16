# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["DocumentCreateParams"]


class DocumentCreateParams(TypedDict, total=False):
    content: str
    """The document text. Maximum 1 MB."""

    file_id: str
    """A file uploaded with purpose `knowledge_base_document`, instead of `content`.

    Its text is extracted in the background.
    """

    folder_id: Optional[str]
    """The folder to upload the document into. Omit or `null` to file it at the root."""

    metadata: Dict[str, str]
    """User-defined string-keyed metadata. Used to filter retrieval at query time."""

    name: Optional[str]
    """An optional display name for the document.

    Defaults to the file's name for a file.
    """
