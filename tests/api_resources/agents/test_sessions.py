# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types.agents import (
    SessionCreateWebrtcResponse,
    SessionCreateWebsocketResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_webrtc(self, client: Cartesia) -> None:
        session = client.agents.sessions.create_webrtc(
            agent_id="x",
        )
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_webrtc_with_all_params(self, client: Cartesia) -> None:
        session = client.agents.sessions.create_webrtc(
            agent_id="x",
            config_overrides={
                "audio": {
                    "output": {
                        "emotion": "neutral",
                        "speed": 0.6,
                        "voice_id": "x",
                    }
                },
                "initial_message": "initial_message",
                "instructions": "x",
                "language": {"primary": "en"},
            },
            dynamic_variables={"foo": "string"},
        )
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_webrtc(self, client: Cartesia) -> None:
        response = client.agents.sessions.with_raw_response.create_webrtc(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_webrtc(self, client: Cartesia) -> None:
        with client.agents.sessions.with_streaming_response.create_webrtc(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_webrtc(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.sessions.with_raw_response.create_webrtc(
                agent_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_websocket(self, client: Cartesia) -> None:
        session = client.agents.sessions.create_websocket(
            agent_id="x",
        )
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_websocket_with_all_params(self, client: Cartesia) -> None:
        session = client.agents.sessions.create_websocket(
            agent_id="x",
            config_overrides={
                "audio": {
                    "output": {
                        "emotion": "neutral",
                        "speed": 0.6,
                        "voice_id": "x",
                    }
                },
                "initial_message": "initial_message",
                "instructions": "x",
                "language": {"primary": "en"},
            },
            dynamic_variables={"foo": "string"},
        )
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_websocket(self, client: Cartesia) -> None:
        response = client.agents.sessions.with_raw_response.create_websocket(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_websocket(self, client: Cartesia) -> None:
        with client.agents.sessions.with_streaming_response.create_websocket(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create_websocket(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.sessions.with_raw_response.create_websocket(
                agent_id="",
            )


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_webrtc(self, async_client: AsyncCartesia) -> None:
        session = await async_client.agents.sessions.create_webrtc(
            agent_id="x",
        )
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_webrtc_with_all_params(self, async_client: AsyncCartesia) -> None:
        session = await async_client.agents.sessions.create_webrtc(
            agent_id="x",
            config_overrides={
                "audio": {
                    "output": {
                        "emotion": "neutral",
                        "speed": 0.6,
                        "voice_id": "x",
                    }
                },
                "initial_message": "initial_message",
                "instructions": "x",
                "language": {"primary": "en"},
            },
            dynamic_variables={"foo": "string"},
        )
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_webrtc(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.sessions.with_raw_response.create_webrtc(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_webrtc(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.sessions.with_streaming_response.create_webrtc(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionCreateWebrtcResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_webrtc(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.sessions.with_raw_response.create_webrtc(
                agent_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_websocket(self, async_client: AsyncCartesia) -> None:
        session = await async_client.agents.sessions.create_websocket(
            agent_id="x",
        )
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_websocket_with_all_params(self, async_client: AsyncCartesia) -> None:
        session = await async_client.agents.sessions.create_websocket(
            agent_id="x",
            config_overrides={
                "audio": {
                    "output": {
                        "emotion": "neutral",
                        "speed": 0.6,
                        "voice_id": "x",
                    }
                },
                "initial_message": "initial_message",
                "instructions": "x",
                "language": {"primary": "en"},
            },
            dynamic_variables={"foo": "string"},
        )
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_websocket(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.sessions.with_raw_response.create_websocket(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_websocket(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.sessions.with_streaming_response.create_websocket(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionCreateWebsocketResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create_websocket(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.sessions.with_raw_response.create_websocket(
                agent_id="",
            )
