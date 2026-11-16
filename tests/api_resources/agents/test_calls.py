# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage
from cartesia.types.agents import (
    AgentCall,
    CallLogsResponse,
    CallCancelResponse,
    CallCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCalls:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        call = client.agents.calls.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        )
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        call = client.agents.calls.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[
                {
                    "to_number": "to_number",
                    "dynamic_variables": {"foo": "string"},
                }
            ],
            max_call_duration_minutes=0,
            ringing_timeout_seconds=5,
        )
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(CallCreateResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        call = client.agents.calls.retrieve(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.retrieve(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        call = client.agents.calls.list(
            agent_id="agent_id",
        )
        assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.list(
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(SyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        call = client.agents.calls.delete(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.delete(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.delete(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(AgentCall, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_cancel(self, client: Cartesia) -> None:
        call = client.agents.calls.cancel(
            "call_id",
        )
        assert_matches_type(CallCancelResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_cancel(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.cancel(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(CallCancelResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_cancel(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.cancel(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(CallCancelResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_cancel(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_download_audio(self, client: Cartesia) -> None:
        call = client.agents.calls.download_audio(
            "call_id",
        )
        assert call is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_download_audio(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.download_audio(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert call is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_download_audio(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.download_audio(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert call is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_download_audio(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.download_audio(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_logs(self, client: Cartesia) -> None:
        call = client.agents.calls.logs(
            "call_id",
        )
        assert_matches_type(CallLogsResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_logs(self, client: Cartesia) -> None:
        response = client.agents.calls.with_raw_response.logs(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = response.parse()
        assert_matches_type(CallLogsResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_logs(self, client: Cartesia) -> None:
        with client.agents.calls.with_streaming_response.logs(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = response.parse()
            assert_matches_type(CallLogsResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_logs(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            client.agents.calls.with_raw_response.logs(
                "",
            )


class TestAsyncCalls:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        )
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[
                {
                    "to_number": "to_number",
                    "dynamic_variables": {"foo": "string"},
                }
            ],
            max_call_duration_minutes=0,
            ringing_timeout_seconds=5,
        )
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(CallCreateResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            outbound_calls=[{"to_number": "to_number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(CallCreateResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.retrieve(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.retrieve(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.list(
            agent_id="agent_id",
        )
        assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.list(
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(AsyncCursorIDPage[AgentCall], call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.delete(
            "call_id",
        )
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.delete(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(AgentCall, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.delete(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(AgentCall, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_cancel(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.cancel(
            "call_id",
        )
        assert_matches_type(CallCancelResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.cancel(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(CallCancelResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.cancel(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(CallCancelResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_download_audio(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.download_audio(
            "call_id",
        )
        assert call is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_download_audio(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.download_audio(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert call is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_download_audio(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.download_audio(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert call is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_download_audio(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.download_audio(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_logs(self, async_client: AsyncCartesia) -> None:
        call = await async_client.agents.calls.logs(
            "call_id",
        )
        assert_matches_type(CallLogsResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.with_raw_response.logs(
            "call_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        call = await response.parse()
        assert_matches_type(CallLogsResponse, call, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.with_streaming_response.logs(
            "call_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            call = await response.parse()
            assert_matches_type(CallLogsResponse, call, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_logs(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `call_id` but received ''"):
            await async_client.agents.calls.with_raw_response.logs(
                "",
            )
