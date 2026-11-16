# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, List, Iterable, Optional, cast
from typing_extensions import Literal, overload

import httpx

from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
from ..._utils import path_template, required_args, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.agents import tool_list_params, tool_create_params, tool_update_params, tool_retrieve_params
from ...types.agents.tool import Tool
from ...types.agents.tool_list_response import ToolListResponse

__all__ = ["ToolsResource", "AsyncToolsResource"]


class ToolsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return ToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return ToolsResourceWithStreamingResponse(self)

    @overload
    def create(
        self,
        *,
        api_schema: tool_create_params.Variant0APISchema,
        description: str,
        execution_mode: Literal["immediate", "async"],
        name: str,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["webhook"],
        assignments: Iterable[tool_create_params.Variant0Assignment] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Creates a shared webhook or client tool that can be attached to agents

        Args:
          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          type: Runs an HTTP request from Cartesia's servers.

          assignments: Configure how to extract values from successful JSON tool responses and assign
              them to dynamic variables for this call.

          response_timeout_secs: Maximum time to wait for the endpoint to respond. Defaults to 20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def create(
        self,
        *,
        description: str,
        execution_mode: Literal["immediate", "async"],
        expects_response: bool,
        name: str,
        parameters: tool_create_params.Variant1Parameters,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["client"],
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Creates a shared webhook or client tool that can be attached to agents

        Args:
          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          expects_response: Whether the client application must return a result. When `false`, the tool call
              is dispatched without waiting for a result.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          parameters: Parameters the agent can pass to the client function.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          type: Runs a function in the connected client application.

          response_timeout_secs: Maximum time to wait for the client application to return a result. Defaults to
              20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["api_schema", "description", "execution_mode", "name", "pre_tool_speech", "type"],
        ["description", "execution_mode", "expects_response", "name", "parameters", "pre_tool_speech", "type"],
    )
    def create(
        self,
        *,
        api_schema: tool_create_params.Variant0APISchema | Omit = omit,
        description: str,
        execution_mode: Literal["immediate", "async"],
        name: str,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["webhook"] | Literal["client"],
        assignments: Iterable[tool_create_params.Variant0Assignment] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        expects_response: bool | Omit = omit,
        parameters: tool_create_params.Variant1Parameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        return cast(
            Tool,
            self._post(
                "/v1/agents/tools",
                body=maybe_transform(
                    {
                        "api_schema": api_schema,
                        "description": description,
                        "execution_mode": execution_mode,
                        "name": name,
                        "pre_tool_speech": pre_tool_speech,
                        "type": type,
                        "assignments": assignments,
                        "response_timeout_secs": response_timeout_secs,
                        "expects_response": expects_response,
                        "parameters": parameters,
                    },
                    tool_create_params.ToolCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def retrieve(
        self,
        tool_id: str,
        *,
        expand: List[Literal["agents"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """Returns one shared tool.

        Expand `agents` to include agents that currently
        reference it.

        Args:
          tool_id: Unique identifier for the tool.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        return cast(
            Tool,
            self._get(
                path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=maybe_transform({"expand": expand}, tool_retrieve_params.ToolRetrieveParams),
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    def update(
        self,
        tool_id: str,
        *,
        api_schema: tool_update_params.Variant0APISchema | Omit = omit,
        assignments: Optional[Iterable[tool_update_params.Variant0Assignment]] | Omit = omit,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        name: str | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Sparsely updates a tool.

        Args:
          tool_id: Unique identifier for the tool.

          assignments: Replace the response assignments. Omit to keep them, or use `null` or `[]` to
              clear them.

          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          response_timeout_secs: Maximum time to wait for the endpoint to respond. Defaults to 20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        tool_id: str,
        *,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        expects_response: bool | Omit = omit,
        name: str | Omit = omit,
        parameters: tool_update_params.Variant1Parameters | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Sparsely updates a tool.

        Args:
          tool_id: Unique identifier for the tool.

          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          expects_response: Whether the client application must return a result. When `false`, the tool call
              is dispatched without waiting for a result.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          parameters: Parameters the agent can pass to the client function.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          response_timeout_secs: Maximum time to wait for the client application to return a result. Defaults to
              20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    def update(
        self,
        tool_id: str,
        *,
        api_schema: tool_update_params.Variant0APISchema | Omit = omit,
        assignments: Optional[Iterable[tool_update_params.Variant0Assignment]] | Omit = omit,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        name: str | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        expects_response: bool | Omit = omit,
        parameters: tool_update_params.Variant1Parameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        return cast(
            Tool,
            self._patch(
                path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
                body=maybe_transform(
                    {
                        "api_schema": api_schema,
                        "assignments": assignments,
                        "description": description,
                        "execution_mode": execution_mode,
                        "name": name,
                        "pre_tool_speech": pre_tool_speech,
                        "response_timeout_secs": response_timeout_secs,
                        "expects_response": expects_response,
                        "parameters": parameters,
                    },
                    tool_update_params.ToolUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    def list(
        self,
        *,
        agent_id: str | Omit = omit,
        ending_before: str | Omit = omit,
        expand: List[Literal["agents"]] | Omit = omit,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        type: Literal["webhook", "client"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ToolListResponse:
        """
        Returns shared webhook and client tools for your account

        Args:
          agent_id: Return only tools used by this agent.

          ending_before: A cursor for pagination. Pass the ID of the first item from the previous page to
              fetch the previous page.

          expand: Related resources to include in each tool. `agents` lists the agents that use
              it.

          limit: The maximum number of items to return, ranging between 1 and 100.

          starting_after: A cursor for pagination. Pass the ID of the last item from the previous page to
              fetch the next page.

          type: Return only tools of this type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/agents/tools",
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
                        "type": type,
                    },
                    tool_list_params.ToolListParams,
                ),
            ),
            cast_to=ToolListResponse,
        )

    def delete(
        self,
        tool_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Deletes an unused tool.

        Detach the tool from current agent configurations first.

        Args:
          tool_id: Unique identifier for the tool.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncToolsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncToolsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncToolsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncToolsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncToolsResourceWithStreamingResponse(self)

    @overload
    async def create(
        self,
        *,
        api_schema: tool_create_params.Variant0APISchema,
        description: str,
        execution_mode: Literal["immediate", "async"],
        name: str,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["webhook"],
        assignments: Iterable[tool_create_params.Variant0Assignment] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Creates a shared webhook or client tool that can be attached to agents

        Args:
          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          type: Runs an HTTP request from Cartesia's servers.

          assignments: Configure how to extract values from successful JSON tool responses and assign
              them to dynamic variables for this call.

          response_timeout_secs: Maximum time to wait for the endpoint to respond. Defaults to 20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def create(
        self,
        *,
        description: str,
        execution_mode: Literal["immediate", "async"],
        expects_response: bool,
        name: str,
        parameters: tool_create_params.Variant1Parameters,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["client"],
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Creates a shared webhook or client tool that can be attached to agents

        Args:
          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          expects_response: Whether the client application must return a result. When `false`, the tool call
              is dispatched without waiting for a result.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          parameters: Parameters the agent can pass to the client function.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          type: Runs a function in the connected client application.

          response_timeout_secs: Maximum time to wait for the client application to return a result. Defaults to
              20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(
        ["api_schema", "description", "execution_mode", "name", "pre_tool_speech", "type"],
        ["description", "execution_mode", "expects_response", "name", "parameters", "pre_tool_speech", "type"],
    )
    async def create(
        self,
        *,
        api_schema: tool_create_params.Variant0APISchema | Omit = omit,
        description: str,
        execution_mode: Literal["immediate", "async"],
        name: str,
        pre_tool_speech: Literal["auto", "force", "off"],
        type: Literal["webhook"] | Literal["client"],
        assignments: Iterable[tool_create_params.Variant0Assignment] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        expects_response: bool | Omit = omit,
        parameters: tool_create_params.Variant1Parameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        return cast(
            Tool,
            await self._post(
                "/v1/agents/tools",
                body=await async_maybe_transform(
                    {
                        "api_schema": api_schema,
                        "description": description,
                        "execution_mode": execution_mode,
                        "name": name,
                        "pre_tool_speech": pre_tool_speech,
                        "type": type,
                        "assignments": assignments,
                        "response_timeout_secs": response_timeout_secs,
                        "expects_response": expects_response,
                        "parameters": parameters,
                    },
                    tool_create_params.ToolCreateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def retrieve(
        self,
        tool_id: str,
        *,
        expand: List[Literal["agents"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """Returns one shared tool.

        Expand `agents` to include agents that currently
        reference it.

        Args:
          tool_id: Unique identifier for the tool.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        return cast(
            Tool,
            await self._get(
                path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
                options=make_request_options(
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    query=await async_maybe_transform({"expand": expand}, tool_retrieve_params.ToolRetrieveParams),
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    @overload
    async def update(
        self,
        tool_id: str,
        *,
        api_schema: tool_update_params.Variant0APISchema | Omit = omit,
        assignments: Optional[Iterable[tool_update_params.Variant0Assignment]] | Omit = omit,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        name: str | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Sparsely updates a tool.

        Args:
          tool_id: Unique identifier for the tool.

          assignments: Replace the response assignments. Omit to keep them, or use `null` or `[]` to
              clear them.

          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          response_timeout_secs: Maximum time to wait for the endpoint to respond. Defaults to 20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        tool_id: str,
        *,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        expects_response: bool | Omit = omit,
        name: str | Omit = omit,
        parameters: tool_update_params.Variant1Parameters | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        """
        Sparsely updates a tool.

        Args:
          tool_id: Unique identifier for the tool.

          description: What the tool does and when the agent should use it.

          execution_mode: Controls how the tool runs relative to the conversation. `immediate` runs it in
              the current turn, while `async` lets the turn finish while the tool runs.

          expects_response: Whether the client application must return a result. When `false`, the tool call
              is dispatched without waiting for a result.

          name: Name the agent uses to call the tool. Names are case-sensitive.

          parameters: Parameters the agent can pass to the client function.

          pre_tool_speech: Controls whether the agent speaks before using the tool. `auto` lets the agent
              decide, `force` always makes the agent speak first, and `off` never asks it to.

          response_timeout_secs: Maximum time to wait for the client application to return a result. Defaults to
              20 seconds.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    async def update(
        self,
        tool_id: str,
        *,
        api_schema: tool_update_params.Variant0APISchema | Omit = omit,
        assignments: Optional[Iterable[tool_update_params.Variant0Assignment]] | Omit = omit,
        description: str | Omit = omit,
        execution_mode: Literal["immediate", "async"] | Omit = omit,
        name: str | Omit = omit,
        pre_tool_speech: Literal["auto", "force", "off"] | Omit = omit,
        response_timeout_secs: int | Omit = omit,
        expects_response: bool | Omit = omit,
        parameters: tool_update_params.Variant1Parameters | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Tool:
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        return cast(
            Tool,
            await self._patch(
                path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
                body=await async_maybe_transform(
                    {
                        "api_schema": api_schema,
                        "assignments": assignments,
                        "description": description,
                        "execution_mode": execution_mode,
                        "name": name,
                        "pre_tool_speech": pre_tool_speech,
                        "response_timeout_secs": response_timeout_secs,
                        "expects_response": expects_response,
                        "parameters": parameters,
                    },
                    tool_update_params.ToolUpdateParams,
                ),
                options=make_request_options(
                    extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
                ),
                cast_to=cast(Any, Tool),  # Union types cannot be passed in as arguments in the type system
            ),
        )

    async def list(
        self,
        *,
        agent_id: str | Omit = omit,
        ending_before: str | Omit = omit,
        expand: List[Literal["agents"]] | Omit = omit,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        type: Literal["webhook", "client"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ToolListResponse:
        """
        Returns shared webhook and client tools for your account

        Args:
          agent_id: Return only tools used by this agent.

          ending_before: A cursor for pagination. Pass the ID of the first item from the previous page to
              fetch the previous page.

          expand: Related resources to include in each tool. `agents` lists the agents that use
              it.

          limit: The maximum number of items to return, ranging between 1 and 100.

          starting_after: A cursor for pagination. Pass the ID of the last item from the previous page to
              fetch the next page.

          type: Return only tools of this type.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/agents/tools",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "agent_id": agent_id,
                        "ending_before": ending_before,
                        "expand": expand,
                        "limit": limit,
                        "starting_after": starting_after,
                        "type": type,
                    },
                    tool_list_params.ToolListParams,
                ),
            ),
            cast_to=ToolListResponse,
        )

    async def delete(
        self,
        tool_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Deletes an unused tool.

        Detach the tool from current agent configurations first.

        Args:
          tool_id: Unique identifier for the tool.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not tool_id:
            raise ValueError(f"Expected a non-empty value for `tool_id` but received {tool_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/v1/agents/tools/{tool_id}", tool_id=tool_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ToolsResourceWithRawResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.create = to_raw_response_wrapper(
            tools.create,
        )
        self.retrieve = to_raw_response_wrapper(
            tools.retrieve,
        )
        self.update = to_raw_response_wrapper(
            tools.update,
        )
        self.list = to_raw_response_wrapper(
            tools.list,
        )
        self.delete = to_raw_response_wrapper(
            tools.delete,
        )


class AsyncToolsResourceWithRawResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.create = async_to_raw_response_wrapper(
            tools.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            tools.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            tools.update,
        )
        self.list = async_to_raw_response_wrapper(
            tools.list,
        )
        self.delete = async_to_raw_response_wrapper(
            tools.delete,
        )


class ToolsResourceWithStreamingResponse:
    def __init__(self, tools: ToolsResource) -> None:
        self._tools = tools

        self.create = to_streamed_response_wrapper(
            tools.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            tools.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            tools.update,
        )
        self.list = to_streamed_response_wrapper(
            tools.list,
        )
        self.delete = to_streamed_response_wrapper(
            tools.delete,
        )


class AsyncToolsResourceWithStreamingResponse:
    def __init__(self, tools: AsyncToolsResource) -> None:
        self._tools = tools

        self.create = async_to_streamed_response_wrapper(
            tools.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            tools.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            tools.update,
        )
        self.list = async_to_streamed_response_wrapper(
            tools.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            tools.delete,
        )
