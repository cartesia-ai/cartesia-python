# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types import WatermarkDetectResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWatermark:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_detect(self, client: Cartesia) -> None:
        watermark = client.watermark.detect(
            file=b"Example data",
        )
        assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_detect(self, client: Cartesia) -> None:
        response = client.watermark.with_raw_response.detect(
            file=b"Example data",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        watermark = response.parse()
        assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_detect(self, client: Cartesia) -> None:
        with client.watermark.with_streaming_response.detect(
            file=b"Example data",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            watermark = response.parse()
            assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWatermark:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_detect(self, async_client: AsyncCartesia) -> None:
        watermark = await async_client.watermark.detect(
            file=b"Example data",
        )
        assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_detect(self, async_client: AsyncCartesia) -> None:
        response = await async_client.watermark.with_raw_response.detect(
            file=b"Example data",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        watermark = await response.parse()
        assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_detect(self, async_client: AsyncCartesia) -> None:
        async with async_client.watermark.with_streaming_response.detect(
            file=b"Example data",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            watermark = await response.parse()
            assert_matches_type(WatermarkDetectResponse, watermark, path=["response"])

        assert cast(Any, response.is_closed) is True
