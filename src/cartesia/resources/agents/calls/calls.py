# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from .batches import (
    BatchesResource,
    AsyncBatchesResource,
    BatchesResourceWithRawResponse,
    AsyncBatchesResourceWithRawResponse,
    BatchesResourceWithStreamingResponse,
    AsyncBatchesResourceWithStreamingResponse,
)
from ...._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ....pagination import SyncCursorIDPage, AsyncCursorIDPage
from ...._base_client import AsyncPaginator, make_request_options
from ....types.agents import call_list_params, call_create_params
from ....types.agents.agent_call import AgentCall
from ....types.agents.call_logs_response import CallLogsResponse
from ....types.agents.call_cancel_response import CallCancelResponse
from ....types.agents.call_create_response import CallCreateResponse

__all__ = ["CallsResource", "AsyncCallsResource"]


class CallsResource(SyncAPIResource):
    @cached_property
    def batches(self) -> BatchesResource:
        return BatchesResource(self._client)

    @cached_property
    def with_raw_response(self) -> CallsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return CallsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CallsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return CallsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        agent_id: str,
        from_number_id: str,
        outbound_calls: Iterable[call_create_params.OutboundCall],
        max_call_duration_minutes: int | Omit = omit,
        ringing_timeout_seconds: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallCreateResponse:
        """
        Create Outbound Call

        Args:
          agent_id: Agent that handles the outbound calls.

          from_number_id: Phone number ID to place calls from. The attached provider handles outbound
              calling for this number.

          outbound_calls: Destinations and optional per-call dynamic variables

          max_call_duration_minutes: Optional maximum call duration in minutes.

          ringing_timeout_seconds: Seconds to wait for the callee to answer before giving up. Omit to use the
              default (60 seconds).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/calls",
            body=maybe_transform(
                {
                    "agent_id": agent_id,
                    "from_number_id": from_number_id,
                    "outbound_calls": outbound_calls,
                    "max_call_duration_minutes": max_call_duration_minutes,
                    "ringing_timeout_seconds": ringing_timeout_seconds,
                },
                call_create_params.CallCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallCreateResponse,
        )

    def retrieve(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentCall:
        """
        Get Call

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return self._get(
            path_template("/agents/calls/{call_id}", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentCall,
        )

    def list(
        self,
        *,
        agent_id: str,
        ending_before: Optional[str] | Omit = omit,
        expand: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorIDPage[AgentCall]:
        """
        Lists calls sorted by start time in descending order for a specific agent.
        `agent_id` is required and if you want to include `transcript` in the response,
        add `expand=transcript` to the request. This endpoint is paginated.

        Args:
          agent_id: The ID of the agent.

          ending_before: (Pagination option) The ID of the call to end before.

          expand: The fields to expand in the response. Currently, the only supported value is
              `transcript`.

          limit: (Pagination option) The number of calls to return per page, ranging between 1
              and 100.

          starting_after: (Pagination option)The ID of the call to start after.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/calls",
            page=SyncCursorIDPage[AgentCall],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "expand": expand,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    call_list_params.CallListParams,
                ),
            ),
            model=AgentCall,
        )

    def delete(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentCall:
        """
        Deletes the sensitive data for a call, including the transcript, audio
        recordings, and logs. The call record is retained with non-sensitive operational
        metadata; deleted fields are omitted from subsequent API responses, and
        `redacted_at` marks when deletion occurred. Deletion cannot be undone.

        Only completed or failed calls can be deleted. Cancel an active call first via
        `POST /agents/calls/{call_id}/cancel`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return self._delete(
            path_template("/agents/calls/{call_id}", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentCall,
        )

    def cancel(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallCancelResponse:
        """Terminates an active call.

        Only calls in the `started` status can be cancelled;
        the call ends with end reason `api_cancelled`.

        Cancelling ends the call but does not delete its data. To delete a call's
        sensitive data after it ends, use `DELETE /agents/calls/{call_id}`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return self._post(
            path_template("/agents/calls/{call_id}/cancel", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallCancelResponse,
        )

    def download_audio(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """The downloaded audio file is in .wav format.

        This endpoint streams the audio
        file content (WAV format) to the client.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        return self._get(
            path_template("/agents/calls/{call_id}/audio", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def logs(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallLogsResponse:
        """
        Get Call Runtime Logs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return self._get(
            path_template("/agents/calls/{call_id}/logs", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallLogsResponse,
        )


class AsyncCallsResource(AsyncAPIResource):
    @cached_property
    def batches(self) -> AsyncBatchesResource:
        return AsyncBatchesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCallsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCallsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCallsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncCallsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        agent_id: str,
        from_number_id: str,
        outbound_calls: Iterable[call_create_params.OutboundCall],
        max_call_duration_minutes: int | Omit = omit,
        ringing_timeout_seconds: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallCreateResponse:
        """
        Create Outbound Call

        Args:
          agent_id: Agent that handles the outbound calls.

          from_number_id: Phone number ID to place calls from. The attached provider handles outbound
              calling for this number.

          outbound_calls: Destinations and optional per-call dynamic variables

          max_call_duration_minutes: Optional maximum call duration in minutes.

          ringing_timeout_seconds: Seconds to wait for the callee to answer before giving up. Omit to use the
              default (60 seconds).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/calls",
            body=await async_maybe_transform(
                {
                    "agent_id": agent_id,
                    "from_number_id": from_number_id,
                    "outbound_calls": outbound_calls,
                    "max_call_duration_minutes": max_call_duration_minutes,
                    "ringing_timeout_seconds": ringing_timeout_seconds,
                },
                call_create_params.CallCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallCreateResponse,
        )

    async def retrieve(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentCall:
        """
        Get Call

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return await self._get(
            path_template("/agents/calls/{call_id}", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentCall,
        )

    def list(
        self,
        *,
        agent_id: str,
        ending_before: Optional[str] | Omit = omit,
        expand: Optional[str] | Omit = omit,
        limit: Optional[int] | Omit = omit,
        starting_after: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[AgentCall, AsyncCursorIDPage[AgentCall]]:
        """
        Lists calls sorted by start time in descending order for a specific agent.
        `agent_id` is required and if you want to include `transcript` in the response,
        add `expand=transcript` to the request. This endpoint is paginated.

        Args:
          agent_id: The ID of the agent.

          ending_before: (Pagination option) The ID of the call to end before.

          expand: The fields to expand in the response. Currently, the only supported value is
              `transcript`.

          limit: (Pagination option) The number of calls to return per page, ranging between 1
              and 100.

          starting_after: (Pagination option)The ID of the call to start after.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/calls",
            page=AsyncCursorIDPage[AgentCall],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "expand": expand,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    call_list_params.CallListParams,
                ),
            ),
            model=AgentCall,
        )

    async def delete(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AgentCall:
        """
        Deletes the sensitive data for a call, including the transcript, audio
        recordings, and logs. The call record is retained with non-sensitive operational
        metadata; deleted fields are omitted from subsequent API responses, and
        `redacted_at` marks when deletion occurred. Deletion cannot be undone.

        Only completed or failed calls can be deleted. Cancel an active call first via
        `POST /agents/calls/{call_id}/cancel`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return await self._delete(
            path_template("/agents/calls/{call_id}", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AgentCall,
        )

    async def cancel(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallCancelResponse:
        """Terminates an active call.

        Only calls in the `started` status can be cancelled;
        the call ends with end reason `api_cancelled`.

        Cancelling ends the call but does not delete its data. To delete a call's
        sensitive data after it ends, use `DELETE /agents/calls/{call_id}`.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return await self._post(
            path_template("/agents/calls/{call_id}/cancel", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallCancelResponse,
        )

    async def download_audio(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """The downloaded audio file is in .wav format.

        This endpoint streams the audio
        file content (WAV format) to the client.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        return await self._get(
            path_template("/agents/calls/{call_id}/audio", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def logs(
        self,
        call_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CallLogsResponse:
        """
        Get Call Runtime Logs

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not call_id:
            raise ValueError(f"Expected a non-empty value for `call_id` but received {call_id!r}")
        return await self._get(
            path_template("/agents/calls/{call_id}/logs", call_id=call_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CallLogsResponse,
        )


class CallsResourceWithRawResponse:
    def __init__(self, calls: CallsResource) -> None:
        self._calls = calls

        self.create = to_raw_response_wrapper(
            calls.create,
        )
        self.retrieve = to_raw_response_wrapper(
            calls.retrieve,
        )
        self.list = to_raw_response_wrapper(
            calls.list,
        )
        self.delete = to_raw_response_wrapper(
            calls.delete,
        )
        self.cancel = to_raw_response_wrapper(
            calls.cancel,
        )
        self.download_audio = to_custom_raw_response_wrapper(
            calls.download_audio,
            BinaryAPIResponse,
        )
        self.logs = to_raw_response_wrapper(
            calls.logs,
        )

    @cached_property
    def batches(self) -> BatchesResourceWithRawResponse:
        return BatchesResourceWithRawResponse(self._calls.batches)


class AsyncCallsResourceWithRawResponse:
    def __init__(self, calls: AsyncCallsResource) -> None:
        self._calls = calls

        self.create = async_to_raw_response_wrapper(
            calls.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            calls.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            calls.list,
        )
        self.delete = async_to_raw_response_wrapper(
            calls.delete,
        )
        self.cancel = async_to_raw_response_wrapper(
            calls.cancel,
        )
        self.download_audio = async_to_custom_raw_response_wrapper(
            calls.download_audio,
            AsyncBinaryAPIResponse,
        )
        self.logs = async_to_raw_response_wrapper(
            calls.logs,
        )

    @cached_property
    def batches(self) -> AsyncBatchesResourceWithRawResponse:
        return AsyncBatchesResourceWithRawResponse(self._calls.batches)


class CallsResourceWithStreamingResponse:
    def __init__(self, calls: CallsResource) -> None:
        self._calls = calls

        self.create = to_streamed_response_wrapper(
            calls.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            calls.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            calls.list,
        )
        self.delete = to_streamed_response_wrapper(
            calls.delete,
        )
        self.cancel = to_streamed_response_wrapper(
            calls.cancel,
        )
        self.download_audio = to_custom_streamed_response_wrapper(
            calls.download_audio,
            StreamedBinaryAPIResponse,
        )
        self.logs = to_streamed_response_wrapper(
            calls.logs,
        )

    @cached_property
    def batches(self) -> BatchesResourceWithStreamingResponse:
        return BatchesResourceWithStreamingResponse(self._calls.batches)


class AsyncCallsResourceWithStreamingResponse:
    def __init__(self, calls: AsyncCallsResource) -> None:
        self._calls = calls

        self.create = async_to_streamed_response_wrapper(
            calls.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            calls.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            calls.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            calls.delete,
        )
        self.cancel = async_to_streamed_response_wrapper(
            calls.cancel,
        )
        self.download_audio = async_to_custom_streamed_response_wrapper(
            calls.download_audio,
            AsyncStreamedBinaryAPIResponse,
        )
        self.logs = async_to_streamed_response_wrapper(
            calls.logs,
        )

    @cached_property
    def batches(self) -> AsyncBatchesResourceWithStreamingResponse:
        return AsyncBatchesResourceWithStreamingResponse(self._calls.batches)
