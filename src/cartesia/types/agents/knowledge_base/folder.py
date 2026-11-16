# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["Folder", "Agent", "Document", "DocumentAgent"]


class Agent(BaseModel):
    """An agent that has access to this folder."""

    id: str
    """The ID of the agent."""

    name: str
    """The name of the agent."""


class DocumentAgent(BaseModel):
    """An agent that has access to this folder."""

    id: str
    """The ID of the agent."""

    name: str
    """The name of the agent."""


class Document(BaseModel):
    """A document summary as returned inside a folder.

    Does not include the document `content`.
    """

    id: str
    """The ID of the document."""

    agents: List[DocumentAgent]
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


class Folder(BaseModel):
    id: str
    """The ID of the folder."""

    agents: List[Agent]
    """Agents that have access to this folder."""

    created_at: datetime
    """When the folder was created."""

    documents: List[Document]
    """Documents inside this folder."""

    name: str
    """The folder's name."""

    parent_id: Optional[str] = None
    """The ID of the parent folder, or `null` for top-level folders."""
