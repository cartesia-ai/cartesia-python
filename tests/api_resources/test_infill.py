# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInfill:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        infill = client.infill.create()
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        infill = client.infill.create(
            language="language",
            left_audio=b"raw file contents",
            model_id="model_id",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            right_audio=b"raw file contents",
            transcript="transcript",
            voice_id="voice_id",
        )
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.infill.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        infill = response.parse()
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.infill.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            infill = response.parse()
            assert infill is None

        assert cast(Any, response.is_closed) is True


class TestAsyncInfill:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        infill = await async_client.infill.create()
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        infill = await async_client.infill.create(
            language="language",
            left_audio=b"raw file contents",
            model_id="model_id",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            right_audio=b"raw file contents",
            transcript="transcript",
            voice_id="voice_id",
        )
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.infill.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        infill = await response.parse()
        assert infill is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.infill.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            infill = await response.parse()
            assert infill is None

        assert cast(Any, response.is_closed) is True
