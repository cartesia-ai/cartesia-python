# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types.agents import (
    Tool,
    ToolListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTools:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: Cartesia) -> None:
        tool = client.agents.tools.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Cartesia) -> None:
        tool = client.agents.tools.create(
            api_schema={
                "method": "GET",
                "url": "x",
                "authentication": {
                    "mode": "basic_auth",
                    "password": {
                        "type": "secret",
                        "secret_description": "x",
                        "secret_value": "secret_value",
                    },
                    "username": "username",
                },
                "path_params_schema": {
                    "foo": {
                        "type": "string",
                        "constant_value": "string",
                        "description": "description",
                        "dynamic_variable": "dynamic_variable",
                        "enum": ["string"],
                    }
                },
                "query_params_schema": {
                    "properties": {
                        "foo": {
                            "type": "string",
                            "constant_value": "string",
                            "description": "description",
                            "dynamic_variable": "dynamic_variable",
                            "enum": ["string"],
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["x"],
                },
                "request_body_schema": {},
                "request_headers": {"foo": "J!"},
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
            assignments=[
                {
                    "dynamic_variable": "dynamic_variable",
                    "value_path": "value_path",
                }
            ],
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: Cartesia) -> None:
        tool = client.agents.tools.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_2(self, client: Cartesia) -> None:
        tool = client.agents.tools.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string",
                        "description": "description",
                        "enum": ["string"],
                        "items": {"type": "string"},
                    }
                },
                "required": ["x"],
            },
            pre_tool_speech="auto",
            type="client",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        tool = client.agents.tools.retrieve(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Cartesia) -> None:
        tool = client.agents.tools.retrieve(
            tool_id="x",
            expand=["agents"],
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.retrieve(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.retrieve(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            client.agents.tools.with_raw_response.retrieve(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_overload_1(self, client: Cartesia) -> None:
        tool = client.agents.tools.update(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: Cartesia) -> None:
        tool = client.agents.tools.update(
            tool_id="x",
            api_schema={
                "authentication": {
                    "mode": "basic_auth",
                    "password": {
                        "type": "secret",
                        "secret_description": "x",
                        "secret_value": "secret_value",
                    },
                    "username": "username",
                },
                "method": "GET",
                "path_params_schema": {
                    "foo": {
                        "type": "string",
                        "constant_value": "string",
                        "description": "description",
                        "dynamic_variable": "dynamic_variable",
                        "enum": ["string"],
                    }
                },
                "query_params_schema": {
                    "properties": {
                        "foo": {
                            "type": "string",
                            "constant_value": "string",
                            "description": "description",
                            "dynamic_variable": "dynamic_variable",
                            "enum": ["string"],
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["x"],
                },
                "request_body_schema": {},
                "request_headers": {"foo": "J!"},
                "url": "x",
            },
            assignments=[
                {
                    "dynamic_variable": "dynamic_variable",
                    "value_path": "value_path",
                }
            ],
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update_overload_1(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.update(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update_overload_1(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.update(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update_overload_1(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            client.agents.tools.with_raw_response.update(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_overload_2(self, client: Cartesia) -> None:
        tool = client.agents.tools.update(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params_overload_2(self, client: Cartesia) -> None:
        tool = client.agents.tools.update(
            tool_id="x",
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string",
                        "description": "description",
                        "enum": ["string"],
                        "items": {"type": "string"},
                    }
                },
                "required": ["x"],
            },
            pre_tool_speech="auto",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update_overload_2(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.update(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update_overload_2(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.update(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update_overload_2(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            client.agents.tools.with_raw_response.update(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        tool = client.agents.tools.list()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        tool = client.agents.tools.list(
            agent_id="x",
            ending_before="ending_before",
            expand=["agents"],
            limit=1,
            starting_after="starting_after",
            type="webhook",
        )
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert_matches_type(ToolListResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        tool = client.agents.tools.delete(
            "x",
        )
        assert tool is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.agents.tools.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = response.parse()
        assert tool is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.agents.tools.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = response.parse()
            assert tool is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            client.agents.tools.with_raw_response.delete(
                "",
            )


class TestAsyncTools:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.create(
            api_schema={
                "method": "GET",
                "url": "x",
                "authentication": {
                    "mode": "basic_auth",
                    "password": {
                        "type": "secret",
                        "secret_description": "x",
                        "secret_value": "secret_value",
                    },
                    "username": "username",
                },
                "path_params_schema": {
                    "foo": {
                        "type": "string",
                        "constant_value": "string",
                        "description": "description",
                        "dynamic_variable": "dynamic_variable",
                        "enum": ["string"],
                    }
                },
                "query_params_schema": {
                    "properties": {
                        "foo": {
                            "type": "string",
                            "constant_value": "string",
                            "description": "description",
                            "dynamic_variable": "dynamic_variable",
                            "enum": ["string"],
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["x"],
                },
                "request_body_schema": {},
                "request_headers": {"foo": "J!"},
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
            assignments=[
                {
                    "dynamic_variable": "dynamic_variable",
                    "value_path": "value_path",
                }
            ],
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.create(
            api_schema={
                "method": "GET",
                "url": "x",
            },
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            type="webhook",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_2(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string",
                        "description": "description",
                        "enum": ["string"],
                        "items": {"type": "string"},
                    }
                },
                "required": ["x"],
            },
            pre_tool_speech="auto",
            type="client",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.create(
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={"type": "object"},
            pre_tool_speech="auto",
            type="client",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.retrieve(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.retrieve(
            tool_id="x",
            expand=["agents"],
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.retrieve(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.retrieve(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            await async_client.agents.tools.with_raw_response.retrieve(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.update(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.update(
            tool_id="x",
            api_schema={
                "authentication": {
                    "mode": "basic_auth",
                    "password": {
                        "type": "secret",
                        "secret_description": "x",
                        "secret_value": "secret_value",
                    },
                    "username": "username",
                },
                "method": "GET",
                "path_params_schema": {
                    "foo": {
                        "type": "string",
                        "constant_value": "string",
                        "description": "description",
                        "dynamic_variable": "dynamic_variable",
                        "enum": ["string"],
                    }
                },
                "query_params_schema": {
                    "properties": {
                        "foo": {
                            "type": "string",
                            "constant_value": "string",
                            "description": "description",
                            "dynamic_variable": "dynamic_variable",
                            "enum": ["string"],
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["x"],
                },
                "request_body_schema": {},
                "request_headers": {"foo": "J!"},
                "url": "x",
            },
            assignments=[
                {
                    "dynamic_variable": "dynamic_variable",
                    "value_path": "value_path",
                }
            ],
            description="x",
            execution_mode="immediate",
            name="name",
            pre_tool_speech="auto",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.update(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.update(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            await async_client.agents.tools.with_raw_response.update(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.update(
            tool_id="x",
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params_overload_2(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.update(
            tool_id="x",
            description="x",
            execution_mode="immediate",
            expects_response=True,
            name="name",
            parameters={
                "type": "object",
                "properties": {
                    "foo": {
                        "type": "string",
                        "description": "description",
                        "enum": ["string"],
                        "items": {"type": "string"},
                    }
                },
                "required": ["x"],
            },
            pre_tool_speech="auto",
            response_timeout_secs=1,
        )
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.update(
            tool_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(Tool, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.update(
            tool_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(Tool, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            await async_client.agents.tools.with_raw_response.update(
                tool_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.list()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.list(
            agent_id="x",
            ending_before="ending_before",
            expand=["agents"],
            limit=1,
            starting_after="starting_after",
            type="webhook",
        )
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert_matches_type(ToolListResponse, tool, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert_matches_type(ToolListResponse, tool, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        tool = await async_client.agents.tools.delete(
            "x",
        )
        assert tool is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.tools.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        tool = await response.parse()
        assert tool is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.tools.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            tool = await response.parse()
            assert tool is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `tool_id` but received ''"):
            await async_client.agents.tools.with_raw_response.delete(
                "",
            )
