# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from noah_testing import NoahTesting, AsyncNoahTesting
from noah_testing._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTTS:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_generate(self, client: NoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tts = client.tts.generate(
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
        assert tts.is_closed
        assert tts.json() == {"foo": "bar"}
        assert cast(Any, tts.is_closed) is True
        assert isinstance(tts, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_generate_with_all_params(self, client: NoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tts = client.tts.generate(
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
        assert tts.is_closed
        assert tts.json() == {"foo": "bar"}
        assert cast(Any, tts.is_closed) is True
        assert isinstance(tts, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_generate(self, client: NoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tts = client.tts.with_raw_response.generate(
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

        assert tts.is_closed is True
        assert tts.http_request.headers.get("X-Stainless-Lang") == "python"
        assert tts.json() == {"foo": "bar"}
        assert isinstance(tts, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_generate(self, client: NoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.tts.with_streaming_response.generate(
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
        ) as tts:
            assert not tts.is_closed
            assert tts.http_request.headers.get("X-Stainless-Lang") == "python"

            assert tts.json() == {"foo": "bar"}
            assert cast(Any, tts.is_closed) is True
            assert isinstance(tts, StreamedBinaryAPIResponse)

        assert cast(Any, tts.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_sse(self, client: NoahTesting) -> None:
        tts = client.tts.generate_sse(
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
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_sse_with_all_params(self, client: NoahTesting) -> None:
        tts = client.tts.generate_sse(
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
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_sse(self, client: NoahTesting) -> None:
        response = client.tts.with_raw_response.generate_sse(
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
        tts = response.parse()
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_sse(self, client: NoahTesting) -> None:
        with client.tts.with_streaming_response.generate_sse(
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

            tts = response.parse()
            assert tts is None

        assert cast(Any, response.is_closed) is True


class TestAsyncTTS:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_generate(self, async_client: AsyncNoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tts = await async_client.tts.generate(
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
        assert tts.is_closed
        assert await tts.json() == {"foo": "bar"}
        assert cast(Any, tts.is_closed) is True
        assert isinstance(tts, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_generate_with_all_params(
        self, async_client: AsyncNoahTesting, respx_mock: MockRouter
    ) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        tts = await async_client.tts.generate(
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
        assert tts.is_closed
        assert await tts.json() == {"foo": "bar"}
        assert cast(Any, tts.is_closed) is True
        assert isinstance(tts, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_generate(self, async_client: AsyncNoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        tts = await async_client.tts.with_raw_response.generate(
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

        assert tts.is_closed is True
        assert tts.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await tts.json() == {"foo": "bar"}
        assert isinstance(tts, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_generate(self, async_client: AsyncNoahTesting, respx_mock: MockRouter) -> None:
        respx_mock.post("/tts/bytes").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.tts.with_streaming_response.generate(
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
        ) as tts:
            assert not tts.is_closed
            assert tts.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await tts.json() == {"foo": "bar"}
            assert cast(Any, tts.is_closed) is True
            assert isinstance(tts, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, tts.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_sse(self, async_client: AsyncNoahTesting) -> None:
        tts = await async_client.tts.generate_sse(
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
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_sse_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        tts = await async_client.tts.generate_sse(
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
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_sse(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.tts.with_raw_response.generate_sse(
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
        tts = await response.parse()
        assert tts is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_sse(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.tts.with_streaming_response.generate_sse(
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

            tts = await response.parse()
            assert tts is None

        assert cast(Any, response.is_closed) is True
