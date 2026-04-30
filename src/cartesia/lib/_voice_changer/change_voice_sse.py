from __future__ import annotations

import warnings
from typing import Mapping, Optional, cast
from typing_extensions import Literal

import httpx

from ...types import (
    RawEncoding,
    OutputFormatContainer,
    voice_changer_change_voice_sse_params,
)
from ..._files import deepcopy_with_paths
from ..._types import Body, Omit, Query, Headers, NoneType, NotGiven, FileTypes
from ..._utils import extract_files, maybe_transform
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._base_client import make_request_options
from ..._utils._transform import async_maybe_transform
from ...types.raw_encoding import RawEncoding
from ...types.output_format_container import OutputFormatContainer


def sync_change_voice_sse(
    resource: SyncAPIResource,
    *,
    clip: FileTypes | Omit,
    output_format_bit_rate: Optional[int] | Omit,
    output_format_container: OutputFormatContainer | Omit,
    output_format_encoding: Optional[RawEncoding] | Omit,
    output_format_sample_rate: Literal[8000, 16000, 22050, 24000, 44100, 48000] | Omit,
    voice_id: str | Omit,
    extra_headers: Headers | None,
    extra_query: Query | None,
    extra_body: Body | None,
    timeout: float | httpx.Timeout | None | NotGiven,
) -> None:
    """
    Deprecated Sync Voice Changer (SSE). This function is no longer maintained.
    """

    warnings.warn(
        "Use .generate_sse() instead",
        DeprecationWarning,
        stacklevel=2,
    )

    extra_headers = {"Accept": "*/*", **(extra_headers or {})}
    body = deepcopy_with_paths(
        {
            "clip": clip,
            "output_format_bit_rate": output_format_bit_rate,
            "output_format_container": output_format_container,
            "output_format_encoding": output_format_encoding,
            "output_format_sample_rate": output_format_sample_rate,
            "voice_id": voice_id,
        },
        [["clip"]],
    )
    files = extract_files(cast(Mapping[str, object], body), paths=[["clip"]])
    # It should be noted that the actual Content-Type header that will be
    # sent to the server will contain a `boundary` parameter, e.g.
    # multipart/form-data; boundary=---abc--
    extra_headers["Content-Type"] = "multipart/form-data"
    return resource._post(
        "/voice-changer/sse",
        body=maybe_transform(body, voice_changer_change_voice_sse_params.VoiceChangerChangeVoiceSseParams),
        files=files,
        options=make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        ),
        cast_to=NoneType,
    )


async def async_change_voice_sse(
    resource: AsyncAPIResource,
    *,
    clip: FileTypes | Omit,
    output_format_bit_rate: Optional[int] | Omit,
    output_format_container: OutputFormatContainer | Omit,
    output_format_encoding: Optional[RawEncoding] | Omit,
    output_format_sample_rate: Literal[8000, 16000, 22050, 24000, 44100, 48000] | Omit,
    voice_id: str | Omit,
    extra_headers: Headers | None,
    extra_query: Query | None,
    extra_body: Body | None,
    timeout: float | httpx.Timeout | None | NotGiven,
) -> None:
    """
    Deprecated Async Voice Changer (SSE). This function is no longer maintained.
    """

    warnings.warn(
        "Use .generate_sse() instead",
        DeprecationWarning,
        stacklevel=2,
    )

    extra_headers = {"Accept": "*/*", **(extra_headers or {})}
    body = deepcopy_with_paths(
        {
            "clip": clip,
            "output_format_bit_rate": output_format_bit_rate,
            "output_format_container": output_format_container,
            "output_format_encoding": output_format_encoding,
            "output_format_sample_rate": output_format_sample_rate,
            "voice_id": voice_id,
        },
        [["clip"]],
    )
    files = extract_files(cast(Mapping[str, object], body), paths=[["clip"]])
    # It should be noted that the actual Content-Type header that will be
    # sent to the server will contain a `boundary` parameter, e.g.
    # multipart/form-data; boundary=---abc--
    extra_headers["Content-Type"] = "multipart/form-data"
    return await resource._post(
        "/voice-changer/sse",
        body=await async_maybe_transform(body, voice_changer_change_voice_sse_params.VoiceChangerChangeVoiceSseParams),
        files=files,
        options=make_request_options(
            extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
        ),
        cast_to=NoneType,
    )
