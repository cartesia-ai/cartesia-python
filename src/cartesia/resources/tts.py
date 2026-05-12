# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Any, AsyncIterator, Iterator, Mapping, Optional, cast
from typing_extensions import deprecated

import httpx

from ..types import (
    ModelSpeed,
    SupportedLanguage,
    tts_infill_params,
    tts_generate_params,
    tts_generate_sse_params,
)
from .._files import deepcopy_with_paths
from .._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, maybe_transform, async_maybe_transform
from .._compat import cached_property
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
from .._streaming import Stream, AsyncStream
from .._base_client import make_request_options
from ..types.model_speed import ModelSpeed
from ..lib.tts.backcompat import (
    BackcompatWebSocketTtsOutput as BackcompatWebSocketTtsOutput,
    BackcompatTTSResourceConnection as BackcompatTTSResourceConnection,
    AsyncBackcompatTTSResourceConnection as AsyncBackcompatTTSResourceConnection,
)
from ..types.tts_sse_event import TTSSSEEvent
from ..types.supported_language import SupportedLanguage
from ..types.voice_specifier_param import VoiceSpecifierParam
from ..types.generation_config_param import GenerationConfigParam

__all__ = ["TTSResource", "AsyncTTSResource"]


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
        Text-to-Speech (Bytes).

        The simplest way to stream generated audio.

        See
        [Compare TTS Endpoints](https://docs.cartesia.ai/use-the-api/compare-tts-endpoints)
        for details.

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

          speed: Speed setting for the model. Defaults to `normal`. This feature is experimental
              and may not work for all voices. Influences the speed of the generated speech.
              Faster speeds may reduce hallucination rate.

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
    ) -> Stream[TTSSSEEvent]:
        """
        Text-to-Speech (SSE).

        Supports:

        - Streaming
        - Timestamps
        - context_id without transcript buffering

        See
        [Compare TTS Endpoints](https://docs.cartesia.ai/use-the-api/compare-tts-endpoints)
        for details.

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

          speed: Speed setting for the model. Defaults to `normal`. This feature is experimental
              and may not work for all voices. Influences the speed of the generated speech.
              Faster speeds may reduce hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSSEParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, TTSSSEEvent),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=Stream[TTSSSEEvent],
        )

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
        """
        Infill (Bytes).

        Generate audio that smoothly connects two existing audio segments. This is
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
        body = deepcopy_with_paths(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format": output_format,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            },
            [["left_audio"], ["right_audio"]],
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

    @deprecated("bytes() is deprecated; use .generate() instead")
    def bytes(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,  # noqa: ARG002
        generation_config: GenerationConfigParam | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Iterator[bytes]:
        """
        Text-to-speech (Bytes).

        .. deprecated::
            Use :meth:`generate` instead.
        """

        response = self.generate(
            model_id=model_id,
            output_format=output_format,
            transcript=transcript,
            voice=voice,
            generation_config=generation_config,
            language=language,
            pronunciation_dict_id=pronunciation_dict_id,
            save=save,
            speed=speed,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response.iter_bytes()

    sse = generate_sse  # alias for backward compatibility

    # def websocket_connect(
    #     self,
    #     extra_query: Query = {},
    #     extra_headers: Headers = {},
    #     websocket_connection_options: WebSocketConnectionOptions = {},
    # ) -> TTSResourceConnectionManager:
    #     """Text-to-Speech (WebSocket).

    #     Supports:
    #       - Streaming
    #       - Long-lived connections allow for lower latency by reusing a live network connection
    #       - Timestamps
    #       - Multiple TTS [contexts](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) over the same connection
    #       - [Context flushing](https://docs.cartesia.ai/use-the-api/tts-websocket/context-flushing-and-flush-i-ds)
    #       - [Transcript buffering](https://docs.cartesia.ai/use-the-api/tts-websocket/buffering)
    #     """

    #     return TTSResourceConnectionManager(
    #         client=self._client,
    #         extra_query=extra_query,
    #         extra_headers=extra_headers,
    #         websocket_connection_options=websocket_connection_options,
    #     )

    # def websocket(
    #     self,
    #     extra_query: Query = {},
    #     extra_headers: Headers = {},
    #     websocket_connection_options: WebSocketConnectionOptions = {},
    # ) -> BackcompatTTSResourceConnection:
    #     """
    #     SDK v2 compatible Text-to-Speech (WebSocket).
    #     """

    #     return BackcompatTTSResourceConnection(
    #         TTSResourceConnectionManager(
    #             client=self._client,
    #             extra_query=extra_query,
    #             extra_headers=extra_headers,
    #             websocket_connection_options=websocket_connection_options,
    #         )
    #     )


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
        Text-to-Speech (Bytes).

        The simplest way to stream generated audio.

        See
        [Compare TTS Endpoints](https://docs.cartesia.ai/use-the-api/compare-tts-endpoints)
        for details.

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

          speed: Speed setting for the model. Defaults to `normal`. This feature is experimental
              and may not work for all voices. Influences the speed of the generated speech.
              Faster speeds may reduce hallucination rate.

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
    ) -> AsyncStream[TTSSSEEvent]:
        """
        Text-to-Speech (SSE).

        Supports:

        - Streaming
        - Timestamps
        - context_id without transcript buffering

        See
        [Compare TTS Endpoints](https://docs.cartesia.ai/use-the-api/compare-tts-endpoints)
        for details.

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

          speed: Speed setting for the model. Defaults to `normal`. This feature is experimental
              and may not work for all voices. Influences the speed of the generated speech.
              Faster speeds may reduce hallucination rate.

          use_normalized_timestamps: Whether to use normalized timestamps (True) or original timestamps (False).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "text/event-stream", **(extra_headers or {})}
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
                    "generation_config": generation_config,
                    "language": language,
                    "pronunciation_dict_id": pronunciation_dict_id,
                    "speed": speed,
                    "use_normalized_timestamps": use_normalized_timestamps,
                },
                tts_generate_sse_params.TTSGenerateSSEParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=cast(Any, TTSSSEEvent),  # Union types cannot be passed in as arguments in the type system
            stream=True,
            stream_cls=AsyncStream[TTSSSEEvent],
        )

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
        """
        Infill (Bytes).

        Generate audio that smoothly connects two existing audio segments. This is
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
        body = deepcopy_with_paths(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format": output_format,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            },
            [["left_audio"], ["right_audio"]],
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

    @deprecated("bytes() is deprecated; use .generate() instead")
    async def bytes(
        self,
        *,
        model_id: str,
        output_format: tts_generate_params.OutputFormat,
        transcript: str,
        voice: VoiceSpecifierParam,
        duration: Optional[float] | Omit = omit,  # noqa: ARG002
        generation_config: GenerationConfigParam | Omit = omit,
        language: Optional[SupportedLanguage] | Omit = omit,
        pronunciation_dict_id: Optional[str] | Omit = omit,
        save: Optional[bool] | Omit = omit,
        speed: ModelSpeed | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncIterator[bytes]:
        """
        Text-to-Speech (Bytes).

        .. deprecated::
            Use :meth:`generate` instead.
        """

        response = await self.generate(
            model_id=model_id,
            output_format=output_format,
            transcript=transcript,
            voice=voice,
            generation_config=generation_config,
            language=language,
            pronunciation_dict_id=pronunciation_dict_id,
            save=save,
            speed=speed,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )
        return response.iter_bytes()

    sse = generate_sse  # Alias for backward compatibility

    # def websocket_connect(
    #     self,
    #     extra_query: Query = {},
    #     extra_headers: Headers = {},
    #     websocket_connection_options: WebSocketConnectionOptions = {},
    # ) -> AsyncTTSResourceConnectionManager:
    #     """Text-to-Speech (WebSocket).

    #     Supports:
    #       - Streaming
    #       - Long-lived connections allow for lower latency by reusing a live network connection
    #       - Timestamps
    #       - Multiple TTS [contexts](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) over the same connection
    #       - [Context flushing](https://docs.cartesia.ai/use-the-api/tts-websocket/context-flushing-and-flush-i-ds)
    #       - [Transcript buffering](https://docs.cartesia.ai/use-the-api/tts-websocket/buffering)
    #     """

    #     return AsyncTTSResourceConnectionManager(
    #         client=self._client,
    #         extra_query=extra_query,
    #         extra_headers=extra_headers,
    #         websocket_connection_options=websocket_connection_options,
    #     )

    # async def websocket(
    #     self,
    #     extra_query: Query = {},
    #     extra_headers: Headers = {},
    #     websocket_connection_options: WebSocketConnectionOptions = {},
    # ) -> AsyncBackcompatTTSResourceConnection:
    #     """
    #     SDK v2 compatible Text-to-Speech (WebSocket).
    #     """

    #     return AsyncBackcompatTTSResourceConnection(
    #         AsyncTTSResourceConnectionManager(
    #             client=self._client,
    #             extra_query=extra_query,
    #             extra_headers=extra_headers,
    #             websocket_connection_options=websocket_connection_options,
    #         )
    #     )


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

        self.sse = self.generate_sse  # Alias for backward compatibility


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

        self.sse = self.generate_sse  # Alias for backward compatibility


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

        self.sse = self.generate_sse  # Alias for backward compatibility


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

        self.sse = self.generate_sse  # Alias for backward compatibility
