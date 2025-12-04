# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .model_speed import ModelSpeed
from .raw_encoding import RawEncoding
from .voice_specifier import VoiceSpecifier
from .supported_language import SupportedLanguage

__all__ = ["GenerationRequest", "OutputFormat"]


class OutputFormat(BaseModel):
    container: Literal["raw"]

    encoding: RawEncoding

    sample_rate: int


class GenerationRequest(BaseModel):
    llm_model_id: str = FieldInfo(alias="model_id")
    """The ID of the model to use for the generation.

    See [Models](/build-with-cartesia/tts-models) for available models.
    """

    output_format: OutputFormat

    transcript: str
    """The transcript to generate speech for."""

    voice: VoiceSpecifier

    add_phoneme_timestamps: Optional[bool] = None
    """Whether to return phoneme-level timestamps.

    If `false` (default), no phoneme timestamps will be produced. If `true`, the
    server will return timestamp events containing phoneme-level timing information.
    """

    add_timestamps: Optional[bool] = None
    """Whether to return word-level timestamps.

    If `false` (default), no word timestamps will be produced at all. If `true`, the
    server will return timestamp events containing word-level timing information.
    """

    context_id: Optional[str] = None
    """A unique identifier for the context.

    You can use any unique identifier, like a UUID or human ID.

    Some customers use unique identifiers from their own systems (such as
    conversation IDs) as context IDs.
    """

    continue_: Optional[bool] = FieldInfo(alias="continue", default=None)
    """
    Whether this input may be followed by more inputs. If not specified, this
    defaults to `false`.
    """

    duration: Optional[float] = None
    """The maximum duration of the audio in seconds.

    You do not usually need to specify this. If the duration is not appropriate for
    the length of the transcript, the output audio may be truncated.
    """

    flush: Optional[bool] = None
    """Whether to flush the context."""

    language: Optional[SupportedLanguage] = None
    """The language that the given voice should speak the transcript in.

    Options: English (en), French (fr), German (de), Spanish (es), Portuguese (pt),
    Chinese (zh), Japanese (ja), Hindi (hi), Italian (it), Korean (ko), Dutch (nl),
    Polish (pl), Russian (ru), Swedish (sv), Turkish (tr).
    """

    max_buffer_delay_ms: Optional[int] = None
    """The maximum time in milliseconds to buffer text before starting generation.

    Values between [0, 1000]ms are supported. Defaults to 0 (no buffering).

    When set, the model will buffer incoming text chunks until it's confident it has
    enough context to generate high-quality speech, or the buffer delay elapses,
    whichever comes first. Without this option set, the model will kick off
    generations immediately, ceding control of buffering to the user.

    Use this to balance responsiveness with higher quality speech generation, which
    often benefits from having more context.
    """

    pronunciation_dict_ids: Optional[List[str]] = None
    """A list of pronunciation dict IDs to use for the generation.

    This will be applied in addition to the pinned pronunciation dict, which will be
    treated as the first element of the list. If there are conflicts with dict
    items, the latest dict will take precedence.
    """

    speed: Optional[ModelSpeed] = None
    """> This feature is experimental and may not work for all voices.

    Speed setting for the model. Defaults to `normal`.

    Influences the speed of the generated speech. Faster speeds may reduce
    hallucination rate.
    """

    use_normalized_timestamps: Optional[bool] = None
    """Whether to use normalized timestamps (True) or original timestamps (False)."""
