# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import json
import logging
from types import TracebackType
from typing import TYPE_CHECKING, Any, Iterator, Optional, cast
from typing_extensions import AsyncIterator

import httpx
from pydantic import BaseModel

from ..types import (
    ModelSpeed,
    SupportedLanguage,
    tts_generate_params,
    tts_generate_sse_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._models import construct_type_unchecked
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._exceptions import CartesiaError
from .._base_client import _merge_mappings, make_request_options
from ..types.model_speed import ModelSpeed
from ..types.supported_language import SupportedLanguage
from ..types.websocket_response import WebsocketResponse
from ..types.voice_specifier_param import VoiceSpecifierParam
from ..types.websocket_client_event import WebsocketClientEvent
from ..types.generation_config_param import GenerationConfigParam
from ..types.websocket_client_event_param import WebsocketClientEventParam
from ..types.websocket_connection_options import WebsocketConnectionOptions

if TYPE_CHECKING:
    from websockets.sync.client import ClientConnection as WebsocketConnection
    from websockets.asyncio.client import ClientConnection as AsyncWebsocketConnection

    from .._client import Cartesia, AsyncCartesia

__all__ = ["TTSResource", "AsyncTTSResource"]

log: logging.Logger = logging.getLogger(__name__)


class TTSResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TTSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python-internal#accessing-raw-response-data-eg-headers
        """
        return TTSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TTSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python-internal#with_streaming_response
        """
        return TTSResourceWithStreamingResponse(self)

    def connect(
        self,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ) -> TTSResourceConnectionManager:
        return TTSResourceConnectionManager(
            client=self._client,
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )

    def generate(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,
        generation_config: Optional[GenerationConfigParam] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """
        Text to Speech (Bytes)

        Args:
          model_id: The ID of the model to use for the generation. See
              [Models](/build-with-cartesia/tts-models) for available models.

          duration: The maximum duration of the audio in seconds. You do not usually need to specify
              this. If the duration is not appropriate for the length of the transcript, the
              output audio may be truncated.

          generation_config: Configure the various attributes of the generated speech. These controls are
              only available for `sonic-3-preview` and will have no effect on earlier models.

          language: The language that the given voice should speak the transcript in.

              Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
              Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
              Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).

          pronunciation_dict_ids: A list of pronunciation dict IDs to use for the generation. This will be applied
              in addition to the pinned pronunciation dict, which will be treated as the first
              element of the list. If there are conflicts with dict items, the latest dict
              will take precedence.

          save: Whether to save the generated audio file. When true, the response will include a
              `Cartesia-File-ID` header.

          speed: > This feature is experimental and may not work for all voices.

              Speed setting for the model. Defaults to `normal`.

              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        return self._post(
            "/tts/bytes",
            body=maybe_transform(
                {
                    "model_id": model_id,
                    "output_format": output_format,
                    "transcript": transcript,
                    "voice": voice,
                    "duration": duration,
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_ids": pronunciation_dict_ids,
                    "save": save,
                    "speed": speed,
                },
                tts_generate_params.TTSGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def generate_sse(
        self,
        *,
        model_id: str,
        output_format: tts_generate_sse_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        context_id: Optional[str] | Omit = omit,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        use_normalized_timestamps: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Text to Speech (SSE)

        Args:
          model_id: The ID of the model to use for the generation. See
              [Models](/build-with-cartesia/tts-models) for available models.

          add_phoneme_timestamps: Whether to return phoneme-level timestamps. If `false` (default), no phoneme
              timestamps will be produced. If `true`, the server will return timestamp events
              containing phoneme-level timing information.

          add_timestamps: Whether to return word-level timestamps. If `false` (default), no word
              timestamps will be produced at all. If `true`, the server will return timestamp
              events containing word-level timing information.

          context_id: Optional context ID for this request.

          duration: The maximum duration of the audio in seconds. You do not usually need to specify
              this. If the duration is not appropriate for the length of the transcript, the
              output audio may be truncated.

          language: The language that the given voice should speak the transcript in.

              Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
              Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
              Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).

          pronunciation_dict_ids: A list of pronunciation dict IDs to use for the generation. This will be applied
              in addition to the pinned pronunciation dict, which will be treated as the first
              element of the list. If there are conflicts with dict items, the latest dict
              will take precedence.

          speed: > This feature is experimental and may not work for all voices.

              Speed setting for the model. Defaults to `normal`.

              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/tts/sse",
            body=maybe_transform(
                {
                    "model_id": model_id,
                    "output_format": output_format,
                    "transcript": transcript,
                    "voice": voice,
                    "add_phoneme_timestamps": add_phoneme_timestamps,
                    "add_timestamps": add_timestamps,
                    "context_id": context_id,
                    "duration": duration,
                    "language": language,
                    "pronunciation_dict_ids": pronunciation_dict_ids,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncTTSResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTTSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python-internal#accessing-raw-response-data-eg-headers
        """
        return AsyncTTSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTTSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python-internal#with_streaming_response
        """
        return AsyncTTSResourceWithStreamingResponse(self)

    def connect(
        self,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ) -> AsyncTTSResourceConnectionManager:
        return AsyncTTSResourceConnectionManager(
            client=self._client,
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )

    async def generate(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,
        generation_config: Optional[GenerationConfigParam] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """
        Text to Speech (Bytes)

        Args:
          model_id: The ID of the model to use for the generation. See
              [Models](/build-with-cartesia/tts-models) for available models.

          duration: The maximum duration of the audio in seconds. You do not usually need to specify
              this. If the duration is not appropriate for the length of the transcript, the
              output audio may be truncated.

          generation_config: Configure the various attributes of the generated speech. These controls are
              only available for `sonic-3-preview` and will have no effect on earlier models.

          language: The language that the given voice should speak the transcript in.

              Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
              Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
              Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).

          pronunciation_dict_ids: A list of pronunciation dict IDs to use for the generation. This will be applied
              in addition to the pinned pronunciation dict, which will be treated as the first
              element of the list. If there are conflicts with dict items, the latest dict
              will take precedence.

          save: Whether to save the generated audio file. When true, the response will include a
              `Cartesia-File-ID` header.

          speed: > This feature is experimental and may not work for all voices.

              Speed setting for the model. Defaults to `normal`.

              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        return await self._post(
            "/tts/bytes",
            body=await async_maybe_transform(
                {
                    "model_id": model_id,
                    "output_format": output_format,
                    "transcript": transcript,
                    "voice": voice,
                    "duration": duration,
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_ids": pronunciation_dict_ids,
                    "save": save,
                    "speed": speed,
                },
                tts_generate_params.TTSGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def generate_sse(
        self,
        *,
        model_id: str,
        output_format: tts_generate_sse_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        context_id: Optional[str] | Omit = omit,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        use_normalized_timestamps: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """
        Text to Speech (SSE)

        Args:
          model_id: The ID of the model to use for the generation. See
              [Models](/build-with-cartesia/tts-models) for available models.

          add_phoneme_timestamps: Whether to return phoneme-level timestamps. If `false` (default), no phoneme
              timestamps will be produced. If `true`, the server will return timestamp events
              containing phoneme-level timing information.

          add_timestamps: Whether to return word-level timestamps. If `false` (default), no word
              timestamps will be produced at all. If `true`, the server will return timestamp
              events containing word-level timing information.

          context_id: Optional context ID for this request.

          duration: The maximum duration of the audio in seconds. You do not usually need to specify
              this. If the duration is not appropriate for the length of the transcript, the
              output audio may be truncated.

          language: The language that the given voice should speak the transcript in.

              Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
              Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
              Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).

          pronunciation_dict_ids: A list of pronunciation dict IDs to use for the generation. This will be applied
              in addition to the pinned pronunciation dict, which will be treated as the first
              element of the list. If there are conflicts with dict items, the latest dict
              will take precedence.

          speed: > This feature is experimental and may not work for all voices.

              Speed setting for the model. Defaults to `normal`.

              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/tts/sse",
            body=await async_maybe_transform(
                {
                    "model_id": model_id,
                    "output_format": output_format,
                    "transcript": transcript,
                    "voice": voice,
                    "add_phoneme_timestamps": add_phoneme_timestamps,
                    "add_timestamps": add_timestamps,
                    "context_id": context_id,
                    "duration": duration,
                    "language": language,
                    "pronunciation_dict_ids": pronunciation_dict_ids,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class TTSResourceWithRawResponse:
    def __init__(self, tts: TTSResource) -> None:
        self._tts = tts

        self.generate = to_custom_raw_response_wrapper(
            tts.generate,
            BinaryAPIResponse,
        )
        self.generate_sse = to_raw_response_wrapper(
            tts.generate_sse,
        )


class AsyncTTSResourceWithRawResponse:
    def __init__(self, tts: AsyncTTSResource) -> None:
        self._tts = tts

        self.generate = async_to_custom_raw_response_wrapper(
            tts.generate,
            AsyncBinaryAPIResponse,
        )
        self.generate_sse = async_to_raw_response_wrapper(
            tts.generate_sse,
        )


class TTSResourceWithStreamingResponse:
    def __init__(self, tts: TTSResource) -> None:
        self._tts = tts

        self.generate = to_custom_streamed_response_wrapper(
            tts.generate,
            StreamedBinaryAPIResponse,
        )
        self.generate_sse = to_streamed_response_wrapper(
            tts.generate_sse,
        )


class AsyncTTSResourceWithStreamingResponse:
    def __init__(self, tts: AsyncTTSResource) -> None:
        self._tts = tts

        self.generate = async_to_custom_streamed_response_wrapper(
            tts.generate,
            AsyncStreamedBinaryAPIResponse,
        )
        self.generate_sse = async_to_streamed_response_wrapper(
            tts.generate_sse,
        )


class AsyncTTSResourceConnection:
    """Represents a live websocket connection to the TTS API"""

    _connection: AsyncWebsocketConnection

    def __init__(self, connection: AsyncWebsocketConnection) -> None:
        self._connection = connection

    async def __aiter__(self) -> AsyncIterator[WebsocketResponse]:
        """
        An infinite-iterator that will continue to yield events until
        the connection is closed.
        """
        from websockets.exceptions import ConnectionClosedOK

        try:
            while True:
                yield await self.recv()
        except ConnectionClosedOK:
            return

    async def recv(self) -> WebsocketResponse:
        """
        Receive the next message from the connection and parses it into a `WebsocketResponse` object.

        Canceling this method is safe. There's no risk of losing data.
        """
        return self.parse_event(await self.recv_bytes())

    async def recv_bytes(self) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into a `WebsocketResponse` object like `.recv()` does,
        then you can call `.parse_event(data)`.
        """
        message = await self._connection.recv(decode=False)
        log.debug(f"Received websocket message: %s", message)
        return message

    async def send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        data = (
            event.to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
            if isinstance(event, BaseModel)
            else json.dumps(await async_maybe_transform(event, WebsocketClientEventParam))
        )
        await self._connection.send(data)

    async def close(self, *, code: int = 1000, reason: str = "") -> None:
        await self._connection.close(code=code, reason=reason)

    def parse_event(self, data: str | bytes) -> WebsocketResponse:
        """
        Converts a raw `str` or `bytes` message into a `WebsocketResponse` object.

        This is helpful if you're using `.recv_bytes()`.
        """
        return cast(
            WebsocketResponse, construct_type_unchecked(value=json.loads(data), type_=cast(Any, WebsocketResponse))
        )


class AsyncTTSResourceConnectionManager:
    """
    Context manager over a `AsyncTTSResourceConnection` that is returned by `tts.connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = await client.tts.connect(...).enter()
    # ...
    await connection.close()
    ```
    """

    def __init__(
        self,
        *,
        client: AsyncCartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebsocketConnectionOptions,
    ) -> None:
        self.__client = client
        self.__connection: AsyncTTSResourceConnection | None = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options

    async def __aenter__(self) -> AsyncTTSResourceConnection:
        """
        👋 If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with `.close()`.

        ```py
        connection = await client.tts.connect(...).enter()
        # ...
        await connection.close()
        ```
        """
        try:
            from websockets.asyncio.client import connect
        except ImportError as exc:
            raise CartesiaError("You need to install `cartesia[websockets]` to use this method") from exc

        url = self._prepare_url().copy_with(
            params={
                **self.__client.base_url.params,
                **self.__extra_query,
            },
        )
        log.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            log.debug("Connection options: %s", self.__websocket_connection_options)

        self.__connection = AsyncTTSResourceConnection(
            await connect(
                str(url),
                user_agent_header=self.__client.user_agent,
                additional_headers=_merge_mappings(
                    {
                        **self.__client.auth_headers,
                    },
                    self.__extra_headers,
                ),
                **self.__websocket_connection_options,
            )
        )

        return self.__connection

    enter = __aenter__

    def _prepare_url(self) -> httpx.URL:
        if self.__client.websocket_base_url is not None:
            base_url = httpx.URL(self.__client.websocket_base_url)
        else:
            base_url = self.__client._base_url.copy_with(scheme="wss")

        merge_raw_path = base_url.raw_path.rstrip(b"/") + b"/tts/websocket"
        return base_url.copy_with(raw_path=merge_raw_path)

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.__connection is not None:
            await self.__connection.close()


class TTSResourceConnection:
    """Represents a live websocket connection to the TTS API"""

    _connection: WebsocketConnection

    def __init__(self, connection: WebsocketConnection) -> None:
        self._connection = connection

    def __iter__(self) -> Iterator[WebsocketResponse]:
        """
        An infinite-iterator that will continue to yield events until
        the connection is closed.
        """
        from websockets.exceptions import ConnectionClosedOK

        try:
            while True:
                yield self.recv()
        except ConnectionClosedOK:
            return

    def recv(self) -> WebsocketResponse:
        """
        Receive the next message from the connection and parses it into a `WebsocketResponse` object.

        Canceling this method is safe. There's no risk of losing data.
        """
        return self.parse_event(self.recv_bytes())

    def recv_bytes(self) -> bytes:
        """Receive the next message from the connection as raw bytes.

        Canceling this method is safe. There's no risk of losing data.

        If you want to parse the message into a `WebsocketResponse` object like `.recv()` does,
        then you can call `.parse_event(data)`.
        """
        message = self._connection.recv(decode=False)
        log.debug(f"Received websocket message: %s", message)
        return message

    def send(self, event: WebsocketClientEvent | WebsocketClientEventParam) -> None:
        data = (
            event.to_json(use_api_names=True, exclude_defaults=True, exclude_unset=True)
            if isinstance(event, BaseModel)
            else json.dumps(maybe_transform(event, WebsocketClientEventParam))
        )
        self._connection.send(data)

    def close(self, *, code: int = 1000, reason: str = "") -> None:
        self._connection.close(code=code, reason=reason)

    def parse_event(self, data: str | bytes) -> WebsocketResponse:
        """
        Converts a raw `str` or `bytes` message into a `WebsocketResponse` object.

        This is helpful if you're using `.recv_bytes()`.
        """
        return cast(
            WebsocketResponse, construct_type_unchecked(value=json.loads(data), type_=cast(Any, WebsocketResponse))
        )


class TTSResourceConnectionManager:
    """
    Context manager over a `TTSResourceConnection` that is returned by `tts.connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = client.tts.connect(...).enter()
    # ...
    connection.close()
    ```
    """

    def __init__(
        self,
        *,
        client: Cartesia,
        extra_query: Query,
        extra_headers: Headers,
        websocket_connection_options: WebsocketConnectionOptions,
    ) -> None:
        self.__client = client
        self.__connection: TTSResourceConnection | None = None
        self.__extra_query = extra_query
        self.__extra_headers = extra_headers
        self.__websocket_connection_options = websocket_connection_options

    def __enter__(self) -> TTSResourceConnection:
        """
        👋 If your application doesn't work well with the context manager approach then you
        can call this method directly to initiate a connection.

        **Warning**: You must remember to close the connection with `.close()`.

        ```py
        connection = client.tts.connect(...).enter()
        # ...
        connection.close()
        ```
        """
        try:
            from websockets.sync.client import connect
        except ImportError as exc:
            raise CartesiaError("You need to install `cartesia[websockets]` to use this method") from exc

        url = self._prepare_url().copy_with(
            params={
                **self.__client.base_url.params,
                **self.__extra_query,
            },
        )
        log.debug("Connecting to %s", url)
        if self.__websocket_connection_options:
            log.debug("Connection options: %s", self.__websocket_connection_options)

        self.__connection = TTSResourceConnection(
            connect(
                str(url),
                user_agent_header=self.__client.user_agent,
                additional_headers=_merge_mappings(
                    {
                        **self.__client.auth_headers,
                    },
                    self.__extra_headers,
                ),
                **self.__websocket_connection_options,
            )
        )

        return self.__connection

    enter = __enter__

    def _prepare_url(self) -> httpx.URL:
        if self.__client.websocket_base_url is not None:
            base_url = httpx.URL(self.__client.websocket_base_url)
        else:
            base_url = self.__client._base_url.copy_with(scheme="wss")

        merge_raw_path = base_url.raw_path.rstrip(b"/") + b"/tts/websocket"
        return base_url.copy_with(raw_path=merge_raw_path)

    def __exit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if self.__connection is not None:
            self.__connection.close()
