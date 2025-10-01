# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr
from .model_speed import ModelSpeed
from .raw_encoding import RawEncoding
from .supported_language import SupportedLanguage
from .voice_specifier_param import VoiceSpecifierParam

__all__ = ["TtSynthesizeSseParams", "OutputFormat"]


class TtSynthesizeSseParams(TypedDict, total=False):
    model_id: Required[str]
    """The ID of the model to use for the generation.

    See [Models](/build-with-cartesia/tts-models) for available models.
    """

    output_format: Required[OutputFormat]

    transcript: Required[str]

    voice: Required[VoiceSpecifierParam]

    add_phoneme_timestamps: Optional[bool]
    """Whether to return phoneme-level timestamps.

    If `false` (default), no phoneme timestamps will be produced. If `true`, the
    server will return timestamp events containing phoneme-level timing information.
    """

    add_timestamps: Optional[bool]
    """Whether to return word-level timestamps.

    If `false` (default), no word timestamps will be produced at all. If `true`, the
    server will return timestamp events containing word-level timing information.
    """

    context_id: Optional[str]
    """Optional context ID for this request."""

    duration: Optional[float]
    """The maximum duration of the audio in seconds.

    You do not usually need to specify this. If the duration is not appropriate for
    the length of the transcript, the output audio may be truncated.
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

    speed: Optional[ModelSpeed]
    """> This feature is experimental and may not work for all voices.

    Speed setting for the model. Defaults to `normal`.

    Influences the speed of the generated speech. Faster speeds may reduce
    hallucination rate.
    """

    use_normalized_timestamps: Optional[bool]
    """Whether to use normalized timestamps (True) or original timestamps (False)."""


class OutputFormat(TypedDict, total=False):
    container: Required[Literal["raw"]]

    encoding: Required[RawEncoding]

    sample_rate: Required[int]
