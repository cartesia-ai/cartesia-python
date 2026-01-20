# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from cartesia import Cartesia, AsyncCartesia
from cartesia._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInfill:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        infill = client.infill.create()
        assert infill.is_closed
        assert infill.json() == {"foo": "bar"}
        assert cast(Any, infill.is_closed) is True
        assert isinstance(infill, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
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
        assert infill.is_closed
        assert infill.json() == {"foo": "bar"}
        assert cast(Any, infill.is_closed) is True
        assert isinstance(infill, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        infill = client.infill.with_raw_response.create()

        assert infill.is_closed is True
        assert infill.http_request.headers.get("X-Stainless-Lang") == "python"
        assert infill.json() == {"foo": "bar"}
        assert isinstance(infill, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.infill.with_streaming_response.create() as infill:
            assert not infill.is_closed
            assert infill.http_request.headers.get("X-Stainless-Lang") == "python"

            assert infill.json() == {"foo": "bar"}
            assert cast(Any, infill.is_closed) is True
            assert isinstance(infill, StreamedBinaryAPIResponse)

        assert cast(Any, infill.is_closed) is True


class TestAsyncInfill:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        infill = await async_client.infill.create()
        assert infill.is_closed
        assert await infill.json() == {"foo": "bar"}
        assert cast(Any, infill.is_closed) is True
        assert isinstance(infill, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
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
        assert infill.is_closed
        assert await infill.json() == {"foo": "bar"}
        assert cast(Any, infill.is_closed) is True
        assert isinstance(infill, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        infill = await async_client.infill.with_raw_response.create()

        assert infill.is_closed is True
        assert infill.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await infill.json() == {"foo": "bar"}
        assert isinstance(infill, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/infill/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.infill.with_streaming_response.create() as infill:
            assert not infill.is_closed
            assert infill.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await infill.json() == {"foo": "bar"}
            assert cast(Any, infill.is_closed) is True
            assert isinstance(infill, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, infill.is_closed) is True
