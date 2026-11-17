# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.agents import session_create_webrtc_params, session_create_websocket_params
from ...types.agents.session_create_webrtc_response import SessionCreateWebrtcResponse
from ...types.agents.session_create_websocket_response import SessionCreateWebsocketResponse

__all__ = ["SessionsResource", "AsyncSessionsResource"]


class SessionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return SessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return SessionsResourceWithStreamingResponse(self)

    def create_webrtc(
        self,
        agent_id: str,
        *,
        config_overrides: session_create_webrtc_params.ConfigOverrides | Omit = omit,
        dynamic_variables: Dict[str, Union[str, float, bool]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCreateWebrtcResponse:
        """
        Creates a WebRTC session on your trusted server and returns credentials for the
        browser to join. Authenticate this request with an API key; access tokens,
        including returned session tokens, cannot create sessions.

        Args:
          config_overrides: Per-call overrides using the same field structure as agent configuration.
              Omitted fields use the agent's published configuration.

          dynamic_variables: Trusted values that Cartesia stores on the call and supplies to the agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            path_template("/v1/agents/webrtc/{agent_id}/sessions", agent_id=agent_id),
            body=maybe_transform(
                {
                    "config_overrides": config_overrides,
                    "dynamic_variables": dynamic_variables,
                },
                session_create_webrtc_params.SessionCreateWebrtcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateWebrtcResponse,
        )

    def create_websocket(
        self,
        agent_id: str,
        *,
        config_overrides: session_create_websocket_params.ConfigOverrides | Omit = omit,
        dynamic_variables: Dict[str, Union[str, float, bool]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCreateWebsocketResponse:
        """
        Creates a call-bound WebSocket session on your trusted server and returns a
        session token for the browser to connect. Authenticate this request with an API
        key; access tokens, including returned session tokens, cannot create sessions.

        Args:
          config_overrides: Per-call overrides using the same field structure as agent configuration.
              Omitted fields use the agent's published configuration.

          dynamic_variables: Trusted values that Cartesia stores on the call and supplies to the agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return self._post(
            path_template("/v1/agents/websocket/{agent_id}/sessions", agent_id=agent_id),
            body=maybe_transform(
                {
                    "config_overrides": config_overrides,
                    "dynamic_variables": dynamic_variables,
                },
                session_create_websocket_params.SessionCreateWebsocketParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateWebsocketResponse,
        )


class AsyncSessionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncSessionsResourceWithStreamingResponse(self)

    async def create_webrtc(
        self,
        agent_id: str,
        *,
        config_overrides: session_create_webrtc_params.ConfigOverrides | Omit = omit,
        dynamic_variables: Dict[str, Union[str, float, bool]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCreateWebrtcResponse:
        """
        Creates a WebRTC session on your trusted server and returns credentials for the
        browser to join. Authenticate this request with an API key; access tokens,
        including returned session tokens, cannot create sessions.

        Args:
          config_overrides: Per-call overrides using the same field structure as agent configuration.
              Omitted fields use the agent's published configuration.

          dynamic_variables: Trusted values that Cartesia stores on the call and supplies to the agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            path_template("/v1/agents/webrtc/{agent_id}/sessions", agent_id=agent_id),
            body=await async_maybe_transform(
                {
                    "config_overrides": config_overrides,
                    "dynamic_variables": dynamic_variables,
                },
                session_create_webrtc_params.SessionCreateWebrtcParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateWebrtcResponse,
        )

    async def create_websocket(
        self,
        agent_id: str,
        *,
        config_overrides: session_create_websocket_params.ConfigOverrides | Omit = omit,
        dynamic_variables: Dict[str, Union[str, float, bool]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SessionCreateWebsocketResponse:
        """
        Creates a call-bound WebSocket session on your trusted server and returns a
        session token for the browser to connect. Authenticate this request with an API
        key; access tokens, including returned session tokens, cannot create sessions.

        Args:
          config_overrides: Per-call overrides using the same field structure as agent configuration.
              Omitted fields use the agent's published configuration.

          dynamic_variables: Trusted values that Cartesia stores on the call and supplies to the agent.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not agent_id:
            raise ValueError(f"Expected a non-empty value for `agent_id` but received {agent_id!r}")
        return await self._post(
            path_template("/v1/agents/websocket/{agent_id}/sessions", agent_id=agent_id),
            body=await async_maybe_transform(
                {
                    "config_overrides": config_overrides,
                    "dynamic_variables": dynamic_variables,
                },
                session_create_websocket_params.SessionCreateWebsocketParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SessionCreateWebsocketResponse,
        )


class SessionsResourceWithRawResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create_webrtc = to_raw_response_wrapper(
            sessions.create_webrtc,
        )
        self.create_websocket = to_raw_response_wrapper(
            sessions.create_websocket,
        )


class AsyncSessionsResourceWithRawResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create_webrtc = async_to_raw_response_wrapper(
            sessions.create_webrtc,
        )
        self.create_websocket = async_to_raw_response_wrapper(
            sessions.create_websocket,
        )


class SessionsResourceWithStreamingResponse:
    def __init__(self, sessions: SessionsResource) -> None:
        self._sessions = sessions

        self.create_webrtc = to_streamed_response_wrapper(
            sessions.create_webrtc,
        )
        self.create_websocket = to_streamed_response_wrapper(
            sessions.create_websocket,
        )


class AsyncSessionsResourceWithStreamingResponse:
    def __init__(self, sessions: AsyncSessionsResource) -> None:
        self._sessions = sessions

        self.create_webrtc = async_to_streamed_response_wrapper(
            sessions.create_webrtc,
        )
        self.create_websocket = async_to_streamed_response_wrapper(
            sessions.create_websocket,
        )
