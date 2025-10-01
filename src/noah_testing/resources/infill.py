# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, Optional, cast

import httpx

from ..types import RawEncoding, OutputFormatContainer, infill_create_params
from .._types import Body, Omit, Query, Headers, NoneType, NotGiven, FileTypes, omit, not_given
from .._utils import extract_files, maybe_transform, deepcopy_minimal, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.raw_encoding import RawEncoding
from ..types.output_format_container import OutputFormatContainer

__all__ = ["InfillResource", "AsyncInfillResource"]


class InfillResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InfillResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/noah-testing-python#accessing-raw-response-data-eg-headers
        """
        return InfillResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InfillResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/noah-testing-python#with_streaming_response
        """
        return InfillResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        language: str | Omit = omit,
        left_audio: FileTypes | Omit = omit,
        model_id: str | Omit = omit,
        output_format_bit_rate: Optional[int] | Omit = omit,
        output_format_container: OutputFormatContainer | Omit = omit,
        output_format_encoding: Optional[RawEncoding] | Omit = omit,
        output_format_sample_rate: int | Omit = omit,
        right_audio: FileTypes | Omit = omit,
        transcript: str | Omit = omit,
        voice_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Generate audio that smoothly connects two existing audio segments.

        This is
        useful for inserting new speech between existing speech segments while
        maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300
        credits.**

        Infilling is only available on `sonic-2` at this time.

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

          model_id: The ID of the model to use for generating audio

          output_format_bit_rate: Required for `mp3` containers.

          output_format_container: The format of the output audio

          output_format_encoding: Required for `raw` and `wav` containers.

          output_format_sample_rate: The sample rate of the output audio

          transcript: The infill text to generate

          voice_id: The ID of the voice to use for generating audio

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        body = deepcopy_minimal(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format_bit_rate": output_format_bit_rate,
                "output_format_container": output_format_container,
                "output_format_encoding": output_format_encoding,
                "output_format_sample_rate": output_format_sample_rate,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["left_audio"], ["right_audio"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return self._post(
            "/infill/bytes",
            body=maybe_transform(body, infill_create_params.InfillCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncInfillResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInfillResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/noah-testing-python#accessing-raw-response-data-eg-headers
        """
        return AsyncInfillResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInfillResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/noah-testing-python#with_streaming_response
        """
        return AsyncInfillResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        language: str | Omit = omit,
        left_audio: FileTypes | Omit = omit,
        model_id: str | Omit = omit,
        output_format_bit_rate: Optional[int] | Omit = omit,
        output_format_container: OutputFormatContainer | Omit = omit,
        output_format_encoding: Optional[RawEncoding] | Omit = omit,
        output_format_sample_rate: int | Omit = omit,
        right_audio: FileTypes | Omit = omit,
        transcript: str | Omit = omit,
        voice_id: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> None:
        """Generate audio that smoothly connects two existing audio segments.

        This is
        useful for inserting new speech between existing speech segments while
        maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300
        credits.**

        Infilling is only available on `sonic-2` at this time.

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

          model_id: The ID of the model to use for generating audio

          output_format_bit_rate: Required for `mp3` containers.

          output_format_container: The format of the output audio

          output_format_encoding: Required for `raw` and `wav` containers.

          output_format_sample_rate: The sample rate of the output audio

          transcript: The infill text to generate

          voice_id: The ID of the voice to use for generating audio

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        body = deepcopy_minimal(
            {
                "language": language,
                "left_audio": left_audio,
                "model_id": model_id,
                "output_format_bit_rate": output_format_bit_rate,
                "output_format_container": output_format_container,
                "output_format_encoding": output_format_encoding,
                "output_format_sample_rate": output_format_sample_rate,
                "right_audio": right_audio,
                "transcript": transcript,
                "voice_id": voice_id,
            }
        )
        files = extract_files(cast(Mapping[str, object], body), paths=[["left_audio"], ["right_audio"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers["Content-Type"] = "multipart/form-data"
        return await self._post(
            "/infill/bytes",
            body=await async_maybe_transform(body, infill_create_params.InfillCreateParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class InfillResourceWithRawResponse:
    def __init__(self, infill: InfillResource) -> None:
        self._infill = infill

        self.create = to_raw_response_wrapper(
            infill.create,
        )


class AsyncInfillResourceWithRawResponse:
    def __init__(self, infill: AsyncInfillResource) -> None:
        self._infill = infill

        self.create = async_to_raw_response_wrapper(
            infill.create,
        )


class InfillResourceWithStreamingResponse:
    def __init__(self, infill: InfillResource) -> None:
        self._infill = infill

        self.create = to_streamed_response_wrapper(
            infill.create,
        )


class AsyncInfillResourceWithStreamingResponse:
    def __init__(self, infill: AsyncInfillResource) -> None:
        self._infill = infill

        self.create = async_to_streamed_response_wrapper(
            infill.create,
        )
