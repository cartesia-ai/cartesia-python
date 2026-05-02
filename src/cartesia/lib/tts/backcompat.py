"""
TTSResource.websocket() and AsyncTTSResource.websocket() implementation.

.. deprecated::
    Use contexts.py instead.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Iterator, Optional, cast
from typing_extensions import AsyncIterator

from pydantic import BaseModel

from ...types.voice_specifier_param import VoiceSpecifierParam

if TYPE_CHECKING:
    from .connection_manager_3_0 import (
        WebSocketContext_3_0,
        AsyncWebSocketContext_3_0,
        TTSResourceConnection_3_0,
        AsyncTTSResourceConnection_3_0,
        TTSResourceConnectionManager_3_0,
        AsyncTTSResourceConnectionManager_3_0,
    )


class BackcompatWebSocketTtsOutput(BaseModel):
    """
    Output object for backward compatibility with v2 WebSocket response.

    .. deprecated::
        Returned by :class:`BackcompatTTSResourceConnection` and :class:`AsyncBackcompatTTSResourceConnection`.
    """

    audio: Optional[bytes] = None
    word_timestamps: Optional[Any] = None
    phoneme_timestamps: Optional[Any] = None
    context_id: Optional[str] = None
    flush_done: Optional[bool] = None
    flush_id: Optional[str] = None


class BackcompatTTSResourceConnection:
    """
    Wrapper for TTSResourceConnection to provide v2-compatible API.

    .. deprecated::
        Use ``cartesia.tts.contexts_ws()`` instead.
    """

    def __init__(self, manager: "TTSResourceConnectionManager_3_0"):
        self._manager = manager
        self._connection: Optional["TTSResourceConnection_3_0"] = None

    def connect(self) -> None:
        if self._connection is None:
            self._connection = self._manager.enter()

    def close(self) -> None:
        if self._connection:
            self._manager.__exit__(None, None, None)
            self._connection = None

    def context(self, context_id: Optional[str] = None) -> "WebSocketContext_3_0":
        """Create a context helper (v2 compatible)."""
        if not self._connection:
            self.connect()
        assert self._connection is not None
        return self._connection.context(context_id)

    def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: Dict[str, Any],
        voice: Dict[str, Any],
        context_id: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> "Iterator[BackcompatWebSocketTtsOutput] | BackcompatWebSocketTtsOutput":
        """Send a request and return responses (v2 compatible).

        If stream is True, returns an iterator of BackcompatWebSocketTtsOutput chunks.
        If stream is False, returns a single BackcompatWebSocketTtsOutput with all
        audio concatenated and timestamps aggregated (matching v2 behaviour).
        """
        if not self._connection:
            self.connect()
        assert self._connection is not None
        self._connection._ensure_connected()

        ctx = self._connection.context(context_id)

        # Send the request
        continue_ = kwargs.pop("continue_", False)
        ctx.send(
            model_id=model_id,
            transcript=transcript,
            voice=cast(VoiceSpecifierParam, voice),
            output_format=output_format,
            continue_=continue_,
            **kwargs,
        )

        # Generate output stream
        def generator() -> Iterator[BackcompatWebSocketTtsOutput]:
            for event in ctx.receive():
                if event.type == "error":
                    raise RuntimeError(f"Error generating audio:\n{getattr(event, 'error', 'Unknown error')}")

                out = BackcompatWebSocketTtsOutput(context_id=event.context_id)

                if event.type == "chunk":
                    out.audio = event.audio
                elif event.type == "timestamps":
                    out.word_timestamps = getattr(event, "word_timestamps", None)
                elif event.type == "phoneme_timestamps":
                    out.phoneme_timestamps = getattr(event, "phoneme_timestamps", None)
                elif event.type == "flush_done":
                    out.flush_done = getattr(event, "flush_done", None)
                    out.flush_id = getattr(event, "flush_id", None)

                yield out

        if stream:
            return generator()

        audio_parts: list[bytes] = []
        words: list[str] = []
        word_starts: list[float] = []
        word_ends: list[float] = []
        phonemes: list[str] = []
        phoneme_starts: list[float] = []
        phoneme_ends: list[float] = []
        for chunk in generator():
            if chunk.audio is not None:
                audio_parts.append(chunk.audio)
            if chunk.word_timestamps is not None:
                wt = chunk.word_timestamps
                words.extend(wt.words)
                word_starts.extend(wt.start)
                word_ends.extend(wt.end)
            if chunk.phoneme_timestamps is not None:
                pt = chunk.phoneme_timestamps
                phonemes.extend(pt.phonemes)
                phoneme_starts.extend(pt.start)
                phoneme_ends.extend(pt.end)
        return BackcompatWebSocketTtsOutput(
            audio=b"".join(audio_parts) if audio_parts else None,
            context_id=ctx._context_id,
            word_timestamps={"words": words, "start": word_starts, "end": word_ends} if words else None,
            phoneme_timestamps={"phonemes": phonemes, "start": phoneme_starts, "end": phoneme_ends}
            if phonemes
            else None,
        )


class AsyncBackcompatTTSResourceConnection:
    """
    Wrapper for AsyncTTSResourceConnection to provide v2-compatible API.

    .. deprecated::
        Use ``cartesia.tts.contexts_ws()`` instead.
    """

    def __init__(self, manager: "AsyncTTSResourceConnectionManager_3_0"):
        self._manager = manager
        self._connection: Optional["AsyncTTSResourceConnection_3_0"] = None

    async def connect(self) -> None:
        if self._connection is None:
            self._connection = await self._manager.enter()

    async def close(self) -> None:
        if self._connection:
            await self._manager.__aexit__(None, None, None)
            self._connection = None

    def context(self, context_id: Optional[str] = None) -> "AsyncWebSocketContext_3_0":
        """Create a context helper (v2 compatible)."""
        if not self._connection:
            raise RuntimeError("Must call connect() before creating context")
        return self._connection.context(context_id)

    async def send(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: Dict[str, Any],
        voice: Dict[str, Any],
        context_id: Optional[str] = None,
        stream: bool = True,
        **kwargs: Any,
    ) -> "AsyncIterator[BackcompatWebSocketTtsOutput] | BackcompatWebSocketTtsOutput":
        """Send a request and return responses (v2 compatible).

        If stream is True, returns an async iterator of BackcompatWebSocketTtsOutput chunks.
        If stream is False, returns a single BackcompatWebSocketTtsOutput with all
        audio concatenated and timestamps aggregated (matching v2 behaviour).
        """
        if not self._connection:
            await self.connect()
        assert self._connection is not None
        await self._connection._ensure_connected()

        ctx = self._connection.context(context_id)

        # Send the request
        continue_ = kwargs.pop("continue_", False)
        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            voice=cast(VoiceSpecifierParam, voice),
            output_format=output_format,
            continue_=continue_,
            **kwargs,
        )

        # Generate output stream
        async def generator() -> AsyncIterator[BackcompatWebSocketTtsOutput]:
            async for event in ctx.receive():
                if event.type == "error":
                    raise RuntimeError(f"Error generating audio:\n{getattr(event, 'error', 'Unknown error')}")

                out = BackcompatWebSocketTtsOutput(context_id=event.context_id)

                if event.type == "chunk":
                    out.audio = event.audio
                elif event.type == "timestamps":
                    out.word_timestamps = getattr(event, "word_timestamps", None)
                elif event.type == "phoneme_timestamps":
                    out.phoneme_timestamps = getattr(event, "phoneme_timestamps", None)
                elif event.type == "flush_done":
                    out.flush_done = getattr(event, "flush_done", None)
                    out.flush_id = getattr(event, "flush_id", None)

                yield out

        if stream:
            return generator()

        audio_parts: list[bytes] = []
        words: list[str] = []
        word_starts: list[float] = []
        word_ends: list[float] = []
        phonemes: list[str] = []
        phoneme_starts: list[float] = []
        phoneme_ends: list[float] = []
        async for chunk in generator():
            if chunk.audio is not None:
                audio_parts.append(chunk.audio)
            if chunk.word_timestamps is not None:
                wt = chunk.word_timestamps
                words.extend(wt.words)
                word_starts.extend(wt.start)
                word_ends.extend(wt.end)
            if chunk.phoneme_timestamps is not None:
                pt = chunk.phoneme_timestamps
                phonemes.extend(pt.phonemes)
                phoneme_starts.extend(pt.start)
                phoneme_ends.extend(pt.end)
        return BackcompatWebSocketTtsOutput(
            audio=b"".join(audio_parts) if audio_parts else None,
            context_id=ctx._context_id,
            word_timestamps={"words": words, "start": word_starts, "end": word_ends} if words else None,
            phoneme_timestamps={"phonemes": phonemes, "start": phoneme_starts, "end": phoneme_ends}
            if phonemes
            else None,
        )
