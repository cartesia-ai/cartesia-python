# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia._utils import parse_datetime
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage
from cartesia.types.agents.metrics import (
    ResultListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResults:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        result = client.agents.metrics.results.list()
        assert_matches_type(SyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        result = client.agents.metrics.results.list(
            agent_id="agent_id",
            call_id="call_id",
            deployment_id="deployment_id",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            ending_before="ending_before",
            limit=0,
            metric_id="metric_id",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.metrics.results.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = response.parse()
        assert_matches_type(SyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.metrics.results.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = response.parse()
            assert_matches_type(SyncCursorIDPage[ResultListResponse], result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_export(self, client: Cartesia) -> None:
        result = client.agents.metrics.results.export()
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_export_with_all_params(self, client: Cartesia) -> None:
        result = client.agents.metrics.results.export(
            agent_id="agent_id",
            call_id="call_id",
            deployment_id="deployment_id",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            metric_id="metric_id",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_export(self, client: Cartesia) -> None:
        response = client.agents.metrics.results.with_raw_response.export()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = response.parse()
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_export(self, client: Cartesia) -> None:
        with client.agents.metrics.results.with_streaming_response.export() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = response.parse()
            assert_matches_type(str, result, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncResults:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        result = await async_client.agents.metrics.results.list()
        assert_matches_type(AsyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        result = await async_client.agents.metrics.results.list(
            agent_id="agent_id",
            call_id="call_id",
            deployment_id="deployment_id",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            ending_before="ending_before",
            limit=0,
            metric_id="metric_id",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.metrics.results.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = await response.parse()
        assert_matches_type(AsyncCursorIDPage[ResultListResponse], result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.metrics.results.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = await response.parse()
            assert_matches_type(AsyncCursorIDPage[ResultListResponse], result, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_export(self, async_client: AsyncCartesia) -> None:
        result = await async_client.agents.metrics.results.export()
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_export_with_all_params(self, async_client: AsyncCartesia) -> None:
        result = await async_client.agents.metrics.results.export(
            agent_id="agent_id",
            call_id="call_id",
            deployment_id="deployment_id",
            end_date=parse_datetime("2019-12-27T18:11:19.117Z"),
            metric_id="metric_id",
            start_date=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_export(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.metrics.results.with_raw_response.export()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        result = await response.parse()
        assert_matches_type(str, result, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_export(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.metrics.results.with_streaming_response.export() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            result = await response.parse()
            assert_matches_type(str, result, path=["response"])

        assert cast(Any, response.is_closed) is True
