# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage
from cartesia.types.agents import AgentCall

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCalls:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        call = client.agents.calls.retrieve(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.retrieve(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.retrieve(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(AgentCall, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        call = client.agents.calls.list(
            agent_id="agent_id",
        )
        assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        call = client.agents.calls.list(
            agent_id="agent_id",
            ending_before="ending_before",
            expand="expand",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.list(
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.list(
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download_audio(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        call = client.agents.calls.download_audio(
            "call_id",
        )
        assert call.is_closed
        assert call.json() == {"foo": "bar"}
        assert cast(Any, call.is_closed) is True
        assert isinstance(call, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download_audio(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        call = client.agents.calls.with_raw_response.download_audio(
            "call_id",
        )

        assert call.is_closed is True
        assert call.http_request.headers.get("X-Stainless-Lang") == "python"
        assert call.json() == {"foo": "bar"}
        assert isinstance(call, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download_audio(self, client: Cartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.agents.calls.with_streaming_response.download_audio(
            "call_id",
        ) as call:
            assert not call.is_closed
            assert call.http_request.headers.get("X-Stainless-Lang") == "python"

            assert call.json() == {"foo": "bar"}
            assert cast(Any, call.is_closed) is True
            assert isinstance(call, StreamedBinaryAPIResponse)

        assert cast(Any, call.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download_audio(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.download_audio(
                "",
            )


class TestAsyncCalls:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.retrieve(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.retrieve(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.retrieve(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(AgentCall, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.list(
            agent_id="agent_id",
        )
        assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.list(
            agent_id="agent_id",
            ending_before="ending_before",
            expand="expand",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.list(
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.list(
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download_audio(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        call = await async_client.agents.calls.download_audio(
            "call_id",
        )
        assert call.is_closed
        assert await call.json() == {"foo": "bar"}
        assert cast(Any, call.is_closed) is True
        assert isinstance(call, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download_audio(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        call = await async_client.agents.calls.with_raw_response.download_audio(
            "call_id",
        )

        assert call.is_closed is True
        assert call.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await call.json() == {"foo": "bar"}
        assert isinstance(call, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download_audio(self, async_client: AsyncCartesia, respx_mock: MockRouter) -> None:
        respx_mock.get("/agents/calls/call_id/audio").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.agents.calls.with_streaming_response.download_audio(
            "call_id",
        ) as call:
            assert not call.is_closed
            assert call.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await call.json() == {"foo": "bar"}
            assert cast(Any, call.is_closed) is True
            assert isinstance(call, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, call.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download_audio(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.download_audio(
                "",
            )
