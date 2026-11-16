# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from ...._types import SequenceNotStr

__all__ = ["FolderListParams"]


class FolderListParams(TypedDict, total=False):
    depth: int
    """How many levels of nested children to include in the response, between 1 and 3.

    Defaults to 3.
    """

    ending_before: str
    """A cursor for pagination.

    Pass the ID of the first folder from the previous page to fetch the previous
    page.
    """

    limit: int
    """The number of folders to return per page, ranging between 1 and 100.

    Defaults to 10. Pagination applies to the top-level folders in the response;
    nested children do not count against this limit.
    """

    parent_ids: SequenceNotStr[str]
    """Filter to folders with these parent IDs.

    Repeat the parameter to pass multiple values (e.g.,
    `?parent_ids[]=folder_abc&parent_ids[]=null`). Pass the literal string `null` to
    include top-level folders. Defaults to `[null]` (top-level folders only).
    """

    starting_after: str
    """A cursor for pagination.

    Pass the ID of the last folder from the previous page to fetch the next page.
    """
