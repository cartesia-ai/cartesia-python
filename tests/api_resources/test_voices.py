# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from noah_testing import NoahTesting, AsyncNoahTesting
from noah_testing.types import (
    Voice,
    VoiceMetadata,
)
from noah_testing.pagination import SyncCursorIDPage, AsyncCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVoices:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve(self, client: NoahTesting) -> None:
        voice = client.voices.retrieve(
            "id",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(Voice, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_retrieve(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.voices.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update(self, client: NoahTesting) -> None:
        voice = client.voices.update(
            id="id",
            description="description",
            name="name",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_update_with_all_params(self, client: NoahTesting) -> None:
        voice = client.voices.update(
            id="id",
            description="description",
            name="name",
            gender="masculine",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_update(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.update(
            id="id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_update(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.update(
            id="id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(Voice, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_update(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.voices.with_raw_response.update(
                id="",
                description="description",
                name="name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list(self, client: NoahTesting) -> None:
        voice = client.voices.list()
        assert_matches_type(SyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_list_with_all_params(self, client: NoahTesting) -> None:
        voice = client.voices.list(
            ending_before="ending_before",
            expand=["is_starred"],
            gender="masculine",
            is_owner=True,
            is_starred=True,
            language="language",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(SyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_list(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(SyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_list(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(SyncCursorIDPage[Voice], voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_delete(self, client: NoahTesting) -> None:
        voice = client.voices.delete(
            "id",
        )
        assert voice is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert voice is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert voice is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: NoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.voices.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_clone(self, client: NoahTesting) -> None:
        voice = client.voices.clone()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_clone_with_all_params(self, client: NoahTesting) -> None:
        voice = client.voices.clone(
            base_voice_id="base_voice_id",
            clip=b"raw file contents",
            description="description",
            enhance=True,
            language="en",
            name="name",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_clone(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.clone()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_clone(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.clone() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceMetadata, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_localize(self, client: NoahTesting) -> None:
        voice = client.voices.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_localize_with_all_params(self, client: NoahTesting) -> None:
        voice = client.voices.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
            dialect="au",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_localize(self, client: NoahTesting) -> None:
        response = client.voices.with_raw_response.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_localize(self, client: NoahTesting) -> None:
        with client.voices.with_streaming_response.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceMetadata, voice, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVoices:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.retrieve(
            "id",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(Voice, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.voices.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.update(
            id="id",
            description="description",
            name="name",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.update(
            id="id",
            description="description",
            name="name",
            gender="masculine",
        )
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.update(
            id="id",
            description="description",
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(Voice, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.update(
            id="id",
            description="description",
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(Voice, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_update(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.voices.with_raw_response.update(
                id="",
                description="description",
                name="name",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.list()
        assert_matches_type(AsyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.list(
            ending_before="ending_before",
            expand=["is_starred"],
            gender="masculine",
            is_owner=True,
            is_starred=True,
            language="language",
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(AsyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(AsyncCursorIDPage[Voice], voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(AsyncCursorIDPage[Voice], voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.delete(
            "id",
        )
        assert voice is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert voice is None

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert voice is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncNoahTesting) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.voices.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_clone(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.clone()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_clone_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.clone(
            base_voice_id="base_voice_id",
            clip=b"raw file contents",
            description="description",
            enhance=True,
            language="en",
            name="name",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_clone(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.clone()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_clone(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.clone() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceMetadata, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_localize(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_localize_with_all_params(self, async_client: AsyncNoahTesting) -> None:
        voice = await async_client.voices.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
            dialect="au",
        )
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_localize(self, async_client: AsyncNoahTesting) -> None:
        response = await async_client.voices.with_raw_response.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceMetadata, voice, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_localize(self, async_client: AsyncNoahTesting) -> None:
        async with async_client.voices.with_streaming_response.localize(
            description="description",
            language="en",
            name="name",
            original_speaker_gender="male",
            voice_id="voice_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceMetadata, voice, path=["response"])

        assert cast(Any, response.is_closed) is True
