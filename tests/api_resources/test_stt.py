# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types import SttTranscribeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStt:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_transcribe(self, client: Cartesia) -> None:
        stt = client.stt.transcribe()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_transcribe_with_all_params(self, client: Cartesia) -> None:
        stt = client.stt.transcribe(
            encoding="pcm_s16le",
            sample_rate=0,
            file=b"raw file contents",
            language="en",
            model="model",
            timestamp_granularities=["word"],
        )
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_transcribe(self, client: Cartesia) -> None:
        response = client.stt.with_raw_response.transcribe()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stt = response.parse()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_transcribe(self, client: Cartesia) -> None:
        with client.stt.with_streaming_response.transcribe() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stt = response.parse()
            assert_matches_type(SttTranscribeResponse, stt, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncStt:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_transcribe(self, async_client: AsyncCartesia) -> None:
        stt = await async_client.stt.transcribe()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_transcribe_with_all_params(self, async_client: AsyncCartesia) -> None:
        stt = await async_client.stt.transcribe(
            encoding="pcm_s16le",
            sample_rate=0,
            file=b"raw file contents",
            language="en",
            model="model",
            timestamp_granularities=["word"],
        )
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_transcribe(self, async_client: AsyncCartesia) -> None:
        response = await async_client.stt.with_raw_response.transcribe()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stt = await response.parse()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_transcribe(self, async_client: AsyncCartesia) -> None:
        async with async_client.stt.with_streaming_response.transcribe() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stt = await response.parse()
            assert_matches_type(SttTranscribeResponse, stt, path=["response"])

        assert cast(Any, response.is_closed) is True
