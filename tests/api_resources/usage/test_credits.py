# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia._utils import parse_datetime
from cartesia.types.usage import CreditRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCredits:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        credit = client.usage.credits.retrieve()
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Cartesia) -> None:
        credit = client.usage.credits.retrieve(
            api_key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_ts=parse_datetime("2026-01-03T00:00:00Z"),
            group_by="capability",
            interval="day",
            start_ts=parse_datetime("2026-01-01T00:00:00Z"),
        )
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.usage.credits.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credit = response.parse()
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.usage.credits.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credit = response.parse()
            assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCredits:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        credit = await async_client.usage.credits.retrieve()
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncCartesia) -> None:
        credit = await async_client.usage.credits.retrieve(
            api_key_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_ts=parse_datetime("2026-01-03T00:00:00Z"),
            group_by="capability",
            interval="day",
            start_ts=parse_datetime("2026-01-01T00:00:00Z"),
        )
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.usage.credits.with_raw_response.retrieve()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        credit = await response.parse()
        assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.usage.credits.with_streaming_response.retrieve() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            credit = await response.parse()
            assert_matches_type(CreditRetrieveResponse, credit, path=["response"])

        assert cast(Any, response.is_closed) is True
