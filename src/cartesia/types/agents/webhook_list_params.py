# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["WebhookListParams"]


class WebhookListParams(TypedDict, total=False):
    ending_before: str
    """A cursor for pagination.

    Pass the ID of the first webhook from the previous page to fetch the previous
    page.
    """

    limit: int
    """The number of webhooks to return per page, ranging between 1 and 100.

    Defaults to 10.
    """

    starting_after: str
    """A cursor for pagination.

    Pass the ID of the last webhook from the previous page to fetch the next page.
    """
