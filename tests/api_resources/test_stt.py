# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from noah_testing import NoahTesting, AsyncNoahTesting
from noah_testing.types import SttTranscribeResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStt:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_transcribe(self, client: NoahTesting) -> None:
        stt = client.stt.transcribe()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_transcribe_with_all_params(self, client: NoahTesting) -> None:
        stt = client.stt.transcribe(
            encoding="pcm_s16le",
            sample_rate=0,
            file=b"raw file contents",
            language="language",
            model="model",
            timestamp_granularities=["word"],
        )
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_transcribe(self, client: NoahTesting) -> None:
        response = client.stt.with_raw_response.transcribe()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stt = response.parse()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_transcribe(self, client: NoahTesting) -> None:
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

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_transcribe(self, async_client: AsyncNoahTesting) -> None:
        stt = await async_client.stt.transcribe()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_transcribe_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        stt = await async_client.stt.transcribe(
            encoding="pcm_s16le",
            sample_rate=0,
            file=b"raw file contents",
            language="language",
            model="model",
            timestamp_granularities=["word"],
        )
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_transcribe(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.stt.with_raw_response.transcribe()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stt = await response.parse()
        assert_matches_type(SttTranscribeResponse, stt, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_transcribe(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.stt.with_streaming_response.transcribe() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stt = await response.parse()
            assert_matches_type(SttTranscribeResponse, stt, path=["response"])

        assert cast(Any, response.is_closed) is True
