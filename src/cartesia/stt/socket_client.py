import typing
from typing import Any, Dict, Generator, Optional, Union

from ..core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from ._async_websocket import AsyncSttWebsocket
from ._websocket import SttWebsocket
from .types.stt_encoding import SttEncoding


class SttClientWithWebsocket:
    """
    Extension of STT functionality that supports a synchronous WebSocket STT connection.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def _ws_url(self):
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    def websocket(self, *, 
                  model: str = "ink-whisper",
                  language: Optional[str] = "en", 
                  encoding: SttEncoding = "pcm_s16le",
                  sample_rate: int = 16000,
                  min_volume: Optional[float] = None,
                  max_silence_duration_secs: Optional[float] = None):
        """Create a WebSocket connection for real-time speech transcription.

        Args:
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data (required)
            sample_rate: The sample rate of the audio in Hz (required)
            min_volume: Volume threshold for voice activity detection (0.0-1.0)
            max_silence_duration_secs: Maximum duration of silence before endpointing

        Returns:
            SttWebsocket: A connected WebSocket client for STT operations.
        """
        client_headers = self._client_wrapper.get_headers()
        ws = SttWebsocket(
            ws_url=self._ws_url(),
            cartesia_version=client_headers["Cartesia-Version"],
            api_key=client_headers["X-API-Key"],
        )
        # Auto-connect like TTS does for consistency
        ws.connect(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
            min_volume=min_volume,
            max_silence_duration_secs=max_silence_duration_secs,
        )
        return ws

    def transcribe(
        self,
        audio_chunks: typing.Iterator[bytes],
        *,
        model: str = "ink-whisper",
        language: Optional[str] = "en",
        encoding: SttEncoding = "pcm_s16le",
        sample_rate: int = 16000,
        min_volume: Optional[float] = None,
        max_silence_duration_secs: Optional[float] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """Transcribe audio chunks using WebSocket.

        Args:
            audio_chunks: Iterator of audio chunks as bytes
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data (required)
            sample_rate: The sample rate of the audio in Hz (required)
            min_volume: Volume threshold for voice activity detection (0.0-1.0)
            max_silence_duration_secs: Maximum duration of silence before endpointing

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages

        Example:
            >>> client = Cartesia(api_key="your-api-key")
            >>> ws_client = client.stt.websocket()
            >>> for result in ws_client.transcribe(audio_chunks):
            ...     print(result["text"])
        """
        ws = self.websocket(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
            min_volume=min_volume,
            max_silence_duration_secs=max_silence_duration_secs,
        )
        try:
            yield from ws.transcribe(
                audio_chunks,
                model=model,
                language=language,
                encoding=encoding,
                sample_rate=sample_rate,
                min_volume=min_volume,
                max_silence_duration_secs=max_silence_duration_secs,
            )
        finally:
            ws.close()


class AsyncSttClientWithWebsocket:
    """
    Extension of STT functionality that supports an asynchronous WebSocket STT connection.
    """

    def __init__(self, *, client_wrapper: AsyncClientWrapper, get_session):
        self._client_wrapper = client_wrapper
        self._get_session = get_session

    def _ws_url(self) -> str:
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    async def websocket(self, *,
                        model: str = "ink-whisper",
                        language: Optional[str] = "en",
                        encoding: SttEncoding = "pcm_s16le", 
                        sample_rate: int = 16000,
                        min_volume: Optional[float] = None,
                        max_silence_duration_secs: Optional[float] = None):
        """Create an async WebSocket connection for real-time speech transcription.

        Args:
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data (required)
            sample_rate: The sample rate of the audio in Hz (required)
            min_volume: Volume threshold for voice activity detection (0.0-1.0)
            max_silence_duration_secs: Maximum duration of silence before endpointing

        Returns:
            AsyncSttWebsocket: A connected async WebSocket client for STT operations.
        """
        client_headers = self._client_wrapper.get_headers()
        ws = AsyncSttWebsocket(
            ws_url=self._ws_url(),
            cartesia_version=client_headers["Cartesia-Version"],
            api_key=client_headers["X-API-Key"],
            get_session=self._get_session,
        )
        # Auto-connect like TTS does for consistency
        await ws.connect(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
            min_volume=min_volume,
            max_silence_duration_secs=max_silence_duration_secs,
        )
        return ws

    async def transcribe(
        self,
        audio_chunks: typing.AsyncIterator[bytes],
        *,
        model: str = "ink-whisper",
        language: Optional[str] = "en",
        encoding: SttEncoding = "pcm_s16le",
        sample_rate: int = 16000,
        min_volume: Optional[float] = None,
        max_silence_duration_secs: Optional[float] = None,
    ) -> typing.AsyncGenerator[Dict[str, Any], None]:
        """Transcribe audio chunks using async WebSocket.

        Args:
            audio_chunks: Async iterator of audio chunks as bytes
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data (required)
            sample_rate: The sample rate of the audio in Hz (required)
            min_volume: Volume threshold for voice activity detection (0.0-1.0)
            max_silence_duration_secs: Maximum duration of silence before endpointing

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages

        Example:
            >>> client = AsyncCartesia(api_key="your-api-key")
            >>> ws_client = await client.stt.websocket()
            >>> async for result in ws_client.transcribe(audio_chunks):
            ...     print(result["text"])
        """
        ws = await self.websocket(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
            min_volume=min_volume,
            max_silence_duration_secs=max_silence_duration_secs,
        )
        try:
            async for result in ws.transcribe(
                audio_chunks,
                model=model,
                language=language,
                encoding=encoding,
                sample_rate=sample_rate,
                min_volume=min_volume,
                max_silence_duration_secs=max_silence_duration_secs,
            ):
                yield result
        finally:
            await ws.close() 
