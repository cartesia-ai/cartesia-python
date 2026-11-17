# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, TypedDict

from ..emotion import Emotion

__all__ = [
    "SessionCreateWebsocketParams",
    "ConfigOverrides",
    "ConfigOverridesAudio",
    "ConfigOverridesAudioOutput",
    "ConfigOverridesLanguage",
]


class SessionCreateWebsocketParams(TypedDict, total=False):
    config_overrides: ConfigOverrides
    """Per-call overrides using the same field structure as agent configuration.

    Omitted fields use the agent's published configuration.
    """

    dynamic_variables: Dict[str, Union[str, float, bool]]
    """Trusted values that Cartesia stores on the call and supplies to the agent."""


class ConfigOverridesAudioOutput(TypedDict, total=False):
    emotion: Optional[Emotion]
    """The primary emotions are `neutral`, `calm`, `angry`, `content`, `sad`, `scared`.

    For more options, see
    [Prompting Sonic-3](https://docs.cartesia.ai/build-with-cartesia/sonic-3/volume-speed-emotion#emotion-controls-beta).
    """

    speed: Optional[float]
    """Speech speed multiplier from `0.6` to `1.5`.

    Set to `null` to use the default speed.
    """

    voice_id: str
    """ID of the voice used for agent speech during this call."""


class ConfigOverridesAudio(TypedDict, total=False):
    output: ConfigOverridesAudioOutput


class ConfigOverridesLanguage(TypedDict, total=False):
    primary: Optional[
        Literal[
            "en",
            "fr",
            "de",
            "es",
            "pt",
            "zh",
            "ja",
            "hi",
            "it",
            "ko",
            "nl",
            "pl",
            "ru",
            "sv",
            "tr",
            "tl",
            "bg",
            "ro",
            "ar",
            "cs",
            "el",
            "fi",
            "hr",
            "ms",
            "sk",
            "da",
            "ta",
            "uk",
            "hu",
            "no",
            "vi",
            "bn",
            "th",
            "he",
            "ka",
            "id",
            "te",
            "gu",
            "kn",
            "ml",
            "mr",
            "pa",
            "or",
            "ur",
            "bg-BG",
            "bn-IN",
            "cs-CZ",
            "da-DK",
            "de-DE",
            "el-GR",
            "en-AU",
            "en-CA",
            "en-GB",
            "en-IE",
            "en-IN",
            "en-NZ",
            "en-SG",
            "en-US",
            "en-ZA",
            "es-ES",
            "es-MX",
            "es-US",
            "fi-FI",
            "fr-CA",
            "fr-FR",
            "gu-IN",
            "he-IL",
            "hi-IN",
            "hr-HR",
            "hu-HU",
            "id-ID",
            "it-IT",
            "ja-JP",
            "ka-GE",
            "kn-IN",
            "ko-KR",
            "ml-IN",
            "mr-IN",
            "ms-MY",
            "nl-BE",
            "nl-NL",
            "no-NO",
            "or-IN",
            "pa-IN",
            "pl-PL",
            "pt-BR",
            "pt-PT",
            "ro-RO",
            "ru-RU",
            "sk-SK",
            "sv-SE",
            "ta-IN",
            "te-IN",
            "th-TH",
            "tl-PH",
            "tr-TR",
            "uk-UA",
            "ur-IN",
            "vi-VN",
            "zh-CN",
        ]
    ]
    """Primary language used for this call.

    Omit to inherit the published language or set to `null` to use English (`en`).
    """


class ConfigOverrides(TypedDict, total=False):
    """Per-call overrides using the same field structure as agent configuration.

    Omitted fields use the agent's published configuration.
    """

    audio: ConfigOverridesAudio

    initial_message: Optional[str]
    """Message spoken when the call begins.

    Set to `null` to wait for the caller to speak first.
    """

    instructions: str
    """Instructions that define the agent's behavior for this call."""

    language: ConfigOverridesLanguage
