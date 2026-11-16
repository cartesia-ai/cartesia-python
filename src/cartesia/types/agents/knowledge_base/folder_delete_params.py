# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["FolderDeleteParams"]


class FolderDeleteParams(TypedDict, total=False):
    force: Literal["true", "false"]
    """Delete the folder even if it has subfolders or agents can search it.

    Its subfolders and documents are deleted too, and agents linked to any of them
    stop using them.
    """
