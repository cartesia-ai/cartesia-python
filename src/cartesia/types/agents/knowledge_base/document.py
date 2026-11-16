# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["Document"]


class Document(BaseModel):
    id: str
    """The ID of the document."""

    content: str
    """The full document text."""

    created_at: datetime
    """When the document was uploaded."""

    error: Optional[str] = None
    """Why processing failed. `null` unless `status` is `failed`."""

    metadata: Dict[str, str]
    """User-defined string-keyed metadata."""

    name: Optional[str] = None
    """The document's display name, or `null` if unnamed."""

    status: Literal["processing", "ready", "failed"]
    """Processing state of the document."""
