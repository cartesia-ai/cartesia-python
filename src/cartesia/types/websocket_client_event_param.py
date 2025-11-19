# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .model_speed import ModelSpeed
from .raw_encoding import RawEncoding
from .supported_language import SupportedLanguage
from .voice_specifier_param import VoiceSpecifierParam

__all__ = ["WebsocketClientEventParam", "GenerationRequest", "GenerationRequestOutputFormat", "CancelContextRequest"]


class GenerationRequestOutputFormat(TypedDict, total=False):
    container: Required[Literal["raw"]]

    encoding: Required[RawEncoding]

    sample_rate: Required[int]


_GenerationRequestReservedKeywords = TypedDict(
    "_GenerationRequestReservedKeywords",
    {
        "continue": Optional[bool],
    },
    total=False,
)


class GenerationRequest(_GenerationRequestReservedKeywords, total=False):
    model_id: Required[str]
    """The ID of the model to use for the generation.

    See [Models](/build-with-cartesia/tts-models) for available models.
    """

    output_format: Required[GenerationRequestOutputFormat]

    transcript: Required[str]
    """The transcript to generate speech for."""

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
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    duration: Optional[float]
    """The maximum duration of the audio in seconds.

    You do not usually need to specify this. If the duration is not appropriate for
    the length of the transcript, the output audio may be truncated.
    """

    flush: Optional[bool]
    """Whether to flush the context."""

    language: Optional[SupportedLanguage]
    """The language that the given voice should speak the transcript in.

    Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
    Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
    Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).
    """

    max_buffer_delay_ms: Optional[int]
    """The maximum time in milliseconds to buffer text before starting generation.

    Values between [0, 1000]ms are supported. Defaults to 0 (no buffering).

    When set, the model will buffer incoming text chunks until it's confident it has
    enough context to generate high-quality speech, or the buffer delay elapses,
    whichever comes first. Without this option set, the model will kick off
    generations immediately, ceding control of buffering to the user.

    Use this to balance responsiveness with higher quality speech generation, which
    often benefits from having more context.
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


class CancelContextRequest(TypedDict, total=False):
    cancel: Required[Literal[True]]
    """
    Whether to cancel the context, so that no more messages are generated for that
    context.
    """

    context_id: Required[str]
    """The ID of the context to cancel."""


WebsocketClientEventParam: TypeAlias = Union[GenerationRequest, CancelContextRequest]
