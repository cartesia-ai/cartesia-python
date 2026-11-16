# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .folder import Folder
from ...._models import BaseModel

__all__ = ["FolderListResponse", "Data", "RootDocument", "RootDocumentAgent"]


class Data(Folder):
    """A folder with its nested subfolders."""

    children: List[Folder]
    """Nested subfolders, up to the requested `depth`.

    Each child has the same shape as this object, including its own `children`.
    """


class RootDocumentAgent(BaseModel):
    """An agent that has access to this folder."""

    id: str
    """The ID of the agent."""

    name: str
    """The name of the agent."""


class RootDocument(BaseModel):
    """A document summary as returned inside a folder.

    Does not include the document `content`.
    """

    id: str
    """The ID of the document."""

    agents: List[RootDocumentAgent]
    """Agents linked to this document directly, not through a folder."""

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


class FolderListResponse(BaseModel):
    data: List[Data]
    """The paginated list of top-level folders matching the request."""

    has_more: bool
    """Whether more results are available after this page."""

    next_page: Optional[str] = None
    """
    An ID that can be passed as `starting_after` or `ending_before` to get the next
    page.
    """

    root_documents: Optional[List[RootDocument]] = None
    """Documents at the root, outside any folder.

    Listed on the first page of top-level folders only.
    """
