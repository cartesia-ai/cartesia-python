import json
import typing
import uuid
from typing import Any, Dict, Generator, Optional, Union

try:
    from websockets.sync.client import connect
    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from cartesia.stt.types import (
    StreamingTranscriptionResponse,
    StreamingTranscriptionResponse_Error,
    StreamingTranscriptionResponse_Transcript,
)

from ..core.pydantic_utilities import parse_obj_as


class SttWebsocket:
    """This class contains methods to transcribe audio using WebSocket. Ideal for real-time speech transcription.

    Usage:
        >>> ws = client.stt.websocket()
        >>> for audio_chunk in audio_chunks:
        ...     ws.send(audio_chunk)
        >>> ws.send("finalize")  # Flush remaining audio
        >>> ws.send("done")      # Close session
        >>> for transcription in ws.receive():
        ...     print(transcription["text"])
    """

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
    ):
        self.ws_url = ws_url
        self.api_key = api_key
        self.cartesia_version = cartesia_version
        self.websocket: Optional[Any] = None
        self._is_listening = False
        # Store default connection parameters for auto-connect with proper typing
        self._default_model: str = "ink-whisper"
        self._default_language: Optional[str] = "en"
        self._default_encoding: Optional[str] = "pcm_s16le"
        self._default_sample_rate: int = 16000

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            raise RuntimeError("Failed to close WebSocket: ", e)

    def connect(
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
        # Store parameters for future auto-connects
        self._default_model = model
        self._default_language = language
        self._default_encoding = encoding
        self._default_sample_rate = sample_rate
        
        if not IS_WEBSOCKET_SYNC_AVAILABLE:
            raise ImportError(
                "The synchronous WebSocket client is not available. Please ensure that you have 'websockets>=12.0' or compatible version installed."
            )
        if self.websocket is None or self._is_websocket_closed():
            route = "stt/websocket"
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
                self.websocket = connect(url)
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
                    raise RuntimeError(f"Failed to connect to WebSocket. {e}")

    def _is_websocket_closed(self):
        return self.websocket is None or (hasattr(self.websocket, 'socket') and self.websocket.socket.fileno() == -1)

    def close(self):
        """This method closes the WebSocket connection. Highly recommended to call this method when done using the WebSocket."""
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()

    def send(self, data: Union[bytes, str]):
        """Send audio data or control commands to the WebSocket.

        Args:
            data: Binary audio data or text command ("finalize" or "done")
        """
        # Auto-connect if not connected, like TTS does
        if self.websocket is None or self._is_websocket_closed():
            self.connect(
                model=self._default_model,
                language=self._default_language,
                encoding=self._default_encoding,
                sample_rate=self._default_sample_rate,
            )
        
        assert self.websocket is not None, "WebSocket should be connected after connect() call"
        
        if isinstance(data, bytes):
            self.websocket.send(data)
        elif isinstance(data, str):
            self.websocket.send(data)
        else:
            raise TypeError("Data must be bytes (audio) or str (command)")

    def receive(self) -> Generator[Dict[str, Any], None, None]:
        """Receive transcription results from the WebSocket.

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages
        """
        # Auto-connect if not connected, like TTS does
        if self.websocket is None or self._is_websocket_closed():
            self.connect(
                model=self._default_model,
                language=self._default_language,
                encoding=self._default_encoding,
                sample_rate=self._default_sample_rate,
            )

        assert self.websocket is not None, "WebSocket should be connected after connect() call"

        try:
            while True:
                try:
                    message = self.websocket.recv()
                    if isinstance(message, str):
                        raw_data = json.loads(message)
                        
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
                
                except Exception as inner_e:
                    self.close()
                    raise RuntimeError(f"Error receiving transcription: {inner_e}")
                        
        except Exception as e:
            self.close()
            raise RuntimeError(f"Failed to receive transcription. {e}")

    def transcribe(
        self,
        audio_chunks: typing.Iterator[bytes],
        *,
        model: str = "ink-whisper",
        language: Optional[str] = "en",
        encoding: Optional[str] = "pcm_s16le",
        sample_rate: int = 16000,
    ) -> Generator[Dict[str, Any], None, None]:
        """Transcribe audio chunks using the WebSocket.

        Args:
            audio_chunks: Iterator of audio chunks as bytes
            model: ID of the model to use for transcription
            language: The language of the input audio in ISO-639-1 format
            encoding: The encoding format of the audio data
            sample_rate: The sample rate of the audio in Hz

        Yields:
            Dictionary containing transcription results, flush_done, done, or error messages
        """
        self.connect(
            model=model,
            language=language,
            encoding=encoding,
            sample_rate=sample_rate,
        )

        try:
            # Send all audio chunks
            for chunk in audio_chunks:
                self.send(chunk)
            
            # Send finalize command to flush remaining audio
            self.send("finalize")
            
            # Send done command to close session cleanly
            self.send("done")
            
            # Receive all responses until done
            yield from self.receive()
            
        finally:
            self.close() 
