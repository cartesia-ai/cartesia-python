# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from ...._utils import path_template, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.agents.knowledge_base import (
    folder_list_params,
    folder_create_params,
    folder_delete_params,
    folder_update_params,
)
from ....types.agents.knowledge_base.folder import Folder
from ....types.agents.knowledge_base.folder_list_response import FolderListResponse

__all__ = ["FoldersResource", "AsyncFoldersResource"]


class FoldersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FoldersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return FoldersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FoldersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return FoldersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        parent_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Create a [knowledge base](/line/knowledge-base) folder

        Args:
          name: A human-readable name for the folder. Must be unique among siblings.

          parent_id: ID of the parent folder. Omit or pass `null` to create a top-level folder.
              Folders can be nested at most three levels deep.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/folders",
            body=maybe_transform(
                {
                    "name": name,
                    "parent_id": parent_id,
                },
                folder_create_params.FolderCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Folder,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Returns the details of a single [knowledge base](/line/knowledge-base) folder,
        including its documents and agents that have access to it

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            path_template("/agents/folders/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Folder,
        )

    def update(
        self,
        id: str,
        *,
        force: Literal["true", "false"] | Omit = omit,
        agents: Iterable[folder_update_params.Agent] | Omit = omit,
        documents: Iterable[folder_update_params.Document] | Omit = omit,
        name: str | Omit = omit,
        parent_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Update a [knowledge base](/line/knowledge-base) folder's name, parent,
        documents, or agents

        Args:
          force: Delete the documents left out of `documents` even if agents can search them.
              Agents linked to them stop using them.

          agents: The complete set of agents that have access to this folder. Agents not in the
              list have their access revoked. Pass an empty array to revoke access for all
              agents.

          documents: The complete set of documents that should be in this folder. Documents not in
              the list are deleted. Pass an empty array to delete all documents in the folder.

          name: A new name for the folder. Must be unique among siblings.

          parent_id: Move the folder under a new parent, or `null` to move it to the top level.
              Cannot create a circular reference.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            path_template("/agents/folders/{id}", id=id),
            body=maybe_transform(
                {
                    "agents": agents,
                    "documents": documents,
                    "name": name,
                    "parent_id": parent_id,
                },
                folder_update_params.FolderUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"force": force}, folder_update_params.FolderUpdateParams),
            ),
            cast_to=Folder,
        )

    def list(
        self,
        *,
        depth: int | Omit = omit,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        parent_ids: SequenceNotStr[str] | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FolderListResponse:
        """
        List [knowledge base](/line/knowledge-base) folders

        Args:
          depth: How many levels of nested children to include in the response, between 1 and 3.
              Defaults to 3.

          ending_before: A cursor for pagination. Pass the ID of the first folder from the previous page
              to fetch the previous page.

          limit: The number of folders to return per page, ranging between 1 and 100. Defaults
              to 10. Pagination applies to the top-level folders in the response; nested
              children do not count against this limit.

          parent_ids: Filter to folders with these parent IDs. Repeat the parameter to pass multiple
              values (e.g., `?parent_ids[]=folder_abc&parent_ids[]=null`). Pass the literal
              string `null` to include top-level folders. Defaults to `[null]` (top-level
              folders only).

          starting_after: A cursor for pagination. Pass the ID of the last folder from the previous page
              to fetch the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/agents/folders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "depth": depth,
                        "ending_before": ending_before,
                        "limit": limit,
                        "parent_ids": parent_ids,
                        "starting_after": starting_after,
                    },
                    folder_list_params.FolderListParams,
                ),
            ),
            cast_to=FolderListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        force: Literal["true", "false"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a [knowledge base](/line/knowledge-base) folder

        Args:
          force: Delete the folder even if it has subfolders or agents can search it. Its
              subfolders and documents are deleted too, and agents linked to any of them stop
              using them.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/agents/folders/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"force": force}, folder_delete_params.FolderDeleteParams),
            ),
            cast_to=NoneType,
        )


class AsyncFoldersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFoldersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFoldersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFoldersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncFoldersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        parent_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Create a [knowledge base](/line/knowledge-base) folder

        Args:
          name: A human-readable name for the folder. Must be unique among siblings.

          parent_id: ID of the parent folder. Omit or pass `null` to create a top-level folder.
              Folders can be nested at most three levels deep.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/folders",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "parent_id": parent_id,
                },
                folder_create_params.FolderCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Folder,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Returns the details of a single [knowledge base](/line/knowledge-base) folder,
        including its documents and agents that have access to it

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            path_template("/agents/folders/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Folder,
        )

    async def update(
        self,
        id: str,
        *,
        force: Literal["true", "false"] | Omit = omit,
        agents: Iterable[folder_update_params.Agent] | Omit = omit,
        documents: Iterable[folder_update_params.Document] | Omit = omit,
        name: str | Omit = omit,
        parent_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Folder:
        """
        Update a [knowledge base](/line/knowledge-base) folder's name, parent,
        documents, or agents

        Args:
          force: Delete the documents left out of `documents` even if agents can search them.
              Agents linked to them stop using them.

          agents: The complete set of agents that have access to this folder. Agents not in the
              list have their access revoked. Pass an empty array to revoke access for all
              agents.

          documents: The complete set of documents that should be in this folder. Documents not in
              the list are deleted. Pass an empty array to delete all documents in the folder.

          name: A new name for the folder. Must be unique among siblings.

          parent_id: Move the folder under a new parent, or `null` to move it to the top level.
              Cannot create a circular reference.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            path_template("/agents/folders/{id}", id=id),
            body=await async_maybe_transform(
                {
                    "agents": agents,
                    "documents": documents,
                    "name": name,
                    "parent_id": parent_id,
                },
                folder_update_params.FolderUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"force": force}, folder_update_params.FolderUpdateParams),
            ),
            cast_to=Folder,
        )

    async def list(
        self,
        *,
        depth: int | Omit = omit,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        parent_ids: SequenceNotStr[str] | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> FolderListResponse:
        """
        List [knowledge base](/line/knowledge-base) folders

        Args:
          depth: How many levels of nested children to include in the response, between 1 and 3.
              Defaults to 3.

          ending_before: A cursor for pagination. Pass the ID of the first folder from the previous page
              to fetch the previous page.

          limit: The number of folders to return per page, ranging between 1 and 100. Defaults
              to 10. Pagination applies to the top-level folders in the response; nested
              children do not count against this limit.

          parent_ids: Filter to folders with these parent IDs. Repeat the parameter to pass multiple
              values (e.g., `?parent_ids[]=folder_abc&parent_ids[]=null`). Pass the literal
              string `null` to include top-level folders. Defaults to `[null]` (top-level
              folders only).

          starting_after: A cursor for pagination. Pass the ID of the last folder from the previous page
              to fetch the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/agents/folders",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "depth": depth,
                        "ending_before": ending_before,
                        "limit": limit,
                        "parent_ids": parent_ids,
                        "starting_after": starting_after,
                    },
                    folder_list_params.FolderListParams,
                ),
            ),
            cast_to=FolderListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        force: Literal["true", "false"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Delete a [knowledge base](/line/knowledge-base) folder

        Args:
          force: Delete the folder even if it has subfolders or agents can search it. Its
              subfolders and documents are deleted too, and agents linked to any of them stop
              using them.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/agents/folders/{id}", id=id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"force": force}, folder_delete_params.FolderDeleteParams),
            ),
            cast_to=NoneType,
        )


class FoldersResourceWithRawResponse:
    def __init__(self, folders: FoldersResource) -> None:
        self._folders = folders

        self.create = to_raw_response_wrapper(
            folders.create,
        )
        self.retrieve = to_raw_response_wrapper(
            folders.retrieve,
        )
        self.update = to_raw_response_wrapper(
            folders.update,
        )
        self.list = to_raw_response_wrapper(
            folders.list,
        )
        self.delete = to_raw_response_wrapper(
            folders.delete,
        )


class AsyncFoldersResourceWithRawResponse:
    def __init__(self, folders: AsyncFoldersResource) -> None:
        self._folders = folders

        self.create = async_to_raw_response_wrapper(
            folders.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            folders.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            folders.update,
        )
        self.list = async_to_raw_response_wrapper(
            folders.list,
        )
        self.delete = async_to_raw_response_wrapper(
            folders.delete,
        )


class FoldersResourceWithStreamingResponse:
    def __init__(self, folders: FoldersResource) -> None:
        self._folders = folders

        self.create = to_streamed_response_wrapper(
            folders.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            folders.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            folders.update,
        )
        self.list = to_streamed_response_wrapper(
            folders.list,
        )
        self.delete = to_streamed_response_wrapper(
            folders.delete,
        )


class AsyncFoldersResourceWithStreamingResponse:
    def __init__(self, folders: AsyncFoldersResource) -> None:
        self._folders = folders

        self.create = async_to_streamed_response_wrapper(
            folders.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            folders.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            folders.update,
        )
        self.list = async_to_streamed_response_wrapper(
            folders.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            folders.delete,
        )
