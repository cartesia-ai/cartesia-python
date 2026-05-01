"""
Aliases for backward compatibility.

Breaking in v3.1.0: Changed SSEEvent from a pydantic model to be the same as SSEEventType.
This was done to remove ``id`` and ``retry`` members from all SSE event models
in order to prevent unexpected behavior in conflict with the SSE protocol.
"""

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

SSEEvent = TTSSSEEvent  # changed from model to type in v3.1.0

ChunkEvent = TTSSSEChunkEvent

TimestampsEvent = TTSSSETimestampsEvent

PhonemeTimestampsEvent = TTSSSEPhonemeTimestampsEvent

DoneEvent = TTSSSEDoneEvent

ErrorEvent = TTSSSEErrorEvent

SSEEventType = TTSSSEEvent
