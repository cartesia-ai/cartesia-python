# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage
from cartesia.types.agents.knowledge_base import (
    Document,
    DocumentCreateBulkResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDocuments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.create()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.create(
            content="x",
            file_id="x",
            folder_id="x",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.retrieve(
            "document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.retrieve(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.retrieve(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.agents.knowledge_base.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.update(
            document_id="document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.update(
            document_id="document_id",
            content="x",
            folder_id="x",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.update(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.update(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.agents.knowledge_base.documents.with_raw_response.update(
                document_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.list()
        assert_matches_type(SyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.list(
            ending_before="ending_before",
            limit=1,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(SyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(SyncCursorIDPage[Document], document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.delete(
            document_id="document_id",
        )
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete_with_all_params(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.delete(
            document_id="document_id",
            force="true",
        )
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.delete(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.delete(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert document is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.agents.knowledge_base.documents.with_raw_response.delete(
                document_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_bulk(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.create_bulk(
            documents=[{}],
        )
        assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_bulk(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.create_bulk(
            documents=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_bulk(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.create_bulk(
            documents=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retry(self, client: Cartesia) -> None:
        document = client.agents.knowledge_base.documents.retry(
            "document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retry(self, client: Cartesia) -> None:
        response = client.agents.knowledge_base.documents.with_raw_response.retry(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retry(self, client: Cartesia) -> None:
        with client.agents.knowledge_base.documents.with_streaming_response.retry(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retry(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            client.agents.knowledge_base.documents.with_raw_response.retry(
                "",
            )


class TestAsyncDocuments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.create()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.create(
            content="x",
            file_id="x",
            folder_id="x",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.retrieve(
            "document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.retrieve(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.retrieve(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.agents.knowledge_base.documents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.update(
            document_id="document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.update(
            document_id="document_id",
            content="x",
            folder_id="x",
            metadata={"foo": "string"},
            name="name",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.update(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.update(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.agents.knowledge_base.documents.with_raw_response.update(
                document_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.list()
        assert_matches_type(AsyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.list(
            ending_before="ending_before",
            limit=1,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(AsyncCursorIDPage[Document], document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(AsyncCursorIDPage[Document], document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.delete(
            document_id="document_id",
        )
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.delete(
            document_id="document_id",
            force="true",
        )
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.delete(
            document_id="document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert document is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.delete(
            document_id="document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert document is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.agents.knowledge_base.documents.with_raw_response.delete(
                document_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_bulk(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.create_bulk(
            documents=[{}],
        )
        assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_bulk(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.create_bulk(
            documents=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_bulk(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.create_bulk(
            documents=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(DocumentCreateBulkResponse, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retry(self, async_client: AsyncCartesia) -> None:
        document = await async_client.agents.knowledge_base.documents.retry(
            "document_id",
        )
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retry(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.knowledge_base.documents.with_raw_response.retry(
            "document_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        document = await response.parse()
        assert_matches_type(Document, document, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retry(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.knowledge_base.documents.with_streaming_response.retry(
            "document_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            document = await response.parse()
            assert_matches_type(Document, document, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retry(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `document_id` but received ''"):
            await async_client.agents.knowledge_base.documents.with_raw_response.retry(
                "",
            )
