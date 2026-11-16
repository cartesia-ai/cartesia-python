# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ModelListParams"]


class ModelListParams(TypedDict, total=False):
    ending_before: str
    """A cursor for pagination.

    Pass the ID of the first item from the previous page to fetch the previous page.
    """

    limit: int
    """The maximum number of items to return, ranging between 1 and 100."""

    starting_after: str
    """A cursor for pagination.

    Pass the ID of the last item from the previous page to fetch the next page.
    """
