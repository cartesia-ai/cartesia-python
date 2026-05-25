# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias, TypedDict

from .._types import FileTypes
from .infill_model import InfillModel
from .mp3_output_format_param import MP3OutputFormatParam
from .raw_output_format_param import RawOutputFormatParam
from .wav_output_format_param import WAVOutputFormatParam

__all__ = [
    "TTSInfillParams",
    "OutputFormat",
    "OutputFormatRawOutputFormat",
    "OutputFormatWavOutputFormat",
    "OutputFormatMP3OutputFormat",
]


class TTSInfillParams(TypedDict, total=False):
    language: str
    """The language of the transcript"""

    left_audio: FileTypes

    model_id: InfillModel
    """Infill models.

    See
    [the docs](https://docs.cartesia.ai/api-reference/infill/bytes#body-model-id)
    for all options.
    """

    output_format: OutputFormat

    right_audio: FileTypes

    transcript: str
    """The infill text to generate"""

    voice_id: str
    """The ID of the voice to use for generating audio"""


OutputFormat: TypeAlias = Union[RawOutputFormatParam, WAVOutputFormatParam, MP3OutputFormatParam]

OutputFormatRawOutputFormat = RawOutputFormatParam  # alias for backward compatibility
OutputFormatWavOutputFormat = WAVOutputFormatParam  # alias for backward compatibility
OutputFormatMP3OutputFormat = MP3OutputFormatParam  # alias for backward compatibility
