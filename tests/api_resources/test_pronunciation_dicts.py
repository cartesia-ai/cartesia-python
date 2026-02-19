# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types import (
    PronunciationDict,
)
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPronunciationDicts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.create(
            name="name",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.create(
            name="name",
            items=[
                {
                    "alias": "alias",
                    "text": "text",
                }
            ],
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.pronunciation_dicts.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.pronunciation_dicts.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.retrieve(
            "id",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.pronunciation_dicts.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.pronunciation_dicts.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.pronunciation_dicts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.update(
            id="id",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.update(
            id="id",
            items=[
                {
                    "alias": "alias",
                    "text": "text",
                }
            ],
            name="name",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Cartesia) -> None:
        response = client.pronunciation_dicts.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Cartesia) -> None:
        with client.pronunciation_dicts.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.pronunciation_dicts.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.list()
        assert_matches_type(SyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.list(
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.pronunciation_dicts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = response.parse()
        assert_matches_type(SyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.pronunciation_dicts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = response.parse()
            assert_matches_type(SyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        pronunciation_dict = client.pronunciation_dicts.delete(
            "id",
        )
        assert pronunciation_dict is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.pronunciation_dicts.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = response.parse()
        assert pronunciation_dict is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.pronunciation_dicts.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = response.parse()
            assert pronunciation_dict is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.pronunciation_dicts.with_raw_response.delete(
                "",
            )


class TestAsyncPronunciationDicts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.create(
            name="name",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.create(
            name="name",
            items=[
                {
                    "alias": "alias",
                    "text": "text",
                }
            ],
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.pronunciation_dicts.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = await response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.pronunciation_dicts.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = await response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.retrieve(
            "id",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.pronunciation_dicts.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = await response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.pronunciation_dicts.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = await response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.pronunciation_dicts.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.update(
            id="id",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.update(
            id="id",
            items=[
                {
                    "alias": "alias",
                    "text": "text",
                }
            ],
            name="name",
        )
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCartesia) -> None:
        response = await async_client.pronunciation_dicts.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = await response.parse()
        assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCartesia) -> None:
        async with async_client.pronunciation_dicts.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = await response.parse()
            assert_matches_type(PronunciationDict, pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.pronunciation_dicts.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.list()
        assert_matches_type(AsyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.list(
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.pronunciation_dicts.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = await response.parse()
        assert_matches_type(AsyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.pronunciation_dicts.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = await response.parse()
            assert_matches_type(AsyncCursorIDPage[PronunciationDict], pronunciation_dict, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        pronunciation_dict = await async_client.pronunciation_dicts.delete(
            "id",
        )
        assert pronunciation_dict is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.pronunciation_dicts.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pronunciation_dict = await response.parse()
        assert pronunciation_dict is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.pronunciation_dicts.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pronunciation_dict = await response.parse()
            assert pronunciation_dict is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.pronunciation_dicts.with_raw_response.delete(
                "",
            )
