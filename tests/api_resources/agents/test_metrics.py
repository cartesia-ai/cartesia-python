# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from noah_testing import NoahTesting, AsyncNoahTesting
from noah_testing.types.agents import Metric, MetricListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMetrics:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.create(
            name="name",
            prompt="prompt",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.create(
            name="name",
            prompt="prompt",
            display_name="display_name",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: NoahTesting) -> None:
        response = client.agents.metrics.with_raw_response.create(
            name="name",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: NoahTesting) -> None:
        with client.agents.metrics.with_streaming_response.create(
            name="name",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(Metric, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.retrieve(
            "metric_id",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: NoahTesting) -> None:
        response = client.agents.metrics.with_raw_response.retrieve(
            "metric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: NoahTesting) -> None:
        with client.agents.metrics.with_streaming_response.retrieve(
            "metric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(Metric, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.agents.metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.list()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: NoahTesting) -> None:
        response = client.agents.metrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: NoahTesting) -> None:
        with client.agents.metrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert_matches_type(MetricListResponse, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_add_to_agent(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_add_to_agent(self, client: NoahTesting) -> None:
        response = client.agents.metrics.with_raw_response.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_add_to_agent(self, client: NoahTesting) -> None:
        with client.agents.metrics.with_streaming_response.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert metric is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_add_to_agent(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.metrics.with_raw_response.add_to_agent(
                metric_id="metric_id",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.agents.metrics.with_raw_response.add_to_agent(
                metric_id="",
                agent_id="agent_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_remove_from_agent(self, client: NoahTesting) -> None:
        metric = client.agents.metrics.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_remove_from_agent(self, client: NoahTesting) -> None:
        response = client.agents.metrics.with_raw_response.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = response.parse()
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_remove_from_agent(self, client: NoahTesting) -> None:
        with client.agents.metrics.with_streaming_response.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = response.parse()
            assert metric is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_remove_from_agent(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.metrics.with_raw_response.remove_from_agent(
                metric_id="metric_id",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            client.agents.metrics.with_raw_response.remove_from_agent(
                metric_id="",
                agent_id="agent_id",
            )


class TestAsyncMetrics:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.create(
            name="name",
            prompt="prompt",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.create(
            name="name",
            prompt="prompt",
            display_name="display_name",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.agents.metrics.with_raw_response.create(
            name="name",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.agents.metrics.with_streaming_response.create(
            name="name",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(Metric, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.retrieve(
            "metric_id",
        )
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.agents.metrics.with_raw_response.retrieve(
            "metric_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(Metric, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.agents.metrics.with_streaming_response.retrieve(
            "metric_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(Metric, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.agents.metrics.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.list()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.agents.metrics.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert_matches_type(MetricListResponse, metric, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.agents.metrics.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert_matches_type(MetricListResponse, metric, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_add_to_agent(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_add_to_agent(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.agents.metrics.with_raw_response.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_add_to_agent(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.agents.metrics.with_streaming_response.add_to_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert metric is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_add_to_agent(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.metrics.with_raw_response.add_to_agent(
                metric_id="metric_id",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.agents.metrics.with_raw_response.add_to_agent(
                metric_id="",
                agent_id="agent_id",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_remove_from_agent(self, async_client: AsyncNoahTesting) -> None:
        metric = await async_client.agents.metrics.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_remove_from_agent(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.agents.metrics.with_raw_response.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        metric = await response.parse()
        assert metric is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_remove_from_agent(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.agents.metrics.with_streaming_response.remove_from_agent(
            metric_id="metric_id",
            agent_id="agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            metric = await response.parse()
            assert metric is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_remove_from_agent(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.metrics.with_raw_response.remove_from_agent(
                metric_id="metric_id",
                agent_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `metric_id` but received ''"):
            await async_client.agents.metrics.with_raw_response.remove_from_agent(
                metric_id="",
                agent_id="agent_id",
            )
