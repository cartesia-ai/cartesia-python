# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .model_speed import ModelSpeed
from .supported_language import SupportedLanguage
from .voice_specifier_param import VoiceSpecifierParam
from .raw_output_format_param import RawOutputFormatParam

__all__ = [
    "TtGenerateParams",
    "OutputFormat",
    "OutputFormatRawOutputFormat",
    "OutputFormatWavOutputFormat",
    "OutputFormatMP3OutputFormat",
    "GenerationConfig",
    "GenerationConfigExperimental",
]


class TtGenerateParams(TypedDict, total=False):
    model_id: Required[str]
    """The ID of the model to use for the generation.

    See [Models](/build-with-cartesia/tts-models) for available models.
    """

    output_format: Required[OutputFormat]

    transcript: Required[str]

    voice: Required[VoiceSpecifierParam]

    duration: Optional[float]
    """The maximum duration of the audio in seconds.

    You do not usually need to specify this. If the duration is not appropriate for
    the length of the transcript, the output audio may be truncated.
    """

    generation_config: Optional[GenerationConfig]
    """Configure the various attributes of the generated speech.

    These controls are only available for `sonic-3-preview` and will have no effect
    on earlier models.
    """

    language: Optional[SupportedLanguage]
    """The language that the given voice should speak the transcript in.

    Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
    Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
    Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).
    """

    pronunciation_dict_ids: Optional[SequenceNotStr[str]]
    """A list of pronunciation dict IDs to use for the generation.

    This will be applied in addition to the pinned pronunciation dict, which will be
    treated as the first element of the list. If there are conflicts with dict
    items, the latest dict will take precedence.
    """

    save: Optional[bool]
    """Whether to save the generated audio file.

    When true, the response will include a `Cartesia-File-ID` header.
    """

    speed: Optional[ModelSpeed]
    """> This feature is experimental and may not work for all voices.

    Speed setting for the model. Defaults to `normal`.

    Influences the speed of the generated speech. Faster speeds may reduce
    hallucination rate.
    """


class OutputFormatRawOutputFormat(RawOutputFormatParam, total=False):
    container: Literal["raw"]


class OutputFormatWavOutputFormat(RawOutputFormatParam, total=False):
    container: Literal["wav"]


class OutputFormatMP3OutputFormat(TypedDict, total=False):
    bit_rate: Required[int]
    """The bit rate of the audio in bits per second.

    Supported bit rates are 32000, 64000, 96000, 128000, 192000.
    """

    sample_rate: Required[int]

    container: Literal["mp3"]


OutputFormat: TypeAlias = Union[OutputFormatRawOutputFormat, OutputFormatWavOutputFormat, OutputFormatMP3OutputFormat]


class GenerationConfigExperimental(TypedDict, total=False):
    accent_localization: Optional[int]
    """
    Toggle accent localization: 0 (disabled, default) or 1 (enabled). When enabled,
    the voice adapts to match the transcript language's accent while preserving
    vocal characteristics. When disabled, maintains the original voice accent. For
    more information, see
    [Localize Voices](/build-with-sonic/capabilities/localize-voices).
    """


class GenerationConfig(TypedDict, total=False):
    experimental: Optional[GenerationConfigExperimental]
    """These controls are **experimental** and subject to breaking changes."""

    speed: Optional[float]
    """Adjust the speed of the generated speech between -1.0 (slower) and 1.0 (faster).

    0.0 is the default speed.
    """

    volume: Optional[float]
    """Adjust the volume of the generated speech between -1.0 (softer) and 1.0
    (louder).

    0.0 is the default volume.
    """
