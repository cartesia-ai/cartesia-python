"""Aliases for backward compatibility."""

from .._models import BaseModel
from .tts_sse_event import (
    TTSSSEEvent,
    TTSSSEDoneEvent,
    TTSSSEChunkEvent,
    TTSSSEErrorEvent,
    TTSSSETimestampsEvent,
    TTSSSEPhonemeTimestampsEvent,
)
from .word_timestamps import WordTimestamps as WordTimestamps
from .phoneme_timestamps import PhonemeTimestamps as PhonemeTimestamps

__all__ = [
    "SSEEvent",
    "ChunkEvent",
    "TimestampsEvent",
    "PhonemeTimestampsEvent",
    "DoneEvent",
    "ErrorEvent",
    "WordTimestamps",
    "PhonemeTimestamps",
]

# This is technically a breaking change from v3.0.2,
# but I think it's worth the cost since accessing SSEEvent.id and SSEEvent.retry
# is undefined behavior
SSEEvent = BaseModel

ChunkEvent = TTSSSEChunkEvent

TimestampsEvent = TTSSSETimestampsEvent

PhonemeTimestampsEvent = TTSSSEPhonemeTimestampsEvent

DoneEvent = TTSSSEDoneEvent

ErrorEvent = TTSSSEErrorEvent

SSEEventType = TTSSSEEvent
