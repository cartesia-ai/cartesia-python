# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia._utils import parse_datetime
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage
from cartesia.types.agents import CallBatch

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatches:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[
                {
                    "to_number": "to_number",
                    "dynamic_variables": {"foo": "string"},
                }
            ],
            max_call_duration_minutes=1,
            region="US",
            ringing_timeout_seconds=5,
            scheduled_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_concurrency_limit=1,
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.agents.calls.batches.with_raw_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.agents.calls.batches.with_streaming_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.retrieve(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.calls.batches.with_raw_response.retrieve(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.calls.batches.with_streaming_response.retrieve(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.agents.calls.batches.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.list()
        assert_matches_type(SyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.list(
            agent_id="agent_id",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.calls.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(SyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.calls.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(SyncCursorIDPage[CallBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_cancel(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.cancel(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_cancel(self, client: Cartesia) -> None:
        response = client.agents.calls.batches.with_raw_response.cancel(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_cancel(self, client: Cartesia) -> None:
        with client.agents.calls.batches.with_streaming_response.cancel(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_cancel(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.agents.calls.batches.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retry(self, client: Cartesia) -> None:
        batch = client.agents.calls.batches.retry(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retry(self, client: Cartesia) -> None:
        response = client.agents.calls.batches.with_raw_response.retry(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retry(self, client: Cartesia) -> None:
        with client.agents.calls.batches.with_streaming_response.retry(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retry(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            client.agents.calls.batches.with_raw_response.retry(
                "",
            )


class TestAsyncBatches:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[
                {
                    "to_number": "to_number",
                    "dynamic_variables": {"foo": "string"},
                }
            ],
            max_call_duration_minutes=1,
            region="US",
            ringing_timeout_seconds=5,
            scheduled_at=parse_datetime("2019-12-27T18:11:19.117Z"),
            target_concurrency_limit=1,
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.batches.with_raw_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.batches.with_streaming_response.create(
            agent_id="agent_id",
            from_number_id="from_number_id",
            name="name",
            recipients=[{"to_number": "to_number"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.retrieve(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.batches.with_raw_response.retrieve(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.batches.with_streaming_response.retrieve(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.agents.calls.batches.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.list()
        assert_matches_type(AsyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.list(
            agent_id="agent_id",
            ending_before="ending_before",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.batches.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(AsyncCursorIDPage[CallBatch], batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.batches.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(AsyncCursorIDPage[CallBatch], batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_cancel(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.cancel(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.batches.with_raw_response.cancel(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.batches.with_streaming_response.cancel(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.agents.calls.batches.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retry(self, async_client: AsyncCartesia) -> None:
        batch = await async_client.agents.calls.batches.retry(
            "batch_id",
        )
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retry(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.calls.batches.with_raw_response.retry(
            "batch_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch = await response.parse()
        assert_matches_type(CallBatch, batch, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retry(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.calls.batches.with_streaming_response.retry(
            "batch_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch = await response.parse()
            assert_matches_type(CallBatch, batch, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retry(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `batch_id` but received ''"):
            await async_client.agents.calls.batches.with_raw_response.retry(
                "",
            )
