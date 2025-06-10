import asyncio
import json
import typing
import uuid
from typing import Any, Awaitable, AsyncGenerator, Callable, Dict, Optional, Union

import aiohttp

from cartesia.stt.types import (
    StreamingTranscriptionResponse,
    StreamingTranscriptionResponse_Error,
    StreamingTranscriptionResponse_Transcript,
)

from ..core.pydantic_utilities import parse_obj_as
from ._websocket import SttWebsocket


class AsyncSttWebsocket(SttWebsocket):
    """This class contains methods to transcribe audio using WebSocket asynchronously."""

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
        get_session: Callable[[], Awaitable[Optional[aiohttp.ClientSession]]],
        timeout: float = 30,
    ):
        """
        Args:
            ws_url: The WebSocket URL for the Cartesia API.
            api_key: The API key to use for authorization.
            cartesia_version: The version of the Cartesia API to use.
            timeout: The timeout for responses on the WebSocket in seconds.
            get_session: A function that returns an awaitable of aiohttp.ClientSession object.
        """
        super().__init__(ws_url, api_key, cartesia_version)
        self.timeout = timeout
        self._get_session = get_session
        self.websocket: Optional[aiohttp.ClientWebSocketResponse] = None
        self._default_model: str = "ink-whisper"
        self._default_language: Optional[str] = "en"
        self._default_encoding: Optional[str] = "pcm_s16le"
        self._default_sample_rate: int = 16000

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        elif loop.is_running():
            loop.create_task(self.close())

    async def connect(
        self,
        *,
        model: str = "ink-whisper",
        language: Optional[str] = "en",
        encoding: Optional[str] = "pcm_s16le",
        sample_rate: int = 16000,
    ):
        """Connect to the STT WebSocket with the specified parameters.

        Args:
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data
            sample_rate: The sample rate of the audio in Hz

        Raises:
            RuntimeError: If the connection to the WebSocket fails.
        """
        self._default_model = model
        self._default_language = language
        self._default_encoding = encoding
        self._default_sample_rate = sample_rate
        
        if self.websocket is None or self._is_websocket_closed():
            route = "stt/websocket"
            session = await self._get_session()
            
            params = {
                "model": model,
                "api_key": self.api_key,
                "cartesia_version": self.cartesia_version,
            }
            if language is not None:
                params["language"] = language
            if encoding is not None:
                params["encoding"] = encoding
            if sample_rate is not None:
                params["sample_rate"] = str(sample_rate)

            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            url = f"{self.ws_url}/{route}?{query_string}"
            
            try:
                if session is None:
                    raise RuntimeError("Session is not available")
                self.websocket = await session.ws_connect(url)
            except Exception as e:
                status_code = None
                error_message = str(e)
                
                if hasattr(e, 'status') and e.status is not None:
                    status_code = e.status
                
                    if status_code == 402:
                        error_message = "Payment required. Your API key may have insufficient credits or permissions."
                    elif status_code == 401:
                        error_message = "Unauthorized. Please check your API key."
                    elif status_code == 403:
                        error_message = "Forbidden. You don't have permission to access this resource."
                    elif status_code == 404:
                        error_message = "Not found. The requested resource doesn't exist."
                    
                    raise RuntimeError(f"Failed to connect to WebSocket.\nStatus: {status_code}. Error message: {error_message}")
                else:
                    raise RuntimeError(f"Failed to connect to WebSocket at {url}. {e}")

    def _is_websocket_closed(self):
        return self.websocket is None or self.websocket.closed

    async def close(self):
        """This method closes the websocket connection. Highly recommended to call this method when done."""
        if self.websocket is not None and not self._is_websocket_closed():
            await self.websocket.close()
        self.websocket = None

    async def send(self, data: Union[bytes, str]):
        """Send audio data or control commands to the WebSocket.

        Args:
            data: Binary audio data or text command ("finalize" or "done")
        """
        if self.websocket is None or self._is_websocket_closed():
            await self.connect(
                model=self._default_model,
                language=self._default_language,
                encoding=self._default_encoding,
                sample_rate=self._default_sample_rate,
            )
        
        assert self.websocket is not None, "WebSocket should be connected after connect() call"
        
        if isinstance(data, bytes):
            await self.websocket.send_bytes(data)
        elif isinstance(data, str):
            await self.websocket.send_str(data)
        else:
            raise TypeError("Data must be bytes (audio) or str (command)")

    async def receive(self) -> AsyncGenerator[Dict[str, Any], None]:  # type: ignore[override]
        """Receive transcription results from the WebSocket.

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages
        """
        if self.websocket is None or self._is_websocket_closed():
            await self.connect(
                model=self._default_model,
                language=self._default_language,
                encoding=self._default_encoding,
                sample_rate=self._default_sample_rate,
            )

        assert self.websocket is not None, "WebSocket should be connected after connect() call"

        try:
            while True:
                try:
                    msg = await asyncio.wait_for(self.websocket.receive(), timeout=self.timeout)
                    
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        raw_data = json.loads(msg.data)
                        
                        # Handle error responses
                        if raw_data.get("type") == "error":
                            raise RuntimeError(f"Error transcribing audio: {raw_data.get('message', 'Unknown error')}")
                        
                        # Handle transcript responses with flexible parsing
                        if raw_data.get("type") == "transcript":
                            # Provide defaults for missing required fields
                            result = {
                                "type": raw_data["type"],
                                "request_id": raw_data.get("request_id", ""),
                                "text": raw_data.get("text", ""),  # Default to empty string if missing
                                "is_final": raw_data.get("is_final", False),  # Default to False if missing
                            }
                            
                            # Add optional fields if present
                            if "duration" in raw_data:
                                result["duration"] = raw_data["duration"]
                            if "language" in raw_data:
                                result["language"] = raw_data["language"]
                            
                            yield result
                        
                        # Handle flush_done acknowledgment
                        elif raw_data.get("type") == "flush_done":
                            result = {
                                "type": raw_data["type"],
                                "request_id": raw_data.get("request_id", ""),
                            }
                            yield result
                        
                        # Handle done acknowledgment - session complete
                        elif raw_data.get("type") == "done":
                            result = {
                                "type": raw_data["type"],
                                "request_id": raw_data.get("request_id", ""),
                            }
                            yield result
                            # Session is complete, break out of loop
                            break
                    
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        websocket_exception = self.websocket.exception() if self.websocket else None
                        await self.close()
                        raise RuntimeError(f"WebSocket error: {websocket_exception}")
                    
                    elif msg.type == aiohttp.WSMsgType.CLOSE:
                        break
                
                except asyncio.TimeoutError:
                    await self.close()
                    raise RuntimeError("Timeout while waiting for transcription")
                except Exception as inner_e:
                    await self.close()
                    raise RuntimeError(f"Error receiving transcription: {inner_e}")
                        
        except Exception as e:
            await self.close()
            raise RuntimeError(f"Failed to receive transcription. {e}")

    async def transcribe(  # type: ignore[override]
        self,
        audio_chunks: typing.AsyncIterator[bytes],
        *,
        model: str = "ink-whisper",
        language: Optional[str] = "en",
        encoding: Optional[str] = "pcm_s16le",
        sample_rate: int = 16000,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Transcribe audio chunks using the WebSocket.

        Args:
            audio_chunks: Async iterator of audio chunks as bytes
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data
            sample_rate: The sample rate of the audio in Hz

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages
        """
        await self.connect(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
        )

        try:
            # Send all audio chunks
            async for chunk in audio_chunks:
                await self.send(chunk)
            
            # Send finalize command to flush remaining audio
            await self.send("finalize")
            
            # Send done command to close session cleanly
            await self.send("done")
            
            # Receive all responses until done
            async for result in self.receive():
                yield result
            
        finally:
            await self.close() 
