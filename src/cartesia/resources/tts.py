# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import ModelSpeed, SupportedLanguage, tts_generate_params, tts_generate_sse_params
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
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
from .._base_client import make_request_options
from ..types.model_speed import ModelSpeed
from ..types.supported_language import SupportedLanguage
from ..types.voice_specifier_param import VoiceSpecifierParam

__all__ = ["TTSResource", "AsyncTTSResource"]


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

    def generate(
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

    async def generate(
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
