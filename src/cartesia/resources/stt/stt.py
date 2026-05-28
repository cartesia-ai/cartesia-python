# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Mapping, Optional, cast
from typing_extensions import Literal

import httpx

from ...types import STTEncoding, STTBatchModel, stt_transcribe_params
from ..._files import deepcopy_with_paths
from ..._types import Body, Omit, Query, Headers, NotGiven, FileTypes, omit, not_given
from ..._utils import extract_files, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .auto_finalize import AutoFinalizeResource, AsyncAutoFinalizeResource
from ..._base_client import make_request_options
from .manual_finalize import ManualFinalizeResource, AsyncManualFinalizeResource
from ...types.stt_encoding import STTEncoding
from ...types.stt_batch_model import STTBatchModel
from ...types.stt_transcribe_response import STTTranscribeResponse

__all__ = ["STTResource", "AsyncSTTResource"]


class STTResource(SyncAPIResource):
    @cached_property
    def auto_finalize(self) -> AutoFinalizeResource:
        return AutoFinalizeResource(self._client)

    @cached_property
    def manual_finalize(self) -> ManualFinalizeResource:
        return ManualFinalizeResource(self._client)

    @cached_property
    def with_raw_response(self) -> STTResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return STTResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> STTResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return STTResourceWithStreamingResponse(self)

    def transcribe(
        self,
        *,
        file: FileTypes,
        model: STTBatchModel,
        encoding: Optional[STTEncoding] | Omit = omit,
        sample_rate: Optional[int] | Omit = omit,
        language: Literal[
            "en",
            "zh",
            "de",
            "es",
            "ru",
            "ko",
            "fr",
            "ja",
            "pt",
            "tr",
            "pl",
            "ca",
            "nl",
            "ar",
            "sv",
            "it",
            "id",
            "hi",
            "fi",
            "vi",
            "he",
            "uk",
            "el",
            "ms",
            "cs",
            "ro",
            "da",
            "hu",
            "ta",
            "no",
            "th",
            "ur",
            "hr",
            "bg",
            "lt",
            "la",
            "mi",
            "ml",
            "cy",
            "sk",
            "te",
            "fa",
            "lv",
            "bn",
            "sr",
            "az",
            "sl",
            "kn",
            "et",
            "mk",
            "br",
            "eu",
            "is",
            "hy",
            "ne",
            "mn",
            "bs",
            "kk",
            "sq",
            "sw",
            "gl",
            "mr",
            "pa",
            "si",
            "km",
            "sn",
            "yo",
            "so",
            "af",
            "oc",
            "ka",
            "be",
            "tg",
            "sd",
            "gu",
            "am",
            "yi",
            "lo",
            "uz",
            "fo",
            "ht",
            "ps",
            "tk",
            "nn",
            "mt",
            "sa",
            "lb",
            "my",
            "bo",
            "tl",
            "mg",
            "as",
            "tt",
            "haw",
            "ln",
            "ha",
            "ba",
            "jw",
            "su",
            "yue",
        ]
        | str
        | Omit = omit,
        timestamp_granularities: List[Literal["word"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> STTTranscribeResponse:
        """
        Transcribes audio files into text.

        **Supported audio formats:** flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav,
        webm

        See [the API docs](https://docs.cartesia.ai/api-reference/stt/transcribe) for
        details.

        Args:
          model: Models that support batch speech-to-text transcription. See
              [the docs](https://docs.cartesia.ai/api-reference/stt/transcribe#body-model) for
              all options.

          encoding: The encoding format for audio data sent to the STT WebSocket.

          sample_rate: The sample rate of the audio in Hz.

          language: The language of the input audio in ISO-639-1 format. Defaults to `en`.

          timestamp_granularities: The timestamp granularities to populate for this transcription. Currently only
              `word` level timestamps are supported.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "file": file,
                "model": model,
                "language": language,
                "timestamp_granularities": timestamp_granularities,
            },
            [["file"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/stt",
            body=maybe_transform(body, stt_transcribe_params.STTTranscribeParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "encoding": encoding,
                        "sample_rate": sample_rate,
                    },
                    stt_transcribe_params.STTTranscribeParams,
                ),
            ),
            cast_to=STTTranscribeResponse,
        )


class AsyncSTTResource(AsyncAPIResource):
    @cached_property
    def auto_finalize(self) -> AsyncAutoFinalizeResource:
        return AsyncAutoFinalizeResource(self._client)

    @cached_property
    def manual_finalize(self) -> AsyncManualFinalizeResource:
        return AsyncManualFinalizeResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSTTResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSTTResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSTTResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncSTTResourceWithStreamingResponse(self)

    async def transcribe(
        self,
        *,
        file: FileTypes,
        model: STTBatchModel,
        encoding: Optional[STTEncoding] | Omit = omit,
        sample_rate: Optional[int] | Omit = omit,
        language: Literal[
            "en",
            "zh",
            "de",
            "es",
            "ru",
            "ko",
            "fr",
            "ja",
            "pt",
            "tr",
            "pl",
            "ca",
            "nl",
            "ar",
            "sv",
            "it",
            "id",
            "hi",
            "fi",
            "vi",
            "he",
            "uk",
            "el",
            "ms",
            "cs",
            "ro",
            "da",
            "hu",
            "ta",
            "no",
            "th",
            "ur",
            "hr",
            "bg",
            "lt",
            "la",
            "mi",
            "ml",
            "cy",
            "sk",
            "te",
            "fa",
            "lv",
            "bn",
            "sr",
            "az",
            "sl",
            "kn",
            "et",
            "mk",
            "br",
            "eu",
            "is",
            "hy",
            "ne",
            "mn",
            "bs",
            "kk",
            "sq",
            "sw",
            "gl",
            "mr",
            "pa",
            "si",
            "km",
            "sn",
            "yo",
            "so",
            "af",
            "oc",
            "ka",
            "be",
            "tg",
            "sd",
            "gu",
            "am",
            "yi",
            "lo",
            "uz",
            "fo",
            "ht",
            "ps",
            "tk",
            "nn",
            "mt",
            "sa",
            "lb",
            "my",
            "bo",
            "tl",
            "mg",
            "as",
            "tt",
            "haw",
            "ln",
            "ha",
            "ba",
            "jw",
            "su",
            "yue",
        ]
        | str
        | Omit = omit,
        timestamp_granularities: List[Literal["word"]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> STTTranscribeResponse:
        """
        Transcribes audio files into text.

        **Supported audio formats:** flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav,
        webm

        See [the API docs](https://docs.cartesia.ai/api-reference/stt/transcribe) for
        details.

        Args:
          model: Models that support batch speech-to-text transcription. See
              [the docs](https://docs.cartesia.ai/api-reference/stt/transcribe#body-model) for
              all options.

          encoding: The encoding format for audio data sent to the STT WebSocket.

          sample_rate: The sample rate of the audio in Hz.

          language: The language of the input audio in ISO-639-1 format. Defaults to `en`.

          timestamp_granularities: The timestamp granularities to populate for this transcription. Currently only
              `word` level timestamps are supported.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths(
            {
                "file": file,
                "model": model,
                "language": language,
                "timestamp_granularities": timestamp_granularities,
            },
            [["file"]],
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/stt",
            body=await async_maybe_transform(body, stt_transcribe_params.STTTranscribeParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "encoding": encoding,
                        "sample_rate": sample_rate,
                    },
                    stt_transcribe_params.STTTranscribeParams,
                ),
            ),
            cast_to=STTTranscribeResponse,
        )


class STTResourceWithRawResponse:
    def __init__(self, stt: STTResource) -> None:
        self._stt = stt

        self.transcribe = to_raw_response_wrapper(
            stt.transcribe,
        )


class AsyncSTTResourceWithRawResponse:
    def __init__(self, stt: AsyncSTTResource) -> None:
        self._stt = stt

        self.transcribe = async_to_raw_response_wrapper(
            stt.transcribe,
        )


class STTResourceWithStreamingResponse:
    def __init__(self, stt: STTResource) -> None:
        self._stt = stt

        self.transcribe = to_streamed_response_wrapper(
            stt.transcribe,
        )


class AsyncSTTResourceWithStreamingResponse:
    def __init__(self, stt: AsyncSTTResource) -> None:
        self._stt = stt

        self.transcribe = async_to_streamed_response_wrapper(
            stt.transcribe,
        )
