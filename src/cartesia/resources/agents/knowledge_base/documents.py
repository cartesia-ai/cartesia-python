# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Literal

import httpx

from ...._types import Body, Omit, Query, Headers, NoneType, NotGiven, omit, not_given
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
from ....types.agents.knowledge_base import (
    document_list_params,
    document_create_params,
    document_delete_params,
    document_update_params,
    document_create_bulk_params,
)
from ....types.agents.knowledge_base.document import Document
from ....types.agents.knowledge_base.document_create_bulk_response import DocumentCreateBulkResponse

__all__ = ["DocumentsResource", "AsyncDocumentsResource"]


class DocumentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return DocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return DocumentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        content: str | Omit = omit,
        file_id: str | Omit = omit,
        folder_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Upload a document into a [knowledge base](/line/knowledge-base) folder

        Args:
          content: The document text. Maximum 1 MB.

          file_id: A file uploaded with purpose `knowledge_base_document`, instead of `content`.
              Its text is extracted in the background.

          folder_id: The folder to upload the document into. Omit or `null` to file it at the root.

          metadata: User-defined string-keyed metadata. Used to filter retrieval at query time.

          name: An optional display name for the document. Defaults to the file's name for a
              file.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/documents",
            body=maybe_transform(
                {
                    "content": content,
                    "file_id": file_id,
                    "folder_id": folder_id,
                    "metadata": metadata,
                    "name": name,
                },
                document_create_params.DocumentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Returns the details of a single [knowledge base](/line/knowledge-base) document,
        including its full content.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._get(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    def update(
        self,
        document_id: str,
        *,
        content: str | Omit = omit,
        folder_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Update a [knowledge base](/line/knowledge-base) document's name, content,
        metadata, or folder

        Args:
          content: New document text. Maximum 1 MB. Updating this property triggers re-indexing of
              the document.

          folder_id: Move the document to a different folder.

          metadata: Replacement metadata map. Updating this property triggers re-indexing of the
              document.

          name: New display name. Pass `null` to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._patch(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            body=maybe_transform(
                {
                    "content": content,
                    "folder_id": folder_id,
                    "metadata": metadata,
                    "name": name,
                },
                document_update_params.DocumentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncCursorIDPage[Document]:
        """
        List all [knowledge base](/line/knowledge-base) documents in your organization

        Args:
          ending_before: A cursor for pagination. Pass the ID of the first document from the previous
              page to fetch the previous page.

          limit: The number of documents to return per page, ranging between 1 and 100. Defaults
              to 10.

          starting_after: A cursor for pagination. Pass the ID of the last document from the previous page
              to fetch the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/documents",
            page=SyncCursorIDPage[Document],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    document_list_params.DocumentListParams,
                ),
            ),
            model=Document,
        )

    def delete(
        self,
        document_id: str,
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
        Delete a [knowledge base](/line/knowledge-base) document.

        Args:
          force: Delete the document even if agents can search it. Agents linked to it stop using
              it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"force": force}, document_delete_params.DocumentDeleteParams),
            ),
            cast_to=NoneType,
        )

    def create_bulk(
        self,
        *,
        documents: Iterable[document_create_bulk_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentCreateBulkResponse:
        """
        Upload up to 100 [knowledge base](/line/knowledge-base) documents in a single
        request

        Args:
          documents: The documents to upload. Up to 100 per request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/agents/documents/bulk",
            body=maybe_transform({"documents": documents}, document_create_bulk_params.DocumentCreateBulkParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateBulkResponse,
        )

    def retry(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Retry processing a [knowledge base](/line/knowledge-base) document that failed.
        Documents that are processing or ready are returned unchanged.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return self._post(
            path_template("/agents/documents/{document_id}/retry", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )


class AsyncDocumentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDocumentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDocumentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDocumentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncDocumentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        content: str | Omit = omit,
        file_id: str | Omit = omit,
        folder_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Upload a document into a [knowledge base](/line/knowledge-base) folder

        Args:
          content: The document text. Maximum 1 MB.

          file_id: A file uploaded with purpose `knowledge_base_document`, instead of `content`.
              Its text is extracted in the background.

          folder_id: The folder to upload the document into. Omit or `null` to file it at the root.

          metadata: User-defined string-keyed metadata. Used to filter retrieval at query time.

          name: An optional display name for the document. Defaults to the file's name for a
              file.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/documents",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "file_id": file_id,
                    "folder_id": folder_id,
                    "metadata": metadata,
                    "name": name,
                },
                document_create_params.DocumentCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    async def retrieve(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Returns the details of a single [knowledge base](/line/knowledge-base) document,
        including its full content.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._get(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    async def update(
        self,
        document_id: str,
        *,
        content: str | Omit = omit,
        folder_id: Optional[str] | Omit = omit,
        metadata: Dict[str, str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Update a [knowledge base](/line/knowledge-base) document's name, content,
        metadata, or folder

        Args:
          content: New document text. Maximum 1 MB. Updating this property triggers re-indexing of
              the document.

          folder_id: Move the document to a different folder.

          metadata: Replacement metadata map. Updating this property triggers re-indexing of the
              document.

          name: New display name. Pass `null` to clear.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._patch(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            body=await async_maybe_transform(
                {
                    "content": content,
                    "folder_id": folder_id,
                    "metadata": metadata,
                    "name": name,
                },
                document_update_params.DocumentUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )

    def list(
        self,
        *,
        ending_before: str | Omit = omit,
        limit: int | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[Document, AsyncCursorIDPage[Document]]:
        """
        List all [knowledge base](/line/knowledge-base) documents in your organization

        Args:
          ending_before: A cursor for pagination. Pass the ID of the first document from the previous
              page to fetch the previous page.

          limit: The number of documents to return per page, ranging between 1 and 100. Defaults
              to 10.

          starting_after: A cursor for pagination. Pass the ID of the last document from the previous page
              to fetch the next page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/agents/documents",
            page=AsyncCursorIDPage[Document],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ending_before": ending_before,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    document_list_params.DocumentListParams,
                ),
            ),
            model=Document,
        )

    async def delete(
        self,
        document_id: str,
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
        Delete a [knowledge base](/line/knowledge-base) document.

        Args:
          force: Delete the document even if agents can search it. Agents linked to it stop using
              it.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            path_template("/agents/documents/{document_id}", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"force": force}, document_delete_params.DocumentDeleteParams),
            ),
            cast_to=NoneType,
        )

    async def create_bulk(
        self,
        *,
        documents: Iterable[document_create_bulk_params.Document],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DocumentCreateBulkResponse:
        """
        Upload up to 100 [knowledge base](/line/knowledge-base) documents in a single
        request

        Args:
          documents: The documents to upload. Up to 100 per request.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/agents/documents/bulk",
            body=await async_maybe_transform(
                {"documents": documents}, document_create_bulk_params.DocumentCreateBulkParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DocumentCreateBulkResponse,
        )

    async def retry(
        self,
        document_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Document:
        """
        Retry processing a [knowledge base](/line/knowledge-base) document that failed.
        Documents that are processing or ready are returned unchanged.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not document_id:
            raise ValueError(f"Expected a non-empty value for `document_id` but received {document_id!r}")
        return await self._post(
            path_template("/agents/documents/{document_id}/retry", document_id=document_id),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=Document,
        )


class DocumentsResourceWithRawResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.create = to_raw_response_wrapper(
            documents.create,
        )
        self.retrieve = to_raw_response_wrapper(
            documents.retrieve,
        )
        self.update = to_raw_response_wrapper(
            documents.update,
        )
        self.list = to_raw_response_wrapper(
            documents.list,
        )
        self.delete = to_raw_response_wrapper(
            documents.delete,
        )
        self.create_bulk = to_raw_response_wrapper(
            documents.create_bulk,
        )
        self.retry = to_raw_response_wrapper(
            documents.retry,
        )


class AsyncDocumentsResourceWithRawResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.create = async_to_raw_response_wrapper(
            documents.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            documents.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            documents.update,
        )
        self.list = async_to_raw_response_wrapper(
            documents.list,
        )
        self.delete = async_to_raw_response_wrapper(
            documents.delete,
        )
        self.create_bulk = async_to_raw_response_wrapper(
            documents.create_bulk,
        )
        self.retry = async_to_raw_response_wrapper(
            documents.retry,
        )


class DocumentsResourceWithStreamingResponse:
    def __init__(self, documents: DocumentsResource) -> None:
        self._documents = documents

        self.create = to_streamed_response_wrapper(
            documents.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            documents.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            documents.update,
        )
        self.list = to_streamed_response_wrapper(
            documents.list,
        )
        self.delete = to_streamed_response_wrapper(
            documents.delete,
        )
        self.create_bulk = to_streamed_response_wrapper(
            documents.create_bulk,
        )
        self.retry = to_streamed_response_wrapper(
            documents.retry,
        )


class AsyncDocumentsResourceWithStreamingResponse:
    def __init__(self, documents: AsyncDocumentsResource) -> None:
        self._documents = documents

        self.create = async_to_streamed_response_wrapper(
            documents.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            documents.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            documents.update,
        )
        self.list = async_to_streamed_response_wrapper(
            documents.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            documents.delete,
        )
        self.create_bulk = async_to_streamed_response_wrapper(
            documents.create_bulk,
        )
        self.retry = async_to_streamed_response_wrapper(
            documents.retry,
        )
