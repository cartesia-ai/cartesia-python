# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
import typing
from .transcription_word import TranscriptionWordParams


class TranscriptionResponseParams(typing_extensions.TypedDict):
    text: str
    """
    The transcribed text.
    """

    language: typing_extensions.NotRequired[str]
    """
    The specified language of the input audio.
    """

    duration: typing_extensions.NotRequired[float]
    """
    The duration of the input audio in seconds.
    """

    words: typing_extensions.NotRequired[typing.Sequence[TranscriptionWordParams]]
    """
    Word-level timestamps showing the start and end time of each word. Only included when `[word]` is passed into `timestamp_granularities`.
    """
