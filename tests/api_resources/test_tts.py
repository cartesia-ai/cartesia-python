# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from noah_testing import NoahTesting, AsyncNoahTesting

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_synthesize_bytes(self, client: NoahTesting) -> None:
        tt = client.tts.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_synthesize_bytes_with_all_params(self, client: NoahTesting) -> None:
        tt = client.tts.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
                "container": "raw",
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
            duration=0,
            generation_config={
                "experimental": {"accent_localization": 0},
                "speed": 0,
                "volume": 0,
            },
            language="en",
            pronunciation_dict_ids=["string"],
            save=True,
            speed="slow",
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_synthesize_bytes(self, client: NoahTesting) -> None:
        response = client.tts.with_raw_response.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tt = response.parse()
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_synthesize_bytes(self, client: NoahTesting) -> None:
        with client.tts.with_streaming_response.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tt = response.parse()
            assert tt is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_synthesize_sse(self, client: NoahTesting) -> None:
        tt = client.tts.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_synthesize_sse_with_all_params(self, client: NoahTesting) -> None:
        tt = client.tts.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
            add_phoneme_timestamps=True,
            add_timestamps=True,
            context_id="context_id",
            duration=0,
            language="en",
            pronunciation_dict_ids=["string"],
            speed="slow",
            use_normalized_timestamps=True,
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_synthesize_sse(self, client: NoahTesting) -> None:
        response = client.tts.with_raw_response.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tt = response.parse()
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_synthesize_sse(self, client: NoahTesting) -> None:
        with client.tts.with_streaming_response.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tt = response.parse()
            assert tt is None

        assert cast(Any, response.is_closed) is True


class TestAsyncTts:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_synthesize_bytes(self, async_client: AsyncNoahTesting) -> None:
        tt = await async_client.tts.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_synthesize_bytes_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        tt = await async_client.tts.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
                "container": "raw",
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
            duration=0,
            generation_config={
                "experimental": {"accent_localization": 0},
                "speed": 0,
                "volume": 0,
            },
            language="en",
            pronunciation_dict_ids=["string"],
            save=True,
            speed="slow",
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_synthesize_bytes(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.tts.with_raw_response.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tt = await response.parse()
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_synthesize_bytes(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.tts.with_streaming_response.synthesize_bytes(
            model_id="model_id",
            output_format={
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tt = await response.parse()
            assert tt is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_synthesize_sse(self, async_client: AsyncNoahTesting) -> None:
        tt = await async_client.tts.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_synthesize_sse_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        tt = await async_client.tts.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
            add_phoneme_timestamps=True,
            add_timestamps=True,
            context_id="context_id",
            duration=0,
            language="en",
            pronunciation_dict_ids=["string"],
            speed="slow",
            use_normalized_timestamps=True,
        )
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_synthesize_sse(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.tts.with_raw_response.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tt = await response.parse()
        assert tt is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_synthesize_sse(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.tts.with_streaming_response.synthesize_sse(
            model_id="model_id",
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 0,
            },
            transcript="transcript",
            voice={
                "id": "id",
                "mode": "id",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tt = await response.parse()
            assert tt is None

        assert cast(Any, response.is_closed) is True
