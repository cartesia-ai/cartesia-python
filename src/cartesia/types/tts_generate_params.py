# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from .tts_model import TTSModel
from .model_speed import ModelSpeed
from .supported_language import SupportedLanguage
from .voice_specifier_param import VoiceSpecifierParam
from .generation_config_param import GenerationConfigParam
from .mp3_output_format_param import MP3OutputFormatParam
from .raw_output_format_param import RawOutputFormatParam
from .wav_output_format_param import WAVOutputFormatParam

__all__ = ["TTSGenerateParams", "OutputFormat"]


class TTSGenerateParams(TypedDict, total=False):
    model_id: Required[TTSModel]
    """Text-to-speech models.

    See [the docs](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest)
    for all options.
    """

    output_format: Required[OutputFormat]

    transcript: Required[str]

    voice: Required[VoiceSpecifierParam]

    generation_config: GenerationConfigParam
    """Configure the various attributes of the generated speech.

    These are only for `sonic-3` and have no effect on earlier models.

    See
    [Volume, Speed, and Emotion in Sonic-3](https://docs.cartesia.ai/build-with-cartesia/sonic-3/volume-speed-emotion)
    for a guide on this option.
    """

    language: Optional[SupportedLanguage]
    """The language that the given voice should speak the transcript in.

    For valid options, see
    [Models](https://docs.cartesia.ai/build-with-cartesia/tts-models).
    """

    pronunciation_dict_id: Optional[str]
    """The ID of a pronunciation dictionary to use for the generation.

    Pronunciation dictionaries are supported by `sonic-3` models and newer.
    """

    save: Optional[bool]
    """Whether to save the generated audio file.

    When true, the response will include a `Cartesia-File-ID` header.
    """

    speed: ModelSpeed
    """Speed setting for the model.

    Defaults to `normal`. This feature is experimental and may not work for all
    voices. Influences the speed of the generated speech. Faster speeds may reduce
    hallucination rate.
    """


OutputFormat: TypeAlias = Union[RawOutputFormatParam, WAVOutputFormatParam, MP3OutputFormatParam]
