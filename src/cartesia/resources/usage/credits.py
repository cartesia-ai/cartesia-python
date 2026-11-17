# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.usage import credit_retrieve_params
from ..._base_client import make_request_options
from ...types.usage.credit_retrieve_response import CreditRetrieveResponse

__all__ = ["CreditsResource", "AsyncCreditsResource"]


class CreditsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CreditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return CreditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CreditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return CreditsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        *,
        api_key_id: Optional[str] | Omit = omit,
        end_ts: Union[str, datetime, None] | Omit = omit,
        group_by: Optional[Literal["capability", "model", "voice", "api_key"]] | Omit = omit,
        interval: Optional[Literal["day", "week", "month"]] | Omit = omit,
        start_ts: Union[str, datetime, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreditRetrieveResponse:
        """
        Returns your credit usage over time, bucketed by the requested interval.

        Args:
          api_key_id: Filter usage to a single API key. When set, only credits attributable to that
              key are returned. Can be combined with `group_by` for other dimensions
              (`capability`, `model`, `voice`), but not with `group_by=api_key`.

          end_ts: End of the time window, as an RFC 3339 datetime (with timezone). Rounded up to
              the start of the next UTC day, unless already at midnight. `start_ts` to
              `end_ts` cannot span more than a year.

          group_by: Break down credit usage by capability, model, voice, or API key. When `interval`
              is set it must be `day`. Cannot be combined with `api_key_id` when
              `group_by=api_key`.

          interval: Omit to receive a single bucket spanning from `start_ts` to `end_ts`. When
              `group_by` is set, must be `day` if provided.

          start_ts: Start of the time window, as an RFC 3339 datetime (with timezone). Rounded down
              to the start of the UTC day. `start_ts` to `end_ts` cannot span more than a
              year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/usage/credits",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "api_key_id": api_key_id,
                        "end_ts": end_ts,
                        "group_by": group_by,
                        "interval": interval,
                        "start_ts": start_ts,
                    },
                    credit_retrieve_params.CreditRetrieveParams,
                ),
            ),
            cast_to=CreditRetrieveResponse,
        )


class AsyncCreditsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCreditsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCreditsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCreditsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncCreditsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        *,
        api_key_id: Optional[str] | Omit = omit,
        end_ts: Union[str, datetime, None] | Omit = omit,
        group_by: Optional[Literal["capability", "model", "voice", "api_key"]] | Omit = omit,
        interval: Optional[Literal["day", "week", "month"]] | Omit = omit,
        start_ts: Union[str, datetime, None] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CreditRetrieveResponse:
        """
        Returns your credit usage over time, bucketed by the requested interval.

        Args:
          api_key_id: Filter usage to a single API key. When set, only credits attributable to that
              key are returned. Can be combined with `group_by` for other dimensions
              (`capability`, `model`, `voice`), but not with `group_by=api_key`.

          end_ts: End of the time window, as an RFC 3339 datetime (with timezone). Rounded up to
              the start of the next UTC day, unless already at midnight. `start_ts` to
              `end_ts` cannot span more than a year.

          group_by: Break down credit usage by capability, model, voice, or API key. When `interval`
              is set it must be `day`. Cannot be combined with `api_key_id` when
              `group_by=api_key`.

          interval: Omit to receive a single bucket spanning from `start_ts` to `end_ts`. When
              `group_by` is set, must be `day` if provided.

          start_ts: Start of the time window, as an RFC 3339 datetime (with timezone). Rounded down
              to the start of the UTC day. `start_ts` to `end_ts` cannot span more than a
              year.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/usage/credits",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "api_key_id": api_key_id,
                        "end_ts": end_ts,
                        "group_by": group_by,
                        "interval": interval,
                        "start_ts": start_ts,
                    },
                    credit_retrieve_params.CreditRetrieveParams,
                ),
            ),
            cast_to=CreditRetrieveResponse,
        )


class CreditsResourceWithRawResponse:
    def __init__(self, credits: CreditsResource) -> None:
        self._credits = credits

        self.retrieve = to_raw_response_wrapper(
            credits.retrieve,
        )


class AsyncCreditsResourceWithRawResponse:
    def __init__(self, credits: AsyncCreditsResource) -> None:
        self._credits = credits

        self.retrieve = async_to_raw_response_wrapper(
            credits.retrieve,
        )


class CreditsResourceWithStreamingResponse:
    def __init__(self, credits: CreditsResource) -> None:
        self._credits = credits

        self.retrieve = to_streamed_response_wrapper(
            credits.retrieve,
        )


class AsyncCreditsResourceWithStreamingResponse:
    def __init__(self, credits: AsyncCreditsResource) -> None:
        self._credits = credits

        self.retrieve = async_to_streamed_response_wrapper(
            credits.retrieve,
        )
