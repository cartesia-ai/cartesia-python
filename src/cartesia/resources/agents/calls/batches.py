# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import datetime
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....pagination import SyncCursorIDPage, AsyncCursorIDPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.agents.calls import batch_list_params, batch_create_params
from ....types.agents.call_batch import CallBatch

__all__ = ["BatchesResource", "AsyncBatchesResource"]


class BatchesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BatchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return BatchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BatchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return BatchesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        agent_id: str,
        from_number_id: str,
        name: str,
        recipients: Iterable[batch_create_params.Recipient],
        max_call_duration_minutes: int | Omit = omit,
        region: Literal["US", "EU", "APAC"] | Omit = omit,
        ringing_timeout_seconds: int | Omit = omit,
        scheduled_at: Union[str, datetime] | Omit = omit,
        target_concurrency_limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """Queues a batch of outbound calls.

        Calls are issued gradually, subject to the
        organization's and the batch's concurrency limits.

        Args:
          agent_id: The identifier of the agent that handles the batch's calls.

          from_number_id: The identifier of the phone number to place calls from. The attached provider
              handles outbound calling for this number.

          name: A label for the batch.

          recipients: Destinations and optional per-call dynamic variables

          max_call_duration_minutes: Maximum call duration in minutes. Omit to use the default (480 minutes).

          region: The region from which the batch's outbound calls are dispatched. Valid only when
              `from_number_id` is a SIP-trunk number; rejected for other telephony account
              types. Omit to derive the region from the telephony account.

          ringing_timeout_seconds: Seconds to wait for the callee to answer before giving up. Omit to use the
              default (60 seconds).

          scheduled_at: When to start dispatching the batch, as an RFC3339 timestamp with a timezone
              offset (e.g. `2026-06-15T16:00:00Z`). Must be in the future and within 30 days.
              Omit to dispatch immediately.

          target_concurrency_limit: Maximum number of calls from this batch to dial concurrently. Must not exceed
              the organization's concurrency limit. Omit to default to half of the
              organization's agent-call concurrency limit, leaving headroom for other calls.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/calls/batches",
            body=maybe_transform(
                {
                    "agent_id": agent_id,
                    "from_number_id": from_number_id,
                    "name": name,
                    "recipients": recipients,
                    "max_call_duration_minutes": max_call_duration_minutes,
                    "region": region,
                    "ringing_timeout_seconds": ringing_timeout_seconds,
                    "scheduled_at": scheduled_at,
                    "target_concurrency_limit": target_concurrency_limit,
                },
                batch_create_params.BatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    def retrieve(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """
        Retrieves a batch and the current status of each of its recipients.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return self._get(
            path_template("/agents/calls/batches/{batch_id}", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    def list(
        self,
        *,
        agent_id: Optional[str] | Omit = omit,
        ending_before: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorIDPage[CallBatch]:
        """
        List Call Batches

        Args:
          agent_id: Filter to batches for this agent.

          ending_before: (Pagination option) The ID of the batch to end before.

          limit: (Pagination option) The number of batches to return per page, ranging between 1
              and 100.

          starting_after: (Pagination option) The ID of the batch to start after.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/calls/batches",
            page=SyncCursorIDPage[CallBatch],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    batch_list_params.BatchListParams,
                ),
            ),
            model=CallBatch,
        )

    def cancel(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """Stops dialing the batch's queued calls.

        Calls already in flight are left to
        finish. Idempotent.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return self._post(
            path_template("/agents/calls/batches/{batch_id}/cancel", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    def retry(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """
        Re-queues the batch's recipients whose latest call attempt failed or went
        unanswered, so the dispatcher dials them again. Recipients that successfully
        completed their call are left untouched. A cancelled batch cannot be retried.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return self._post(
            path_template("/agents/calls/batches/{batch_id}/retry", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )


class AsyncBatchesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBatchesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBatchesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBatchesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncBatchesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        agent_id: str,
        from_number_id: str,
        name: str,
        recipients: Iterable[batch_create_params.Recipient],
        max_call_duration_minutes: int | Omit = omit,
        region: Literal["US", "EU", "APAC"] | Omit = omit,
        ringing_timeout_seconds: int | Omit = omit,
        scheduled_at: Union[str, datetime] | Omit = omit,
        target_concurrency_limit: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """Queues a batch of outbound calls.

        Calls are issued gradually, subject to the
        organization's and the batch's concurrency limits.

        Args:
          agent_id: The identifier of the agent that handles the batch's calls.

          from_number_id: The identifier of the phone number to place calls from. The attached provider
              handles outbound calling for this number.

          name: A label for the batch.

          recipients: Destinations and optional per-call dynamic variables

          max_call_duration_minutes: Maximum call duration in minutes. Omit to use the default (480 minutes).

          region: The region from which the batch's outbound calls are dispatched. Valid only when
              `from_number_id` is a SIP-trunk number; rejected for other telephony account
              types. Omit to derive the region from the telephony account.

          ringing_timeout_seconds: Seconds to wait for the callee to answer before giving up. Omit to use the
              default (60 seconds).

          scheduled_at: When to start dispatching the batch, as an RFC3339 timestamp with a timezone
              offset (e.g. `2026-06-15T16:00:00Z`). Must be in the future and within 30 days.
              Omit to dispatch immediately.

          target_concurrency_limit: Maximum number of calls from this batch to dial concurrently. Must not exceed
              the organization's concurrency limit. Omit to default to half of the
              organization's agent-call concurrency limit, leaving headroom for other calls.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/calls/batches",
            body=await async_maybe_transform(
                {
                    "agent_id": agent_id,
                    "from_number_id": from_number_id,
                    "name": name,
                    "recipients": recipients,
                    "max_call_duration_minutes": max_call_duration_minutes,
                    "region": region,
                    "ringing_timeout_seconds": ringing_timeout_seconds,
                    "scheduled_at": scheduled_at,
                    "target_concurrency_limit": target_concurrency_limit,
                },
                batch_create_params.BatchCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    async def retrieve(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """
        Retrieves a batch and the current status of each of its recipients.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return await self._get(
            path_template("/agents/calls/batches/{batch_id}", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    def list(
        self,
        *,
        agent_id: Optional[str] | Omit = omit,
        ending_before: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[CallBatch, AsyncCursorIDPage[CallBatch]]:
        """
        List Call Batches

        Args:
          agent_id: Filter to batches for this agent.

          ending_before: (Pagination option) The ID of the batch to end before.

          limit: (Pagination option) The number of batches to return per page, ranging between 1
              and 100.

          starting_after: (Pagination option) The ID of the batch to start after.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/calls/batches",
            page=AsyncCursorIDPage[CallBatch],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    batch_list_params.BatchListParams,
                ),
            ),
            model=CallBatch,
        )

    async def cancel(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """Stops dialing the batch's queued calls.

        Calls already in flight are left to
        finish. Idempotent.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return await self._post(
            path_template("/agents/calls/batches/{batch_id}/cancel", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )

    async def retry(
        self,
        batch_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallBatch:
        """
        Re-queues the batch's recipients whose latest call attempt failed or went
        unanswered, so the dispatcher dials them again. Recipients that successfully
        completed their call are left untouched. A cancelled batch cannot be retried.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not batch_id:
            raise ValueError(f"Expected a non-empty value for `batch_id` but received {batch_id!r}")
        return await self._post(
            path_template("/agents/calls/batches/{batch_id}/retry", batch_id=batch_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallBatch,
        )


class BatchesResourceWithRawResponse:
    def __init__(self, batches: BatchesResource) -> None:
        self._batches = batches

        self.create = to_raw_response_wrapper(
            batches.create,
        )
        self.retrieve = to_raw_response_wrapper(
            batches.retrieve,
        )
        self.list = to_raw_response_wrapper(
            batches.list,
        )
        self.cancel = to_raw_response_wrapper(
            batches.cancel,
        )
        self.retry = to_raw_response_wrapper(
            batches.retry,
        )


class AsyncBatchesResourceWithRawResponse:
    def __init__(self, batches: AsyncBatchesResource) -> None:
        self._batches = batches

        self.create = async_to_raw_response_wrapper(
            batches.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            batches.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            batches.list,
        )
        self.cancel = async_to_raw_response_wrapper(
            batches.cancel,
        )
        self.retry = async_to_raw_response_wrapper(
            batches.retry,
        )


class BatchesResourceWithStreamingResponse:
    def __init__(self, batches: BatchesResource) -> None:
        self._batches = batches

        self.create = to_streamed_response_wrapper(
            batches.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            batches.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            batches.list,
        )
        self.cancel = to_streamed_response_wrapper(
            batches.cancel,
        )
        self.retry = to_streamed_response_wrapper(
            batches.retry,
        )


class AsyncBatchesResourceWithStreamingResponse:
    def __init__(self, batches: AsyncBatchesResource) -> None:
        self._batches = batches

        self.create = async_to_streamed_response_wrapper(
            batches.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            batches.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            batches.list,
        )
        self.cancel = async_to_streamed_response_wrapper(
            batches.cancel,
        )
        self.retry = async_to_streamed_response_wrapper(
            batches.retry,
        )
