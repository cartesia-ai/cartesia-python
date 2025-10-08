# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from noah_testing import NoahTesting, AsyncNoahTesting
from noah_testing.types import (
    FineTune,
    FineTuneListResponse,
    FineTuneListVoicesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFineTunes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        )
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: NoahTesting) -> None:
        response = client.fine_tunes.with_raw_response.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = response.parse()
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: NoahTesting) -> None:
        with client.fine_tunes.with_streaming_response.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = response.parse()
            assert_matches_type(FineTune, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.retrieve(
            "id",
        )
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: NoahTesting) -> None:
        response = client.fine_tunes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = response.parse()
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: NoahTesting) -> None:
        with client.fine_tunes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = response.parse()
            assert_matches_type(FineTune, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.fine_tunes.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.list()
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.list(
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: NoahTesting) -> None:
        response = client.fine_tunes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = response.parse()
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: NoahTesting) -> None:
        with client.fine_tunes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = response.parse()
            assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.delete(
            "id",
        )
        assert fine_tune is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: NoahTesting) -> None:
        response = client.fine_tunes.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = response.parse()
        assert fine_tune is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: NoahTesting) -> None:
        with client.fine_tunes.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = response.parse()
            assert fine_tune is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.fine_tunes.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_voices(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.list_voices(
            id="id",
        )
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_voices_with_all_params(self, client: NoahTesting) -> None:
        fine_tune = client.fine_tunes.list_voices(
            id="id",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list_voices(self, client: NoahTesting) -> None:
        response = client.fine_tunes.with_raw_response.list_voices(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = response.parse()
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list_voices(self, client: NoahTesting) -> None:
        with client.fine_tunes.with_streaming_response.list_voices(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = response.parse()
            assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_list_voices(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.fine_tunes.with_raw_response.list_voices(
                id="",
            )


class TestAsyncFineTunes:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        )
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.fine_tunes.with_raw_response.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = await response.parse()
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.fine_tunes.with_streaming_response.create(
            dataset="dataset",
            description="description",
            language="language",
            model_id="model_id",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = await response.parse()
            assert_matches_type(FineTune, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.retrieve(
            "id",
        )
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.fine_tunes.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = await response.parse()
        assert_matches_type(FineTune, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.fine_tunes.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = await response.parse()
            assert_matches_type(FineTune, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.fine_tunes.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.list()
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.list(
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.fine_tunes.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = await response.parse()
        assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.fine_tunes.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = await response.parse()
            assert_matches_type(FineTuneListResponse, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.delete(
            "id",
        )
        assert fine_tune is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.fine_tunes.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = await response.parse()
        assert fine_tune is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.fine_tunes.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = await response.parse()
            assert fine_tune is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.fine_tunes.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_voices(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.list_voices(
            id="id",
        )
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_voices_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        fine_tune = await async_client.fine_tunes.list_voices(
            id="id",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list_voices(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.fine_tunes.with_raw_response.list_voices(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        fine_tune = await response.parse()
        assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list_voices(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.fine_tunes.with_streaming_response.list_voices(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            fine_tune = await response.parse()
            assert_matches_type(FineTuneListVoicesResponse, fine_tune, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_list_voices(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.fine_tunes.with_raw_response.list_voices(
                id="",
            )
