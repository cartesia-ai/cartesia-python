import base64
import json
import uuid
from collections import defaultdict
from typing import Any, Dict, Generator, Iterator, List, Optional, Set, Union

try:
    from websockets.sync.client import connect

    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from iterators import TimeoutIterator

from cartesia._types import EventType, OutputFormat, VoiceControls
from cartesia.utils.tts import _construct_tts_request


class _TTSContext:
    """Manage a single context over a WebSocket.

    This class can be used to stream inputs, as they become available, to a specific `context_id`. See README for usage.

    See :class:`_AsyncTTSContext` for asynchronous use cases.

    Each TTSContext will close automatically when a done message is received for that context. It also closes if there is an error.
    """

    def __init__(self, context_id: str, websocket: "_WebSocket"):
        self._context_id = context_id
        self._websocket = websocket
        self._error = None

    def __del__(self):
        self._close()

    @property
    def context_id(self) -> str:
        return self._context_id

    def send(
        self,
        model_id: str,
        transcript: Iterator[str],
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Generator[bytes, None, None]:
        """Send audio generation requests to the WebSocket and yield responses.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: Iterator over text chunks with <1s latency.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Yields:
            Dictionary containing the following key(s):
            - audio: The audio as bytes.
            - context_id: The context ID for the request.

        Raises:
            ValueError: If provided context_id doesn't match the current context.
            RuntimeError: If there's an error generating audio.
        """
        if context_id is not None and context_id != self._context_id:
            raise ValueError("Context ID does not match the context ID of the current context.")

        self._websocket.connect()

        # Create the initial request body
        request_body = _construct_tts_request(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            duration=duration,
            language=language,
            context_id=self._context_id,
            add_timestamps=add_timestamps,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        try:
            # Create an iterator with a timeout to get text chunks
            text_iterator = TimeoutIterator(
                transcript, timeout=0.001
            )  # 1ms timeout for nearly non-blocking receive
            next_chunk = next(text_iterator, None)

            while True:
                # Send the next text chunk to the WebSocket if available
                if next_chunk is not None and next_chunk != text_iterator.get_sentinel():
                    request_body["transcript"] = next_chunk
                    request_body["continue"] = True
                    self._websocket.websocket.send(json.dumps(request_body))
                    next_chunk = next(text_iterator, None)

                try:
                    # Receive responses from the WebSocket with a small timeout
                    response = json.loads(
                        self._websocket.websocket.recv(timeout=0.001)
                    )  # 1ms timeout for nearly non-blocking receive
                    if response["context_id"] != self._context_id:
                        pass
                    if "error" in response:
                        raise RuntimeError(f"Error generating audio:\n{response['error']}")
                    if response["done"]:
                        break
                    if response["data"]:
                        yield self._websocket._convert_response(
                            response=response, include_context_id=True
                        )
                except TimeoutError:
                    pass

                # Continuously receive from WebSocket until the next text chunk is available
                while next_chunk == text_iterator.get_sentinel():
                    try:
                        response = json.loads(self._websocket.websocket.recv(timeout=0.001))
                        if response["context_id"] != self._context_id:
                            continue
                        if "error" in response:
                            raise RuntimeError(f"Error generating audio:\n{response['error']}")
                        if response["done"]:
                            break
                        if response["data"]:
                            yield self._websocket._convert_response(
                                response=response, include_context_id=True
                            )
                    except TimeoutError:
                        pass
                    next_chunk = next(text_iterator, None)

                # Send final message if all input text chunks are exhausted
                if next_chunk is None:
                    request_body["transcript"] = ""
                    request_body["continue"] = False
                    self._websocket.websocket.send(json.dumps(request_body))
                    break

            # Receive remaining messages from the WebSocket until "done" is received
            while True:
                response = json.loads(self._websocket.websocket.recv())
                if response["context_id"] != self._context_id:
                    continue
                if "error" in response:
                    raise RuntimeError(f"Error generating audio:\n{response['error']}")
                if response["done"]:
                    break
                yield self._websocket._convert_response(response=response, include_context_id=True)

        except Exception as e:
            self._websocket.close()
            raise RuntimeError(f"Failed to generate audio. {e}")

    def _close(self):
        """Closes the context. Automatically called when a done message is received for this context."""
        self._websocket._remove_context(self._context_id)

    def is_closed(self):
        """Check if the context is closed or not. Returns True if closed."""
        return self._context_id not in self._websocket._contexts


class _WebSocket:
    """This class contains methods to generate audio using WebSocket. Ideal for low-latency audio generation.

    Usage:
        >>> ws = client.tts.websocket()
        >>> for audio_chunk in ws.send(
        ...     model_id="sonic-english", transcript="Hello world!", voice_embedding=embedding,
        ...     output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        ...     context_id=context_id, stream=True
        ... ):
        ...     audio = audio_chunk["audio"]
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
        self.websocket = None
        self._contexts: Set[str] = set()

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            raise RuntimeError("Failed to close WebSocket: ", e)

    def connect(self):
        """This method connects to the WebSocket if it is not already connected.

        Raises:
            RuntimeError: If the connection to the WebSocket fails.
        """
        if not IS_WEBSOCKET_SYNC_AVAILABLE:
            raise ImportError(
                "The synchronous WebSocket client is not available. Please ensure that you have 'websockets>=12.0' or compatible version installed."
            )
        if self.websocket is None or self._is_websocket_closed():
            route = "tts/websocket"
            try:
                self.websocket = connect(
                    f"{self.ws_url}/{route}?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
                )
            except Exception as e:
                raise RuntimeError(f"Failed to connect to WebSocket. {e}")

    def _is_websocket_closed(self):
        return self.websocket.socket.fileno() == -1

    def close(self):
        """This method closes the WebSocket connection. *Highly* recommended to call this method when done using the WebSocket."""
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()

        if self._contexts:
            self._contexts.clear()

    def _convert_response(
        self, response: Dict[str, any], include_context_id: bool
    ) -> Dict[str, Any]:
        out = {}
        if response["type"] == EventType.AUDIO:
            out["audio"] = base64.b64decode(response["data"])
        elif response["type"] == EventType.TIMESTAMPS:
            out["word_timestamps"] = response["word_timestamps"]

        if include_context_id:
            out["context_id"] = response["context_id"]

        return out

    def send(
        self,
        model_id: str,
        transcript: str,
        output_format: dict,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Union[bytes, Generator[bytes, None, None]]:
        """Send a request to the WebSocket to generate audio.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: The text to convert to speech.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`
            stream: Whether to stream the audio or not.
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Returns:
            If `stream` is True, the method returns a generator that yields chunks. Each chunk is a dictionary.
            If `stream` is False, the method returns a dictionary.
            Both the generator and the dictionary contain the following key(s):
            - audio: The audio as bytes.
            - context_id: The context ID for the request.
        """
        self.connect()

        if context_id is None:
            context_id = str(uuid.uuid4())

        request_body = _construct_tts_request(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            context_id=context_id,
            duration=duration,
            language=language,
            add_timestamps=add_timestamps,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        generator = self._websocket_generator(request_body)

        if stream:
            return generator

        chunks = []
        word_timestamps = defaultdict(list)
        for chunk in generator:
            if "audio" in chunk:
                chunks.append(chunk["audio"])
            if add_timestamps and "word_timestamps" in chunk:
                for k, v in chunk["word_timestamps"].items():
                    word_timestamps[k].extend(v)
        out = {"audio": b"".join(chunks), "context_id": context_id}
        if add_timestamps:
            out["word_timestamps"] = word_timestamps
        return out

    def _websocket_generator(self, request_body: Dict[str, Any]):
        self.websocket.send(json.dumps(request_body))

        try:
            while True:
                response = json.loads(self.websocket.recv())
                if "error" in response:
                    raise RuntimeError(f"Error generating audio:\n{response['error']}")
                if response["done"]:
                    break
                yield self._convert_response(response=response, include_context_id=True)
        except Exception as e:
            # Close the websocket connection if an error occurs.
            self.close()
            raise RuntimeError(f"Failed to generate audio. {response}") from e

    def _remove_context(self, context_id: str):
        if context_id in self._contexts:
            self._contexts.remove(context_id)

    def context(self, context_id: Optional[str] = None) -> _TTSContext:
        if context_id in self._contexts:
            raise ValueError(f"Context for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._contexts:
            self._contexts.add(context_id)
        return _TTSContext(context_id, self)
