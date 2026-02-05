# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import json
import logging
import uuid
from types import TracebackType
from typing import TYPE_CHECKING, Any, Mapping, Iterator, Optional, cast, Dict
from typing_extensions import AsyncIterator

import httpx
from pydantic import BaseModel

from ..types import (
    ModelSpeed,
    SupportedLanguage,
    tts_infill_params,
    tts_generate_params,
    tts_generate_sse_params,
)
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
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
from .._streaming import SSEEventStream, AsyncSSEEventStream
from .._exceptions import CartesiaError
from .._base_client import _merge_mappings, make_request_options
from ..types.model_speed import ModelSpeed
from ..types.supported_language import SupportedLanguage
from ..types.websocket_response import WebsocketResponse
from ..types.voice_specifier_param import VoiceSpecifierParam
from ..types.websocket_client_event import WebsocketClientEvent, GenerationRequest
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

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return TTSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TTSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return TTSResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        generation_config: GenerationConfigParam | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
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

          generation_config: Configure the various attributes of the generated speech. These are only for
              `sonic-3` and have no effect on earlier models.

              See
              [Volume, Speed, and Emotion in Sonic-3](/build-with-cartesia/sonic-3/volume-speed-emotion)
              for a guide on this option.

          language: The language that the given voice should speak the transcript in. For valid
              options, see [Models](/build-with-cartesia/tts-models).

          pronunciation_dict_id: The ID of a pronunciation dictionary to use for the generation. Pronunciation
              dictionaries are supported by `sonic-3` models and newer.

          save: Whether to save the generated audio file. When true, the response will include a
              `Cartesia-File-ID` header.

          speed: Use `generation_config.speed` for sonic-3. Speed setting for the model. Defaults
              to `normal`. This feature is experimental and may not work for all voices.
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
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
        generation_config: GenerationConfigParam | Omit = omit,
        language: SupportedLanguage | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
        use_normalized_timestamps: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SSEEventStream:
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

          generation_config: Configure the various attributes of the generated speech. These are only for
              `sonic-3` and have no effect on earlier models.

              See
              [Volume, Speed, and Emotion in Sonic-3](/build-with-cartesia/sonic-3/volume-speed-emotion)
              for a guide on this option.

          language: The language that the given voice should speak the transcript in. For valid
              options, see [Models](/build-with-cartesia/tts-models).

          pronunciation_dict_id: The ID of a pronunciation dictionary to use for the generation. Pronunciation
              dictionaries are supported by `sonic-3` models and newer.

          speed: Use `generation_config.speed` for sonic-3. Speed setting for the model. Defaults
              to `normal`. This feature is experimental and may not work for all voices.
              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        response = self._post(
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx.Response,
        )
        return SSEEventStream(response=response, client=self._client)

    def websocket(
        self,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ):
        """Create a WebSocket connection for real-time TTS streaming.

        Returns a connection that can be used directly.
        """
        manager = self.connect(
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )
        return manager.__enter__()

    def bytes(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,
        generation_config: Optional[tts_generate_params.GenerationConfig] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ):
        """Text to Speech returning an iterator of audio bytes.

        This is a convenience wrapper around generate() that returns an iterator
        directly, allowing you to iterate over chunks without calling .iter_bytes().
        """
        response = self.generate(
            model_id=model_id,
            output_format=output_format,
            transcript=transcript,
            voice=voice,
            duration=duration,
            generation_config=generation_config,
            language=language,
            pronunciation_dict_ids=pronunciation_dict_ids,
            save=save,
            speed=speed,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response.iter_bytes()

    def infill(
        self,
        *,
        language: str | Omit = omit,
        left_audio: FileTypes | Omit = omit,
        model_id: str | Omit = omit,
        output_format: tts_infill_params.OutputFormat | Omit = omit,
        right_audio: FileTypes | Omit = omit,
        transcript: str | Omit = omit,
        voice_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> BinaryAPIResponse:
        """Generate audio that smoothly connects two existing audio segments.

        This is
        useful for inserting new speech between existing speech segments while
        maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300
        credits.**

        At least one of `left_audio` or `right_audio` must be provided.

        As with all generative models, there's some inherent variability, but here's
        some tips we recommend to get the best results from infill:

        - Use longer infill transcripts
          - This gives the model more flexibility to adapt to the rest of the audio
        - Target natural pauses in the audio when deciding where to clip
          - This means you don't need word-level timestamps to be as precise
        - Clip right up to the start and end of the audio segment you want infilled,
          keeping as much silence in the left/right audio segments as possible
          - This helps the model generate more natural transitions

        Args:
          language: The language of the transcript

          model_id: The ID of the model to use for generating audio. Any model other than the first
              `"sonic"` model is supported.

          transcript: The infill text to generate

          voice_id: The ID of the voice to use for generating audio

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        body = deepcopy_minimal(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format": output_format,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["left_audio"], ["right_audio"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/infill/bytes",
            body=maybe_transform(body, tts_infill_params.TTSInfillParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def websocket_connect(
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


class AsyncTTSResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTTSResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTTSResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTTSResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncTTSResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        generation_config: GenerationConfigParam | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
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

          generation_config: Configure the various attributes of the generated speech. These are only for
              `sonic-3` and have no effect on earlier models.

              See
              [Volume, Speed, and Emotion in Sonic-3](/build-with-cartesia/sonic-3/volume-speed-emotion)
              for a guide on this option.

          language: The language that the given voice should speak the transcript in. For valid
              options, see [Models](/build-with-cartesia/tts-models).

          pronunciation_dict_id: The ID of a pronunciation dictionary to use for the generation. Pronunciation
              dictionaries are supported by `sonic-3` models and newer.

          save: Whether to save the generated audio file. When true, the response will include a
              `Cartesia-File-ID` header.

          speed: Use `generation_config.speed` for sonic-3. Speed setting for the model. Defaults
              to `normal`. This feature is experimental and may not work for all voices.
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
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
        generation_config: GenerationConfigParam | Omit = omit,
        language: SupportedLanguage | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
        use_normalized_timestamps: Optional[bool] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncSSEEventStream:
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

          generation_config: Configure the various attributes of the generated speech. These are only for
              `sonic-3` and have no effect on earlier models.

              See
              [Volume, Speed, and Emotion in Sonic-3](/build-with-cartesia/sonic-3/volume-speed-emotion)
              for a guide on this option.

          language: The language that the given voice should speak the transcript in. For valid
              options, see [Models](/build-with-cartesia/tts-models).

          pronunciation_dict_id: The ID of a pronunciation dictionary to use for the generation. Pronunciation
              dictionaries are supported by `sonic-3` models and newer.

          speed: Use `generation_config.speed` for sonic-3. Speed setting for the model. Defaults
              to `normal`. This feature is experimental and may not work for all voices.
              Influences the speed of the generated speech. Faster speeds may reduce
              hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        response = await self._post(
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSseParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=httpx.Response,
        )
        return AsyncSSEEventStream(response=response, client=self._client)

    async def websocket(
        self,
        extra_query: Query = {},
        extra_headers: Headers = {},
        websocket_connection_options: WebsocketConnectionOptions = {},
    ):
        """Create a WebSocket connection for real-time TTS streaming.

        Returns a connection that can be used directly.
        """
        manager = self.connect(
            extra_query=extra_query,
            extra_headers=extra_headers,
            websocket_connection_options=websocket_connection_options,
        )
        return await manager.__aenter__()

    async def bytes(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,
        generation_config: Optional[tts_generate_params.GenerationConfig] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ):
        """Text to Speech returning an async iterator of audio bytes.

        This is a convenience wrapper around generate() that returns an iterator
        directly, allowing you to iterate over chunks without calling .iter_bytes().
        """
        response = await self.generate(
            model_id=model_id,
            output_format=output_format,
            transcript=transcript,
            voice=voice,
            duration=duration,
            generation_config=generation_config,
            language=language,
            pronunciation_dict_ids=pronunciation_dict_ids,
            save=save,
            speed=speed,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response.iter_bytes()

    async def infill(
        self,
        *,
        language: str | Omit = omit,
        left_audio: FileTypes | Omit = omit,
        model_id: str | Omit = omit,
        output_format: tts_infill_params.OutputFormat | Omit = omit,
        right_audio: FileTypes | Omit = omit,
        transcript: str | Omit = omit,
        voice_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncBinaryAPIResponse:
        """Generate audio that smoothly connects two existing audio segments.

        This is
        useful for inserting new speech between existing speech segments while
        maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300
        credits.**

        At least one of `left_audio` or `right_audio` must be provided.

        As with all generative models, there's some inherent variability, but here's
        some tips we recommend to get the best results from infill:

        - Use longer infill transcripts
          - This gives the model more flexibility to adapt to the rest of the audio
        - Target natural pauses in the audio when deciding where to clip
          - This means you don't need word-level timestamps to be as precise
        - Clip right up to the start and end of the audio segment you want infilled,
          keeping as much silence in the left/right audio segments as possible
          - This helps the model generate more natural transitions

        Args:
          language: The language of the transcript

          model_id: The ID of the model to use for generating audio. Any model other than the first
              `"sonic"` model is supported.

          transcript: The infill text to generate

          voice_id: The ID of the voice to use for generating audio

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "audio/wav", **(extra_headers or {})}
        body = deepcopy_minimal(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format": output_format,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["left_audio"], ["right_audio"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/infill/bytes",
            body=await async_maybe_transform(body, tts_infill_params.TTSInfillParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    def websocket_connect(
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
        self.infill = to_custom_raw_response_wrapper(
            tts.infill,
            BinaryAPIResponse,
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
        self.infill = async_to_custom_raw_response_wrapper(
            tts.infill,
            AsyncBinaryAPIResponse,
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
        self.infill = to_custom_streamed_response_wrapper(
            tts.infill,
            StreamedBinaryAPIResponse,
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
        self.infill = async_to_custom_streamed_response_wrapper(
            tts.infill,
            AsyncStreamedBinaryAPIResponse,
        )


class AsyncTTSResourceConnection:
    """Represents a live WebSocket connection to the TTS API"""

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

    def context(self, context_id: Optional[str] = None):
        """Create a context helper for managing conversational flows.

        Args:
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated.

        Returns:
            AsyncWebSocketContext helper for simplified sending and receiving
        """
        if context_id is None:
            context_id = str(uuid.uuid4())
        return AsyncWebSocketContext(self, context_id)


class AsyncTTSResourceConnectionManager:
    """
    Context manager over a `AsyncTTSResourceConnection` that is returned by `tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = await client.tts.websocket_connect(...).enter()
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
        connection = await client.tts.websocket_connect(...).enter()
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
    """Represents a live WebSocket connection to the TTS API"""

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

    def context(self, context_id: Optional[str] = None):
        """Create a context helper for managing conversational flows.

        Args:
            context_id: Unique identifier for this context. If not provided,
                a UUID will be auto-generated.

        Returns:
            WebSocketContext helper for simplified sending and receiving
        """
        if context_id is None:
            context_id = str(uuid.uuid4())
        return WebSocketContext(self, context_id)


class TTSResourceConnectionManager:
    """
    Context manager over a `TTSResourceConnection` that is returned by `tts.websocket_connect()`

    This context manager ensures that the connection will be closed when it exits.

    ---

    Note that if your application doesn't work well with the context manager approach then you
    can call the `.enter()` method directly to initiate a connection.

    **Warning**: You must remember to close the connection with `.close()`.

    ```py
    connection = client.tts.websocket_connect(...).enter()
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
        connection = client.tts.websocket_connect(...).enter()
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
                        "Cartesia-Version": "2025-04-16",
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

# WebSocket context helpers for managing conversational flows.
class WebSocketContext:
    """Context helper for managing WebSocket conversations with automatic context_id handling."""

    def __init__(self, connection: 'TTSResourceConnection', context_id: str):
        self._connection = connection
        self._context_id = context_id
        self._completed = False

    def send(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: VoiceSpecifierParam,
        output_format: Optional[Dict[str, Any]] = None,
        continue_: bool = True,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        **kwargs,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is None:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Build request parameters, excluding omitted values
        request_params = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": output_format,
            "context_id": self._context_id,
            "continue_": continue_,
        }

        # Add optional parameters only if they're not omitted
        if not isinstance(duration, Omit):
            request_params["duration"] = duration
        if not isinstance(language, Omit):
            request_params["language"] = language
        if not isinstance(speed, Omit):
            request_params["speed"] = speed
        if not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        if not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps

        # Add any additional kwargs
        request_params.update(kwargs)

        request = GenerationRequest(**request_params)
        self._connection.send(request)

    def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        # Send a final request with continue_=False to signal completion
        request = GenerationRequest(
            model_id="sonic-3",
            transcript="",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            context_id=self._context_id,
            continue_=False,
        )

        self._connection.send(request)
        self._completed = True

    def receive(self) -> Iterator[WebsocketResponse]:
        """Receive responses filtered to this context only."""
        for event in self._connection:
            # Filter events by context_id
            if hasattr(event, "context_id") and event.context_id == self._context_id:
                yield event
                # Stop iteration when context is done
                if event.type == "done":
                    break
            elif not hasattr(event, "context_id") and event.type in ["done", "error"]:
                # Handle events without context_id (legacy or global events)
                yield event
                if event.type in ["done", "error"]:
                    break


class AsyncWebSocketContext:
    """Async context helper for managing WebSocket conversations with automatic context_id handling."""

    def __init__(self, connection: 'AsyncTTSResourceConnection', context_id: str):
        self._connection = connection
        self._context_id = context_id
        self._completed = False

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: VoiceSpecifierParam,
        output_format: Optional[Dict[str, Any]] = None,
        continue_: bool = True,
        duration: Optional[float] | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        speed: Optional[ModelSpeed] | Omit = omit,
        add_timestamps: Optional[bool] | Omit = omit,
        add_phoneme_timestamps: Optional[bool] | Omit = omit,
        **kwargs,
    ) -> None:
        """Send a generation request with automatic context_id management."""
        if self._completed:
            raise ValueError("Cannot send to completed context. Call no_more_inputs() only once per context.")

        # Default output format
        if output_format is None:
            output_format = {
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            }

        # Build request parameters, excluding omitted values
        request_params = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": output_format,
            "context_id": self._context_id,
            "continue_": continue_,
        }

        # Add optional parameters only if they're not omitted
        if not isinstance(duration, Omit):
            request_params["duration"] = duration
        if not isinstance(language, Omit):
            request_params["language"] = language
        if not isinstance(speed, Omit):
            request_params["speed"] = speed
        if not isinstance(add_timestamps, Omit):
            request_params["add_timestamps"] = add_timestamps
        if not isinstance(add_phoneme_timestamps, Omit):
            request_params["add_phoneme_timestamps"] = add_phoneme_timestamps

        # Add any additional kwargs
        request_params.update(kwargs)

        request = GenerationRequest(**request_params)
        await self._connection.send(request)

    async def no_more_inputs(self) -> None:
        """Signal that no more inputs will be sent for this context."""
        if self._completed:
            return  # Already completed, ignore

        # Send a final request with continue_=False to signal completion
        request = GenerationRequest(
            model_id="sonic-3",
            transcript="",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            context_id=self._context_id,
            continue_=False,
        )

        await self._connection.send(request)
        self._completed = True

    async def receive(self) -> AsyncIterator[WebsocketResponse]:
        """Receive responses filtered to this context only."""
        async for event in self._connection:
            # Filter events by context_id
            if hasattr(event, "context_id") and event.context_id == self._context_id:
                yield event
                # Stop iteration when context is done
                if event.type == "done":
                    break
            elif not hasattr(event, "context_id") and event.type in ["done", "error"]:
                # Handle events without context_id (legacy or global events)
                yield event
                if event.type in ["done", "error"]:
                    break

# Custom Cartesia stuff:
