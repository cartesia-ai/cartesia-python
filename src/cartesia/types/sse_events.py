"""
Aliases for backward compatibility.
"""

from .tts_sse_event import (
    TTSSSEEvent,
    TTSSSEDoneEvent as DoneEvent,
    TTSSSEChunkEvent as ChunkEvent,
    TTSSSEErrorEvent as ErrorEvent,
    TTSSSETimestampsEvent as TimestampsEvent,
    TTSSSEPhonemeTimestampsEvent as PhonemeTimestampsEvent,
    _TTSSSEEventBase as SSEEvent,
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

SSEEventType = TTSSSEEvent
