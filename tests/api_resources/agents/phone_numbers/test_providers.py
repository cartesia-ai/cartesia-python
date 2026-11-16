# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from cartesia import Cartesia, AsyncCartesia
from tests.utils import assert_matches_type
from cartesia.types.agents.phone_numbers import (
    ProviderListResponse,
    ProviderCreateResponse,
    ProviderUpdateResponse,
    ProviderRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestProviders:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_1(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params_overload_1(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
            label="x",
            region="us1",
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_1(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_1(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderCreateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_overload_2(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.create(
            body={},
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_overload_2(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.create(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_overload_2(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.create(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderCreateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.retrieve(
            "id",
        )
        assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.agents.phone_numbers.providers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_overload_1(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
            region="us1",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update_overload_1(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update_overload_1(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update_overload_1(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.agents.phone_numbers.providers.with_raw_response.update(
                id="",
                api_key_secret="api_key_secret",
                api_key_sid="api_key_sid",
                type="twilio",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_overload_2(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.update(
            id="id",
            type="sip_trunk",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_update_with_all_params_overload_2(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.update(
            id="id",
            type="sip_trunk",
            inbound={
                "allowed_addresses": ["string"],
                "allowed_numbers": ["string"],
                "credentials": {
                    "username": "x",
                    "password": "x",
                },
                "media_encryption": "disabled",
            },
            label="x",
            outbound={
                "address": "x",
                "credentials": {
                    "username": "x",
                    "password": "x",
                },
                "destination_country": "se",
                "media_encryption": "disabled",
                "transport": "tcp",
            },
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_update_overload_2(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.update(
            id="id",
            type="sip_trunk",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_update_overload_2(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.update(
            id="id",
            type="sip_trunk",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_update_overload_2(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.agents.phone_numbers.providers.with_raw_response.update(
                id="",
                type="sip_trunk",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.list()
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.list(
            account_sid="account_sid",
            type="twilio",
        )
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert_matches_type(ProviderListResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: Cartesia) -> None:
        provider = client.agents.phone_numbers.providers.delete(
            "id",
        )
        assert provider is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: Cartesia) -> None:
        response = client.agents.phone_numbers.providers.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = response.parse()
        assert provider is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: Cartesia) -> None:
        with client.agents.phone_numbers.providers.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = response.parse()
            assert provider is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: Cartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.agents.phone_numbers.providers.with_raw_response.delete(
                "",
            )


class TestAsyncProviders:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_1(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params_overload_1(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
            label="x",
            region="us1",
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_1(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_1(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.create(
            account_sid="account_sid",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderCreateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_overload_2(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.create(
            body={},
        )
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_overload_2(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.create(
            body={},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderCreateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_overload_2(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.create(
            body={},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderCreateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.retrieve(
            "id",
        )
        assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderRetrieveResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.agents.phone_numbers.providers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
            region="us1",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.update(
            id="id",
            api_key_secret="api_key_secret",
            api_key_sid="api_key_sid",
            type="twilio",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.agents.phone_numbers.providers.with_raw_response.update(
                id="",
                api_key_secret="api_key_secret",
                api_key_sid="api_key_sid",
                type="twilio",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.update(
            id="id",
            type="sip_trunk",
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_update_with_all_params_overload_2(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.update(
            id="id",
            type="sip_trunk",
            inbound={
                "allowed_addresses": ["string"],
                "allowed_numbers": ["string"],
                "credentials": {
                    "username": "x",
                    "password": "x",
                },
                "media_encryption": "disabled",
            },
            label="x",
            outbound={
                "address": "x",
                "credentials": {
                    "username": "x",
                    "password": "x",
                },
                "destination_country": "se",
                "media_encryption": "disabled",
                "transport": "tcp",
            },
        )
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.update(
            id="id",
            type="sip_trunk",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.update(
            id="id",
            type="sip_trunk",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderUpdateResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.agents.phone_numbers.providers.with_raw_response.update(
                id="",
                type="sip_trunk",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.list()
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.list(
            account_sid="account_sid",
            type="twilio",
        )
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert_matches_type(ProviderListResponse, provider, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert_matches_type(ProviderListResponse, provider, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncCartesia) -> None:
        provider = await async_client.agents.phone_numbers.providers.delete(
            "id",
        )
        assert provider is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncCartesia) -> None:
        response = await async_client.agents.phone_numbers.providers.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        provider = await response.parse()
        assert provider is None

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncCartesia) -> None:
        async with async_client.agents.phone_numbers.providers.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            provider = await response.parse()
            assert provider is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncCartesia) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.agents.phone_numbers.providers.with_raw_response.delete(
                "",
            )
