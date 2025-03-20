# This file was auto-generated by Fern from our API Definition.

import typing_extensions
from ..types.voice_id import VoiceId
import datetime as dt
import typing_extensions
from ...embedding.types.embedding import Embedding
from ...tts.types.supported_language import SupportedLanguage


class VoiceParams(typing_extensions.TypedDict):
    id: VoiceId
    is_owner: bool
    """
    Whether the current user is the owner of the voice.
    """

    name: str
    """
    The name of the voice.
    """

    description: str
    """
    The description of the voice.
    """

    created_at: dt.datetime
    """
    The date and time the voice was created.
    """

    embedding: typing_extensions.NotRequired[Embedding]
    """
    The vector embedding of the voice. Only included when `expand` includes `embedding`.
    """

    is_starred: typing_extensions.NotRequired[bool]
    """
    Whether the current user has starred the voice. Only included when `expand` includes `is_starred`.
    """

    language: SupportedLanguage
