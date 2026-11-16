# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["FolderUpdateParams", "Agent", "Document"]


class FolderUpdateParams(TypedDict, total=False):
    force: Literal["true", "false"]
    """Delete the documents left out of `documents` even if agents can search them.

    Agents linked to them stop using them.
    """

    agents: Iterable[Agent]
    """The complete set of agents that have access to this folder.

    Agents not in the list have their access revoked. Pass an empty array to revoke
    access for all agents.
    """

    documents: Iterable[Document]
    """The complete set of documents that should be in this folder.

    Documents not in the list are deleted. Pass an empty array to delete all
    documents in the folder.
    """

    name: str
    """A new name for the folder. Must be unique among siblings."""

    parent_id: Optional[str]
    """Move the folder under a new parent, or `null` to move it to the top level.

    Cannot create a circular reference.
    """


class Agent(TypedDict, total=False):
    id: Required[str]


class Document(TypedDict, total=False):
    id: Required[str]
