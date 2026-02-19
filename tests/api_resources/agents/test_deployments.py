# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types.agents import Deployment, DeploymentListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDeployments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        deployment = client.agents.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(Deployment, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(Deployment, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(Deployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.agents.deployments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        deployment = client.agents.deployments.list(
            "agent_id",
        )
        assert_matches_type(DeploymentListResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.deployments.with_raw_response.list(
            "agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = response.parse()
        assert_matches_type(DeploymentListResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.deployments.with_streaming_response.list(
            "agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = response.parse()
            assert_matches_type(DeploymentListResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_list(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.deployments.with_raw_response.list(
                "",
            )


class TestAsyncDeployments:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        deployment = await async_client.agents.deployments.retrieve(
            "deployment_id",
        )
        assert_matches_type(Deployment, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.deployments.with_raw_response.retrieve(
            "deployment_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(Deployment, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.deployments.with_streaming_response.retrieve(
            "deployment_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(Deployment, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.agents.deployments.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        deployment = await async_client.agents.deployments.list(
            "agent_id",
        )
        assert_matches_type(DeploymentListResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.deployments.with_raw_response.list(
            "agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        deployment = await response.parse()
        assert_matches_type(DeploymentListResponse, deployment, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.deployments.with_streaming_response.list(
            "agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            deployment = await response.parse()
            assert_matches_type(DeploymentListResponse, deployment, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_list(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.deployments.with_raw_response.list(
                "",
            )
