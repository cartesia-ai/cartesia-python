# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Mapping, cast

import httpx

from ..types import watermark_detect_params
from .._files import deepcopy_with_paths
from .._types import Body, Query, Headers, NotGiven, FileTypes, not_given
from .._utils import extract_files, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.watermark_detect_response import WatermarkDetectResponse

__all__ = ["WatermarkResource", "AsyncWatermarkResource"]


class WatermarkResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WatermarkResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return WatermarkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WatermarkResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return WatermarkResourceWithStreamingResponse(self)

    def detect(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WatermarkDetectResponse:
        """Check audio for a Cartesia watermark.

        Requires a paid plan.

        Args:
          file: Audio file to check, between 5 seconds and 5 minutes long, up to 32 MiB.
              Supported formats are FLAC, M4A, MP3, MP4, MPEG, MPGA, OGA, OGG, WAV, and WebM.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return self._post(
            "/v1/watermark/detect",
            body=maybe_transform(body, watermark_detect_params.WatermarkDetectParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WatermarkDetectResponse,
        )


class AsyncWatermarkResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWatermarkResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWatermarkResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWatermarkResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/cartesia-ai/cartesia-python#with_streaming_response
        """
        return AsyncWatermarkResourceWithStreamingResponse(self)

    async def detect(
        self,
        *,
        file: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> WatermarkDetectResponse:
        """Check audio for a Cartesia watermark.

        Requires a paid plan.

        Args:
          file: Audio file to check, between 5 seconds and 5 minutes long, up to 32 MiB.
              Supported formats are FLAC, M4A, MP3, MP4, MPEG, MPGA, OGA, OGG, WAV, and WebM.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        body = deepcopy_with_paths({"file": file}, [["file"]])
        files = extract_files(cast(Mapping[str, object], body), paths=[["file"]])
        # It should be noted that the actual Content-Type header that will be
        # sent to the server will contain a `boundary` parameter, e.g.
        # multipart/form-data; boundary=---abc--
        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}
        return await self._post(
            "/v1/watermark/detect",
            body=await async_maybe_transform(body, watermark_detect_params.WatermarkDetectParams),
            files=files,
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WatermarkDetectResponse,
        )


class WatermarkResourceWithRawResponse:
    def __init__(self, watermark: WatermarkResource) -> None:
        self._watermark = watermark

        self.detect = to_raw_response_wrapper(
            watermark.detect,
        )


class AsyncWatermarkResourceWithRawResponse:
    def __init__(self, watermark: AsyncWatermarkResource) -> None:
        self._watermark = watermark

        self.detect = async_to_raw_response_wrapper(
            watermark.detect,
        )


class WatermarkResourceWithStreamingResponse:
    def __init__(self, watermark: WatermarkResource) -> None:
        self._watermark = watermark

        self.detect = to_streamed_response_wrapper(
            watermark.detect,
        )


class AsyncWatermarkResourceWithStreamingResponse:
    def __init__(self, watermark: AsyncWatermarkResource) -> None:
        self._watermark = watermark

        self.detect = async_to_streamed_response_wrapper(
            watermark.detect,
        )
