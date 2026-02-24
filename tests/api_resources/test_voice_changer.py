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


class TestVoiceChanger:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_change_voice_bytes(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        voice_changer = client.voice_changer.change_voice_bytes()
        assert voice_changer.is_closed
        assert voice_changer.json() == {"foo": "bar"}
        assert cast(Any, voice_changer.is_closed) is True
        assert isinstance(voice_changer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_change_voice_bytes_with_all_params(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        voice_changer = client.voice_changer.change_voice_bytes(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            voice_id="voice[id]",
        )
        assert voice_changer.is_closed
        assert voice_changer.json() == {"foo": "bar"}
        assert cast(Any, voice_changer.is_closed) is True
        assert isinstance(voice_changer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_change_voice_bytes(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        voice_changer = client.voice_changer.with_raw_response.change_voice_bytes()

        assert voice_changer.is_closed is True
        assert voice_changer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert voice_changer.json() == {"foo": "bar"}
        assert isinstance(voice_changer, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_change_voice_bytes(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.voice_changer.with_streaming_response.change_voice_bytes() as voice_changer:
            assert not voice_changer.is_closed
            assert voice_changer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert voice_changer.json() == {"foo": "bar"}
            assert cast(Any, voice_changer.is_closed) is True
            assert isinstance(voice_changer, StreamedBinaryAPIResponse)

        assert cast(Any, voice_changer.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_change_voice_sse(self, client: Cartesia) -> None:
        voice_changer = client.voice_changer.change_voice_sse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_change_voice_sse_with_all_params(self, client: Cartesia) -> None:
        voice_changer = client.voice_changer.change_voice_sse(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_change_voice_sse(self, client: Cartesia) -> None:
        response = client.voice_changer.with_raw_response.change_voice_sse()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_change_voice_sse(self, client: Cartesia) -> None:
        with client.voice_changer.with_streaming_response.change_voice_sse() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice_changer = response.parse()
            assert voice_changer is None

        assert cast(Any, response.is_closed) is True


class TestAsyncVoiceChanger:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_change_voice_bytes(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        voice_changer = await async_client.voice_changer.change_voice_bytes()
        assert voice_changer.is_closed
        assert await voice_changer.json() == {"foo": "bar"}
        assert cast(Any, voice_changer.is_closed) is True
        assert isinstance(voice_changer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_change_voice_bytes_with_all_params(
        self, async_client: AsyncCartesia, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        voice_changer = await async_client.voice_changer.change_voice_bytes(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            voice_id="voice[id]",
        )
        assert voice_changer.is_closed
        assert await voice_changer.json() == {"foo": "bar"}
        assert cast(Any, voice_changer.is_closed) is True
        assert isinstance(voice_changer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_change_voice_bytes(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        voice_changer = await async_client.voice_changer.with_raw_response.change_voice_bytes()

        assert voice_changer.is_closed is True
        assert voice_changer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await voice_changer.json() == {"foo": "bar"}
        assert isinstance(voice_changer, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_change_voice_bytes(
        self, async_client: AsyncCartesia, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/voice-changer/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.voice_changer.with_streaming_response.change_voice_bytes() as voice_changer:
            assert not voice_changer.is_closed
            assert voice_changer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await voice_changer.json() == {"foo": "bar"}
            assert cast(Any, voice_changer.is_closed) is True
            assert isinstance(voice_changer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, voice_changer.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_change_voice_sse(self, async_client: AsyncCartesia) -> None:
        voice_changer = await async_client.voice_changer.change_voice_sse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_change_voice_sse_with_all_params(self, async_client: AsyncCartesia) -> None:
        voice_changer = await async_client.voice_changer.change_voice_sse(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=8000,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_change_voice_sse(self, async_client: AsyncCartesia) -> None:
        response = await async_client.voice_changer.with_raw_response.change_voice_sse()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = await response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_change_voice_sse(self, async_client: AsyncCartesia) -> None:
        async with async_client.voice_changer.with_streaming_response.change_voice_sse() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice_changer = await response.parse()
            assert voice_changer is None

        assert cast(Any, response.is_closed) is True
