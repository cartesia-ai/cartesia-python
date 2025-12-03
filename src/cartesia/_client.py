# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Body,
    Omit,
    Query,
    Headers,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from ._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .resources import stt, tts, infill, voices, fine_tunes, access_token, voice_changer, pronunciation_dicts
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
    make_request_options,
)
from .resources.agents import agents
from .resources.datasets import datasets
from .types.get_status_response import GetStatusResponse

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "Cartesia",
    "AsyncCartesia",
    "Client",
    "AsyncClient",
]


class Cartesia(SyncAPIClient):
    agents: agents.AgentsResource
    access_token: access_token.AccessTokenResource
    datasets: datasets.DatasetsResource
    fine_tunes: fine_tunes.FineTunesResource
    infill: infill.InfillResource
    pronunciation_dicts: pronunciation_dicts.PronunciationDictsResource
    stt: stt.SttResource
    tts: tts.TTSResource
    voice_changer: voice_changer.VoiceChangerResource
    voices: voices.VoicesResource
    with_raw_response: CartesiaWithRawResponse
    with_streaming_response: CartesiaWithStreamedResponse

    # client options
    token: str | None
    api_key: str | None

    websocket_base_url: str | httpx.URL | None
    """Base URL for WebSocket connections.

    If not specified, the default base URL will be used, with 'wss://' replacing the
    'http://' or 'https://' scheme. For example: 'http://example.com' becomes
    'wss://example.com'
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Cartesia client instance."""
        self.token = token

        self.api_key = api_key

        self.websocket_base_url = websocket_base_url

        if base_url is None:
            base_url = os.environ.get("CARTESIA_BASE_URL")
        if base_url is None:
            base_url = f"https://api.cartesia.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agents = agents.AgentsResource(self)
        self.access_token = access_token.AccessTokenResource(self)
        self.datasets = datasets.DatasetsResource(self)
        self.fine_tunes = fine_tunes.FineTunesResource(self)
        self.infill = infill.InfillResource(self)
        self.pronunciation_dicts = pronunciation_dicts.PronunciationDictsResource(self)
        self.stt = stt.SttResource(self)
        self.tts = tts.TTSResource(self)
        self.voice_changer = voice_changer.VoiceChangerResource(self)
        self.voices = voices.VoicesResource(self)
        self.with_raw_response = CartesiaWithRawResponse(self)
        self.with_streaming_response = CartesiaWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="brackets")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._token_auth, **self._api_key_auth}

    @property
    def _token_auth(self) -> dict[str, str]:
        token = self.token
        if token is None:
            return {}
        return {"Authorization": f"Bearer {token}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            "cartesia-version": "2025-04-16",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either token or api_key to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        token: str | None = None,
        api_key: str | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            token=token or self.token,
            api_key=api_key or self.api_key,
            websocket_base_url=websocket_base_url or self.websocket_base_url,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    def get_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GetStatusResponse:
        """API Status and Version"""
        return self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GetStatusResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncCartesia(AsyncAPIClient):
    agents: agents.AsyncAgentsResource
    access_token: access_token.AsyncAccessTokenResource
    datasets: datasets.AsyncDatasetsResource
    fine_tunes: fine_tunes.AsyncFineTunesResource
    infill: infill.AsyncInfillResource
    pronunciation_dicts: pronunciation_dicts.AsyncPronunciationDictsResource
    stt: stt.AsyncSttResource
    tts: tts.AsyncTTSResource
    voice_changer: voice_changer.AsyncVoiceChangerResource
    voices: voices.AsyncVoicesResource
    with_raw_response: AsyncCartesiaWithRawResponse
    with_streaming_response: AsyncCartesiaWithStreamedResponse

    # client options
    token: str | None
    api_key: str | None

    websocket_base_url: str | httpx.URL | None
    """Base URL for WebSocket connections.

    If not specified, the default base URL will be used, with 'wss://' replacing the
    'http://' or 'https://' scheme. For example: 'http://example.com' becomes
    'wss://example.com'
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncCartesia client instance."""
        self.token = token

        self.api_key = api_key

        self.websocket_base_url = websocket_base_url

        if base_url is None:
            base_url = os.environ.get("CARTESIA_BASE_URL")
        if base_url is None:
            base_url = f"https://api.cartesia.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.agents = agents.AsyncAgentsResource(self)
        self.access_token = access_token.AsyncAccessTokenResource(self)
        self.datasets = datasets.AsyncDatasetsResource(self)
        self.fine_tunes = fine_tunes.AsyncFineTunesResource(self)
        self.infill = infill.AsyncInfillResource(self)
        self.pronunciation_dicts = pronunciation_dicts.AsyncPronunciationDictsResource(self)
        self.stt = stt.AsyncSttResource(self)
        self.tts = tts.AsyncTTSResource(self)
        self.voice_changer = voice_changer.AsyncVoiceChangerResource(self)
        self.voices = voices.AsyncVoicesResource(self)
        self.with_raw_response = AsyncCartesiaWithRawResponse(self)
        self.with_streaming_response = AsyncCartesiaWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="brackets")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        return {**self._token_auth, **self._api_key_auth}

    @property
    def _token_auth(self) -> dict[str, str]:
        token = self.token
        if token is None:
            return {}
        return {"Authorization": f"Bearer {token}"}

    @property
    def _api_key_auth(self) -> dict[str, str]:
        api_key = self.api_key
        if api_key is None:
            return {}
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            "cartesia-version": "2025-04-16",
            **self._custom_headers,
        }

    @override
    def _validate_headers(self, headers: Headers, custom_headers: Headers) -> None:
        if self.token and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        if self.api_key and headers.get("Authorization"):
            return
        if isinstance(custom_headers.get("Authorization"), Omit):
            return

        raise TypeError(
            '"Could not resolve authentication method. Expected either token or api_key to be set. Or for one of the `Authorization` or `Authorization` headers to be explicitly omitted"'
        )

    def copy(
        self,
        *,
        token: str | None = None,
        api_key: str | None = None,
        websocket_base_url: str | httpx.URL | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            token=token or self.token,
            api_key=api_key or self.api_key,
            websocket_base_url=websocket_base_url or self.websocket_base_url,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    async def get_status(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GetStatusResponse:
        """API Status and Version"""
        return await self.get(
            "/",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=GetStatusResponse,
        )

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class CartesiaWithRawResponse:
    def __init__(self, client: Cartesia) -> None:
        self.agents = agents.AgentsResourceWithRawResponse(client.agents)
        self.access_token = access_token.AccessTokenResourceWithRawResponse(client.access_token)
        self.datasets = datasets.DatasetsResourceWithRawResponse(client.datasets)
        self.fine_tunes = fine_tunes.FineTunesResourceWithRawResponse(client.fine_tunes)
        self.infill = infill.InfillResourceWithRawResponse(client.infill)
        self.pronunciation_dicts = pronunciation_dicts.PronunciationDictsResourceWithRawResponse(
            client.pronunciation_dicts
        )
        self.stt = stt.SttResourceWithRawResponse(client.stt)
        self.tts = tts.TTSResourceWithRawResponse(client.tts)
        self.voice_changer = voice_changer.VoiceChangerResourceWithRawResponse(client.voice_changer)
        self.voices = voices.VoicesResourceWithRawResponse(client.voices)

        self.get_status = to_raw_response_wrapper(
            client.get_status,
        )


class AsyncCartesiaWithRawResponse:
    def __init__(self, client: AsyncCartesia) -> None:
        self.agents = agents.AsyncAgentsResourceWithRawResponse(client.agents)
        self.access_token = access_token.AsyncAccessTokenResourceWithRawResponse(client.access_token)
        self.datasets = datasets.AsyncDatasetsResourceWithRawResponse(client.datasets)
        self.fine_tunes = fine_tunes.AsyncFineTunesResourceWithRawResponse(client.fine_tunes)
        self.infill = infill.AsyncInfillResourceWithRawResponse(client.infill)
        self.pronunciation_dicts = pronunciation_dicts.AsyncPronunciationDictsResourceWithRawResponse(
            client.pronunciation_dicts
        )
        self.stt = stt.AsyncSttResourceWithRawResponse(client.stt)
        self.tts = tts.AsyncTTSResourceWithRawResponse(client.tts)
        self.voice_changer = voice_changer.AsyncVoiceChangerResourceWithRawResponse(client.voice_changer)
        self.voices = voices.AsyncVoicesResourceWithRawResponse(client.voices)

        self.get_status = async_to_raw_response_wrapper(
            client.get_status,
        )


class CartesiaWithStreamedResponse:
    def __init__(self, client: Cartesia) -> None:
        self.agents = agents.AgentsResourceWithStreamingResponse(client.agents)
        self.access_token = access_token.AccessTokenResourceWithStreamingResponse(client.access_token)
        self.datasets = datasets.DatasetsResourceWithStreamingResponse(client.datasets)
        self.fine_tunes = fine_tunes.FineTunesResourceWithStreamingResponse(client.fine_tunes)
        self.infill = infill.InfillResourceWithStreamingResponse(client.infill)
        self.pronunciation_dicts = pronunciation_dicts.PronunciationDictsResourceWithStreamingResponse(
            client.pronunciation_dicts
        )
        self.stt = stt.SttResourceWithStreamingResponse(client.stt)
        self.tts = tts.TTSResourceWithStreamingResponse(client.tts)
        self.voice_changer = voice_changer.VoiceChangerResourceWithStreamingResponse(client.voice_changer)
        self.voices = voices.VoicesResourceWithStreamingResponse(client.voices)

        self.get_status = to_streamed_response_wrapper(
            client.get_status,
        )


class AsyncCartesiaWithStreamedResponse:
    def __init__(self, client: AsyncCartesia) -> None:
        self.agents = agents.AsyncAgentsResourceWithStreamingResponse(client.agents)
        self.access_token = access_token.AsyncAccessTokenResourceWithStreamingResponse(client.access_token)
        self.datasets = datasets.AsyncDatasetsResourceWithStreamingResponse(client.datasets)
        self.fine_tunes = fine_tunes.AsyncFineTunesResourceWithStreamingResponse(client.fine_tunes)
        self.infill = infill.AsyncInfillResourceWithStreamingResponse(client.infill)
        self.pronunciation_dicts = pronunciation_dicts.AsyncPronunciationDictsResourceWithStreamingResponse(
            client.pronunciation_dicts
        )
        self.stt = stt.AsyncSttResourceWithStreamingResponse(client.stt)
        self.tts = tts.AsyncTTSResourceWithStreamingResponse(client.tts)
        self.voice_changer = voice_changer.AsyncVoiceChangerResourceWithStreamingResponse(client.voice_changer)
        self.voices = voices.AsyncVoicesResourceWithStreamingResponse(client.voices)

        self.get_status = async_to_streamed_response_wrapper(
            client.get_status,
        )


Client = Cartesia

AsyncClient = AsyncCartesia
