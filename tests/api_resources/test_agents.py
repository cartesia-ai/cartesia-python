# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types import Agent, AgentSummary
from cartesia.pagination import SyncCursorIDPage, AsyncCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Cartesia) -> None:
        agent = client.agents.create()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Cartesia) -> None:
        agent = client.agents.create(
            config={
                "audio": {
                    "input": {
                        "asr_model": "auto",
                        "keyterms": ["string"],
                        "noise_suppression": "off",
                    },
                    "output": {
                        "background_sound": {
                            "file_id": "x",
                            "volume": 0,
                        },
                        "emotion": "emotion",
                        "pronunciation_dictionary_id": "x",
                        "speed": 0.6,
                        "tts_model": "x",
                        "voice_id": "x",
                        "volume": 0.5,
                    },
                },
                "dynamic_variable_placeholders": {"foo": "string"},
                "event_webhook_id": "x",
                "initial_message": "initial_message",
                "initial_message_interruptions": "allow",
                "instructions": "instructions",
                "knowledge_base_documents": [{"id": "x"}],
                "knowledge_base_folders": [{"id": "x"}],
                "language": {
                    "additional": ["string"],
                    "presets": {
                        "foo": {
                            "normalization": "normalization",
                            "voice_id": "x",
                        }
                    },
                    "primary": "primary",
                },
                "model": {
                    "id": "x",
                    "custom_llm": {
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
                        "model_id": "x",
                        "request_headers": {"foo": "J!"},
                        "send_call_context": True,
                    },
                    "fallback_strategy": {"type": "auto"},
                    "max_output_tokens": 1,
                    "temperature": 0,
                },
                "prompt_optimization": True,
                "speculative_generation": True,
                "system_tools": {
                    "end_call": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "send_dtmf": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "skip_turn": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "wait_timeout_secs": -9007199254740991,
                    },
                    "transfer_to_number": {
                        "transfers": [
                            {
                                "condition": "x",
                                "destination": {
                                    "phone_number": "phone_number",
                                    "type": "phone",
                                },
                            }
                        ],
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "voicemail_detection": {
                        "description": "x",
                        "message": "x",
                        "pre_tool_speech": "auto",
                    },
                },
                "timezone": "timezone",
                "tools": [{"id": "x"}],
                "turn": {
                    "inactivity_check_in_secs": 5,
                    "inactivity_end_call_secs": 20,
                },
            },
            description="description",
            name="x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Cartesia) -> None:
        response = client.agents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Cartesia) -> None:
        with client.agents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        agent = client.agents.retrieve(
            "x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.with_raw_response.retrieve(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.with_streaming_response.retrieve(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update(self, client: Cartesia) -> None:
        agent = client.agents.update(
            agent_id="x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: Cartesia) -> None:
        agent = client.agents.update(
            agent_id="x",
            config={
                "audio": {
                    "input": {
                        "asr_model": "auto",
                        "keyterms": ["string"],
                        "noise_suppression": "off",
                    },
                    "output": {
                        "background_sound": {
                            "file_id": "x",
                            "volume": 0,
                        },
                        "emotion": "emotion",
                        "pronunciation_dictionary_id": "x",
                        "speed": 0.6,
                        "tts_model": "x",
                        "voice_id": "x",
                        "volume": 0.5,
                    },
                },
                "dynamic_variable_placeholders": {"foo": "string"},
                "event_webhook_id": "x",
                "initial_message": "initial_message",
                "initial_message_interruptions": "allow",
                "instructions": "instructions",
                "knowledge_base_documents": [{"id": "x"}],
                "knowledge_base_folders": [{"id": "x"}],
                "language": {
                    "additional": ["string"],
                    "presets": {
                        "foo": {
                            "normalization": "normalization",
                            "voice_id": "x",
                        }
                    },
                    "primary": "primary",
                },
                "model": {
                    "id": "x",
                    "custom_llm": {
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
                        "model_id": "x",
                        "request_headers": {"foo": "J!"},
                        "send_call_context": True,
                    },
                    "fallback_strategy": {"type": "auto"},
                    "max_output_tokens": 1,
                    "temperature": 0,
                },
                "prompt_optimization": True,
                "speculative_generation": True,
                "system_tools": {
                    "end_call": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "send_dtmf": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "skip_turn": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "wait_timeout_secs": -9007199254740991,
                    },
                    "transfer_to_number": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "transfers": [
                            {
                                "condition": "x",
                                "destination": {
                                    "phone_number": "phone_number",
                                    "type": "phone",
                                },
                            }
                        ],
                    },
                    "voicemail_detection": {
                        "description": "x",
                        "message": "x",
                        "pre_tool_speech": "auto",
                    },
                },
                "timezone": "timezone",
                "tools": [{"id": "x"}],
                "turn": {
                    "inactivity_check_in_secs": 5,
                    "inactivity_end_call_secs": 20,
                },
            },
            description="description",
            name="x",
            version_description="version_description",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: Cartesia) -> None:
        response = client.agents.with_raw_response.update(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: Cartesia) -> None:
        with client.agents.with_streaming_response.update(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.with_raw_response.update(
                agent_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        agent = client.agents.list()
        assert_matches_type(SyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        agent = client.agents.list(
            ending_before="ending_before",
            limit=1,
            q="q",
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(SyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(SyncCursorIDPage[AgentSummary], agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        agent = client.agents.delete(
            "x",
        )
        assert agent is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.agents.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert agent is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.agents.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert agent is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.agents.with_raw_response.delete(
                "",
            )


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.create()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.create(
            config={
                "audio": {
                    "input": {
                        "asr_model": "auto",
                        "keyterms": ["string"],
                        "noise_suppression": "off",
                    },
                    "output": {
                        "background_sound": {
                            "file_id": "x",
                            "volume": 0,
                        },
                        "emotion": "emotion",
                        "pronunciation_dictionary_id": "x",
                        "speed": 0.6,
                        "tts_model": "x",
                        "voice_id": "x",
                        "volume": 0.5,
                    },
                },
                "dynamic_variable_placeholders": {"foo": "string"},
                "event_webhook_id": "x",
                "initial_message": "initial_message",
                "initial_message_interruptions": "allow",
                "instructions": "instructions",
                "knowledge_base_documents": [{"id": "x"}],
                "knowledge_base_folders": [{"id": "x"}],
                "language": {
                    "additional": ["string"],
                    "presets": {
                        "foo": {
                            "normalization": "normalization",
                            "voice_id": "x",
                        }
                    },
                    "primary": "primary",
                },
                "model": {
                    "id": "x",
                    "custom_llm": {
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
                        "model_id": "x",
                        "request_headers": {"foo": "J!"},
                        "send_call_context": True,
                    },
                    "fallback_strategy": {"type": "auto"},
                    "max_output_tokens": 1,
                    "temperature": 0,
                },
                "prompt_optimization": True,
                "speculative_generation": True,
                "system_tools": {
                    "end_call": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "send_dtmf": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "skip_turn": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "wait_timeout_secs": -9007199254740991,
                    },
                    "transfer_to_number": {
                        "transfers": [
                            {
                                "condition": "x",
                                "destination": {
                                    "phone_number": "phone_number",
                                    "type": "phone",
                                },
                            }
                        ],
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "voicemail_detection": {
                        "description": "x",
                        "message": "x",
                        "pre_tool_speech": "auto",
                    },
                },
                "timezone": "timezone",
                "tools": [{"id": "x"}],
                "turn": {
                    "inactivity_check_in_secs": 5,
                    "inactivity_end_call_secs": 20,
                },
            },
            description="description",
            name="x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.retrieve(
            "x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.with_raw_response.retrieve(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.with_streaming_response.retrieve(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.update(
            agent_id="x",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.update(
            agent_id="x",
            config={
                "audio": {
                    "input": {
                        "asr_model": "auto",
                        "keyterms": ["string"],
                        "noise_suppression": "off",
                    },
                    "output": {
                        "background_sound": {
                            "file_id": "x",
                            "volume": 0,
                        },
                        "emotion": "emotion",
                        "pronunciation_dictionary_id": "x",
                        "speed": 0.6,
                        "tts_model": "x",
                        "voice_id": "x",
                        "volume": 0.5,
                    },
                },
                "dynamic_variable_placeholders": {"foo": "string"},
                "event_webhook_id": "x",
                "initial_message": "initial_message",
                "initial_message_interruptions": "allow",
                "instructions": "instructions",
                "knowledge_base_documents": [{"id": "x"}],
                "knowledge_base_folders": [{"id": "x"}],
                "language": {
                    "additional": ["string"],
                    "presets": {
                        "foo": {
                            "normalization": "normalization",
                            "voice_id": "x",
                        }
                    },
                    "primary": "primary",
                },
                "model": {
                    "id": "x",
                    "custom_llm": {
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
                        "model_id": "x",
                        "request_headers": {"foo": "J!"},
                        "send_call_context": True,
                    },
                    "fallback_strategy": {"type": "auto"},
                    "max_output_tokens": 1,
                    "temperature": 0,
                },
                "prompt_optimization": True,
                "speculative_generation": True,
                "system_tools": {
                    "end_call": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "send_dtmf": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                    },
                    "skip_turn": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "wait_timeout_secs": -9007199254740991,
                    },
                    "transfer_to_number": {
                        "description": "x",
                        "pre_tool_speech": "auto",
                        "transfers": [
                            {
                                "condition": "x",
                                "destination": {
                                    "phone_number": "phone_number",
                                    "type": "phone",
                                },
                            }
                        ],
                    },
                    "voicemail_detection": {
                        "description": "x",
                        "message": "x",
                        "pre_tool_speech": "auto",
                    },
                },
                "timezone": "timezone",
                "tools": [{"id": "x"}],
                "turn": {
                    "inactivity_check_in_secs": 5,
                    "inactivity_end_call_secs": 20,
                },
            },
            description="description",
            name="x",
            version_description="version_description",
        )
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.with_raw_response.update(
            agent_id="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(Agent, agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.with_streaming_response.update(
            agent_id="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(Agent, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.with_raw_response.update(
                agent_id="",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.list()
        assert_matches_type(AsyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.list(
            ending_before="ending_before",
            limit=1,
            q="q",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AsyncCursorIDPage[AgentSummary], agent, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AsyncCursorIDPage[AgentSummary], agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        agent = await async_client.agents.delete(
            "x",
        )
        assert agent is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.with_raw_response.delete(
            "x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert agent is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.with_streaming_response.delete(
            "x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert agent is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.agents.with_raw_response.delete(
                "",
            )
