# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from noah_testing import NoahTesting, AsyncNoahTesting

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVoiceChanger:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_voice_bytes(self, client: NoahTesting) -> None:
        voice_changer = client.voice_changer.change_voice_bytes()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_voice_bytes_with_all_params(self, client: NoahTesting) -> None:
        voice_changer = client.voice_changer.change_voice_bytes(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=0,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_change_voice_bytes(self, client: NoahTesting) -> None:
        response = client.voice_changer.with_raw_response.change_voice_bytes()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_change_voice_bytes(self, client: NoahTesting) -> None:
        with client.voice_changer.with_streaming_response.change_voice_bytes() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice_changer = response.parse()
            assert voice_changer is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_voice_sse(self, client: NoahTesting) -> None:
        voice_changer = client.voice_changer.change_voice_sse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_change_voice_sse_with_all_params(self, client: NoahTesting) -> None:
        voice_changer = client.voice_changer.change_voice_sse(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=0,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_change_voice_sse(self, client: NoahTesting) -> None:
        response = client.voice_changer.with_raw_response.change_voice_sse()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_change_voice_sse(self, client: NoahTesting) -> None:
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

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_voice_bytes(self, async_client: AsyncNoahTesting) -> None:
        voice_changer = await async_client.voice_changer.change_voice_bytes()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_voice_bytes_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice_changer = await async_client.voice_changer.change_voice_bytes(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=0,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_change_voice_bytes(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voice_changer.with_raw_response.change_voice_bytes()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = await response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_change_voice_bytes(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voice_changer.with_streaming_response.change_voice_bytes() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice_changer = await response.parse()
            assert voice_changer is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_voice_sse(self, async_client: AsyncNoahTesting) -> None:
        voice_changer = await async_client.voice_changer.change_voice_sse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_change_voice_sse_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice_changer = await async_client.voice_changer.change_voice_sse(
            clip=b"raw file contents",
            output_format_bit_rate=0,
            output_format_container="raw",
            output_format_encoding="pcm_f32le",
            output_format_sample_rate=0,
            voice_id="voice[id]",
        )
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_change_voice_sse(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voice_changer.with_raw_response.change_voice_sse()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice_changer = await response.parse()
        assert voice_changer is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_change_voice_sse(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voice_changer.with_streaming_response.change_voice_sse() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice_changer = await response.parse()
            assert voice_changer is None

        assert cast(Any, response.is_closed) is True
