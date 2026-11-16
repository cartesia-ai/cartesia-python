# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .folders import (
    FoldersResource,
    AsyncFoldersResource,
    FoldersResourceWithRawResponse,
    AsyncFoldersResourceWithRawResponse,
    FoldersResourceWithStreamingResponse,
    AsyncFoldersResourceWithStreamingResponse,
)
from .documents import (
    DocumentsResource,
    AsyncDocumentsResource,
    DocumentsResourceWithRawResponse,
    AsyncDocumentsResourceWithRawResponse,
    DocumentsResourceWithStreamingResponse,
    AsyncDocumentsResourceWithStreamingResponse,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["KnowledgeBaseResource", "AsyncKnowledgeBaseResource"]


class KnowledgeBaseResource(SyncAPIResource):
    @cached_property
    def folders(self) -> FoldersResource:
        return FoldersResource(self._client)

    @cached_property
    def documents(self) -> DocumentsResource:
        return DocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> KnowledgeBaseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return KnowledgeBaseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> KnowledgeBaseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return KnowledgeBaseResourceWithStreamingResponse(self)


class AsyncKnowledgeBaseResource(AsyncAPIResource):
    @cached_property
    def folders(self) -> AsyncFoldersResource:
        return AsyncFoldersResource(self._client)

    @cached_property
    def documents(self) -> AsyncDocumentsResource:
        return AsyncDocumentsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncKnowledgeBaseResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncKnowledgeBaseResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncKnowledgeBaseResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncKnowledgeBaseResourceWithStreamingResponse(self)


class KnowledgeBaseResourceWithRawResponse:
    def __init__(self, knowledge_base: KnowledgeBaseResource) -> None:
        self._knowledge_base = knowledge_base

    @cached_property
    def folders(self) -> FoldersResourceWithRawResponse:
        return FoldersResourceWithRawResponse(self._knowledge_base.folders)

    @cached_property
    def documents(self) -> DocumentsResourceWithRawResponse:
        return DocumentsResourceWithRawResponse(self._knowledge_base.documents)


class AsyncKnowledgeBaseResourceWithRawResponse:
    def __init__(self, knowledge_base: AsyncKnowledgeBaseResource) -> None:
        self._knowledge_base = knowledge_base

    @cached_property
    def folders(self) -> AsyncFoldersResourceWithRawResponse:
        return AsyncFoldersResourceWithRawResponse(self._knowledge_base.folders)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithRawResponse:
        return AsyncDocumentsResourceWithRawResponse(self._knowledge_base.documents)


class KnowledgeBaseResourceWithStreamingResponse:
    def __init__(self, knowledge_base: KnowledgeBaseResource) -> None:
        self._knowledge_base = knowledge_base

    @cached_property
    def folders(self) -> FoldersResourceWithStreamingResponse:
        return FoldersResourceWithStreamingResponse(self._knowledge_base.folders)

    @cached_property
    def documents(self) -> DocumentsResourceWithStreamingResponse:
        return DocumentsResourceWithStreamingResponse(self._knowledge_base.documents)


class AsyncKnowledgeBaseResourceWithStreamingResponse:
    def __init__(self, knowledge_base: AsyncKnowledgeBaseResource) -> None:
        self._knowledge_base = knowledge_base

    @cached_property
    def folders(self) -> AsyncFoldersResourceWithStreamingResponse:
        return AsyncFoldersResourceWithStreamingResponse(self._knowledge_base.folders)

    @cached_property
    def documents(self) -> AsyncDocumentsResourceWithStreamingResponse:
        return AsyncDocumentsResourceWithStreamingResponse(self._knowledge_base.documents)
