import asyncio
import base64
import json
import logging
import os
import uuid
from collections import defaultdict
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Generator,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import aiohttp
import httpx
import requests

try:
    from websockets.sync.client import connect

    IS_WEBSOCKET_SYNC_AVAILABLE = True
except ImportError:
    IS_WEBSOCKET_SYNC_AVAILABLE = False

from cartesia._types import (
    DeprecatedOutputFormatMapping,
    EventType,
    OutputFormat,
    OutputFormatMapping,
    VoiceControls,
    VoiceMetadata,
)
from cartesia.utils.retry import retry_on_connection_error, retry_on_connection_error_async
from iterators import TimeoutIterator
from websockets.sync.client import connect

DEFAULT_MODEL_ID = "sonic-english"  # latest default model
MULTILINGUAL_MODEL_ID = "sonic-multilingual"  # latest multilingual model
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_CARTESIA_VERSION = "2024-06-10"  # latest version
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_NUM_CONNECTIONS = 10  # connections per client

BACKOFF_FACTOR = 1
MAX_RETRIES = 3

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Constructor for the BaseClient. Used by the Cartesia and AsyncCartesia clients."""
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self._base_url = base_url or os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.timeout = timeout

    @property
    def base_url(self):
        return self._base_url


class Resource:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
    ):
        """Constructor for the Resource class. Used by the Voices and TTS classes."""
        self.api_key = api_key
        self.timeout = timeout
        self._base_url = base_url
        self.cartesia_version = DEFAULT_CARTESIA_VERSION
        self.headers = {
            "X-API-Key": self.api_key,
            "Cartesia-Version": self.cartesia_version,
            "Content-Type": "application/json",
        }

    @property
    def base_url(self):
        return self._base_url

    def _http_url(self):
        """Returns the HTTP URL for the Cartesia API.
        If the base URL is localhost, the URL will start with 'http'. Otherwise, it will start with 'https'.
        """
        if self._base_url.startswith("http://") or self._base_url.startswith("https://"):
            return self._base_url
        else:
            prefix = "http" if "localhost" in self._base_url else "https"
            return f"{prefix}://{self._base_url}"

    def _ws_url(self):
        """Returns the WebSocket URL for the Cartesia API.
        If the base URL is localhost, the URL will start with 'ws'. Otherwise, it will start with 'wss'.
        """
        if self._base_url.startswith("ws://") or self._base_url.startswith("wss://"):
            return self._base_url
        else:
            prefix = "ws" if "localhost" in self._base_url else "wss"
            return f"{prefix}://{self._base_url}"


class Cartesia(BaseClient):
    """
    The client for Cartesia's text-to-speech library.

    This client contains methods to interact with the Cartesia text-to-speech API.
    The client can be used to manage your voice library and generate speech from text.

    The client supports generating audio using both Server-Sent Events and WebSocket for lower latency.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Constructor for the Cartesia client.

        Args:
            api_key: The API key to use for authorization.
                If not specified, the API key will be read from the environment variable
                `CARTESIA_API_KEY`.
            base_url: The base URL for the Cartesia API.
                If not specified, the base URL will be read from the enviroment variable
                `CARTESIA_BASE_URL`. Defaults to `api.cartesia.ai`.
            timeout: The timeout for HTTP and WebSocket requests in seconds. Defaults to 30 seconds.
        """
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.voices = Voices(api_key=self.api_key, base_url=self._base_url, timeout=self.timeout)
        self.tts = TTS(api_key=self.api_key, base_url=self._base_url, timeout=self.timeout)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        pass


class Voices(Resource):
    """This resource contains methods to list, get, clone, and create voices in your Cartesia voice library.

    Usage:
        >>> client = Cartesia(api_key="your_api_key")
        >>> voices = client.voices.list()
        >>> voice = client.voices.get(id="a0e99841-438c-4a64-b679-ae501e7d6091")
        >>> print("Voice Name:", voice["name"], "Voice Description:", voice["description"])
        >>> embedding = client.voices.clone(filepath="path/to/clip.wav")
        >>> new_voice = client.voices.create(
        ...     name="My Voice", description="A new voice", embedding=embedding
        ... )
    """

    def list(self) -> List[VoiceMetadata]:
        """List all voices in your voice library.

        Returns:
        This method returns a list of VoiceMetadata objects.
        """
        response = httpx.get(
            f"{self._http_url()}/voices",
            headers=self.headers,
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to get voices. Error: {response.text}")

        voices = response.json()
        return voices

    def get(self, id: str) -> VoiceMetadata:
        """Get a voice by its ID.

        Args:
            id: The ID of the voice.

        Returns:
            A VoiceMetadata object containing the voice metadata.
        """
        url = f"{self._http_url()}/voices/{id}"
        response = httpx.get(url, headers=self.headers, timeout=self.timeout)

        if not response.is_success:
            raise ValueError(
                f"Failed to get voice. Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        return response.json()

    def clone(self, filepath: Optional[str] = None, enhance: str = True) -> List[float]:
        """Clone a voice from a clip.

        Args:
            filepath: The path to the clip file.
            enhance: Whether to enhance the clip before cloning the voice (highly recommended). Defaults to True.

        Returns:
            The embedding of the cloned voice as a list of floats.
        """
        if not filepath:
            raise ValueError("Filepath must be specified.")
        url = f"{self._http_url()}/voices/clone/clip"
        with open(filepath, "rb") as file:
            files = {"clip": file}
            files["enhance"] = str(enhance).lower()
            headers = self.headers.copy()
            headers.pop("Content-Type", None)
            response = httpx.post(url, headers=headers, files=files, timeout=self.timeout)
            if not response.is_success:
                raise ValueError(f"Failed to clone voice from clip. Error: {response.text}")

        return response.json()["embedding"]

    def create(self, name: str, description: str, embedding: List[float]) -> VoiceMetadata:
        """Create a new voice.

        Args:
            name: The name of the voice.
            description: The description of the voice.
            embedding: The embedding of the voice. This should be generated with :meth:`clone`.

        Returns:
            A dictionary containing the voice metadata.
        """
        response = httpx.post(
            f"{self._http_url()}/voices",
            headers=self.headers,
            json={"name": name, "description": description, "embedding": embedding},
            timeout=self.timeout,
        )

        if not response.is_success:
            raise ValueError(f"Failed to create voice. Error: {response.text}")

        return response.json()


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

        voice = TTS._validate_and_construct_voice(
            voice_id,
            voice_embedding=voice_embedding,
            experimental_voice_controls=_experimental_voice_controls,
        )

        # Create the initial request body
        request_body = {
            "model_id": model_id,
            "voice": voice,
            "output_format": {
                "container": output_format["container"],
                "encoding": output_format["encoding"],
                "sample_rate": output_format["sample_rate"],
            },
            "context_id": self._context_id,
            "language": language,
        }

        if duration is not None:
            request_body["duration"] = duration

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

        voice = TTS._validate_and_construct_voice(
            voice_id,
            voice_embedding=voice_embedding,
            experimental_voice_controls=_experimental_voice_controls,
        )

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": {
                "container": output_format["container"],
                "encoding": output_format["encoding"],
                "sample_rate": output_format["sample_rate"],
            },
            "context_id": context_id,
            "language": language,
            "add_timestamps": add_timestamps,
        }

        if duration is not None:
            request_body["duration"] = duration

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


class _SSE:
    """This class contains methods to generate audio using Server-Sent Events.

    Usage:
        >>> for audio_chunk in client.tts.sse(
        ...     model_id="sonic-english", transcript="Hello world!", voice_embedding=embedding,
        ...     output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}, stream=True
        ... ):
        ...     audio = audio_chunk["audio"]
    """

    def __init__(
        self,
        http_url: str,
        headers: Dict[str, str],
        timeout: float,
    ):
        self.http_url = http_url
        self.headers = headers
        self.timeout = timeout

    def _update_buffer(self, buffer: str, chunk_bytes: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        buffer += chunk_bytes.decode("utf-8")
        outputs = []
        while "{" in buffer and "}" in buffer:
            start_index = buffer.find("{")
            end_index = buffer.find("}", start_index)
            if start_index != -1 and end_index != -1:
                try:
                    chunk_json = json.loads(buffer[start_index : end_index + 1])
                    if "error" in chunk_json:
                        raise RuntimeError(f"Error generating audio:\n{chunk_json['error']}")
                    if chunk_json["done"]:
                        break
                    audio = base64.b64decode(chunk_json["data"])
                    outputs.append({"audio": audio})
                    buffer = buffer[end_index + 1 :]
                except json.JSONDecodeError:
                    break
        return buffer, outputs

    def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Union[bytes, Generator[bytes, None, None]]:
        """Send a request to the server to generate audio using Server-Sent Events.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: The text to convert to speech.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            output_format: A dictionary containing the details of the output format.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`
            stream: Whether to stream the audio or not.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Returns:
            If `stream` is True, the method returns a generator that yields chunks. Each chunk is a dictionary.
            If `stream` is False, the method returns a dictionary.
            Both the generator and the dictionary contain the following key(s):
            - audio: The audio as bytes.
        """
        voice = TTS._validate_and_construct_voice(
            voice_id,
            voice_embedding=voice_embedding,
            experimental_voice_controls=_experimental_voice_controls,
        )
        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": {
                "container": output_format["container"],
                "encoding": output_format["encoding"],
                "sample_rate": output_format["sample_rate"],
            },
            "language": language,
        }

        if duration is not None:
            request_body["duration"] = duration

        generator = self._sse_generator_wrapper(request_body)

        if stream:
            return generator

        chunks = []
        for chunk in generator:
            chunks.append(chunk["audio"])

        return {"audio": b"".join(chunks)}

    @retry_on_connection_error(
        max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, logger=logger
    )
    def _sse_generator_wrapper(self, request_body: Dict[str, Any]):
        """Need to wrap the sse generator in a function for the retry decorator to work."""
        try:
            for chunk in self._sse_generator(request_body):
                yield chunk
        except Exception as e:
            raise RuntimeError(f"Error generating audio. {e}")

    def _sse_generator(self, request_body: Dict[str, Any]):
        response = requests.post(
            f"{self.http_url}/tts/sse",
            stream=True,
            data=json.dumps(request_body),
            headers=self.headers,
            timeout=(self.timeout, self.timeout),
        )
        if not response.ok:
            raise ValueError(f"Failed to generate audio. {response.text}")

        buffer = ""
        for chunk_bytes in response.iter_content(chunk_size=None):
            buffer, outputs = self._update_buffer(buffer=buffer, chunk_bytes=chunk_bytes)
            for output in outputs:
                yield output

        if buffer:
            try:
                chunk_json = json.loads(buffer)
                audio = base64.b64decode(chunk_json["data"])
                yield {"audio": audio}
            except json.JSONDecodeError:
                pass


class TTS(Resource):
    """This resource contains methods to generate audio using Cartesia's text-to-speech API."""

    def __init__(self, api_key: str, base_url: str, timeout: float):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self._sse_class = _SSE(self._http_url(), self.headers, self.timeout)
        self.sse = self._sse_class.send

    def websocket(self) -> _WebSocket:
        """This method returns a WebSocket object that can be used to generate audio using WebSocket.

        Returns:
            _WebSocket: A WebSocket object that can be used to generate audio using WebSocket.
        """
        ws = _WebSocket(self._ws_url(), self.api_key, self.cartesia_version)
        ws.connect()
        return ws

    @staticmethod
    def get_output_format(output_format_name: str) -> OutputFormat:
        """Convenience method to get the output_format dictionary from a given output format name.

        Args:
            output_format_name (str): The name of the output format.

        Returns:
            OutputFormat: A dictionary containing the details of the output format to be passed into tts.sse() or tts.websocket().send()

        Raises:
            ValueError: If the output_format name is not supported
        """
        if output_format_name in OutputFormatMapping._format_mapping:
            output_format_obj = OutputFormatMapping.get_format(output_format_name)
        elif output_format_name in DeprecatedOutputFormatMapping._format_mapping:
            output_format_obj = DeprecatedOutputFormatMapping.get_format_deprecated(
                output_format_name
            )
        else:
            raise ValueError(f"Unsupported format: {output_format_name}")

        return OutputFormat(
            container=output_format_obj["container"],
            encoding=output_format_obj["encoding"],
            sample_rate=output_format_obj["sample_rate"],
        )

    @staticmethod
    def get_sample_rate(self, output_format_name: str) -> int:
        """Convenience method to get the sample rate for a given output format.

        Args:
            output_format_name (str): The name of the output format.

        Returns:
            int: The sample rate for the output format.

        Raises:
            ValueError: If the output_format name is not supported
        """
        if output_format_name in OutputFormatMapping._format_mapping:
            output_format_obj = OutputFormatMapping.get_format(output_format_name)
        elif output_format_name in DeprecatedOutputFormatMapping._format_mapping:
            output_format_obj = DeprecatedOutputFormatMapping.get_format_deprecated(
                output_format_name
            )
        else:
            raise ValueError(f"Unsupported format: {output_format_name}")

        return output_format_obj["sample_rate"]

    @staticmethod
    def _validate_and_construct_voice(
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> dict:
        """Validate and construct the voice dictionary for the request.

        Args:
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            experimental_voice_controls: Voice controls for emotion and speed.
                Note: This is an experimental feature and may rapidly change in the future.

        Returns:
            A dictionary representing the voice configuration.

        Raises:
            ValueError: If neither or both voice_id and voice_embedding are specified.
        """
        if voice_id is None and voice_embedding is None:
            raise ValueError("Either voice_id or voice_embedding must be specified.")

        if voice_id is not None and voice_embedding is not None:
            raise ValueError("Only one of voice_id or voice_embedding should be specified.")

        if voice_id:
            voice = {"mode": "id", "id": voice_id}
        else:
            voice = {"mode": "embedding", "embedding": voice_embedding}
        if experimental_voice_controls is not None:
            voice["__experimental_controls"] = experimental_voice_controls
        return voice


class AsyncCartesia(Cartesia):
    """The asynchronous version of the Cartesia client."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_num_connections: int = DEFAULT_NUM_CONNECTIONS,
    ):
        """
        Args:
            api_key: See :class:`Cartesia`.
            base_url: See :class:`Cartesia`.
            timeout: See :class:`Cartesia`.
            max_num_connections: The maximum number of concurrent connections to use for the client.
                This is used to limit the number of connections that can be made to the server.
        """
        self._session = None
        self._loop = None
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.max_num_connections = max_num_connections
        self.tts = AsyncTTS(
            api_key=self.api_key,
            base_url=self._base_url,
            timeout=self.timeout,
            get_session=self._get_session,
        )

    async def _get_session(self):
        current_loop = asyncio.get_event_loop()
        if self._loop is not current_loop:
            # If the loop has changed, close the session and create a new one.
            await self.close()
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(limit=self.max_num_connections)
            self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
            self._loop = current_loop
        return self._session

    async def close(self):
        """This method closes the session.

        It is *strongly* recommended to call this method when you are done using the client.
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        elif loop.is_running():
            loop.create_task(self.close())

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        await self.close()


class _AsyncSSE(_SSE):
    """This class contains methods to generate audio using Server-Sent Events asynchronously."""

    def __init__(
        self,
        http_url: str,
        headers: Dict[str, str],
        timeout: float,
        get_session: Callable[[], Optional[aiohttp.ClientSession]],
    ):
        super().__init__(http_url, headers, timeout)
        self._get_session = get_session

    async def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Union[bytes, AsyncGenerator[bytes, None]]:
        voice = TTS._validate_and_construct_voice(
            voice_id,
            voice_embedding=voice_embedding,
            experimental_voice_controls=_experimental_voice_controls,
        )

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": {
                "container": output_format["container"],
                "encoding": output_format["encoding"],
                "sample_rate": output_format["sample_rate"],
            },
            "language": language,
        }

        if duration is not None:
            request_body["duration"] = duration

        generator = self._sse_generator_wrapper(request_body)

        if stream:
            return generator

        chunks = []
        async for chunk in generator:
            chunks.append(chunk["audio"])

        return {"audio": b"".join(chunks)}

    @retry_on_connection_error_async(
        max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, logger=logger
    )
    async def _sse_generator_wrapper(self, request_body: Dict[str, Any]):
        """Need to wrap the sse generator in a function for the retry decorator to work."""
        try:
            async for chunk in self._sse_generator(request_body):
                yield chunk
        except Exception as e:
            raise RuntimeError(f"Error generating audio. {e}")

    async def _sse_generator(self, request_body: Dict[str, Any]):
        session = await self._get_session()
        async with session.post(
            f"{self.http_url}/tts/sse", data=json.dumps(request_body), headers=self.headers
        ) as response:
            if not response.ok:
                raise ValueError(f"Failed to generate audio. {await response.text()}")

            buffer = ""
            async for chunk_bytes in response.content.iter_any():
                buffer, outputs = self._update_buffer(buffer=buffer, chunk_bytes=chunk_bytes)
                for output in outputs:
                    yield output

            if buffer:
                try:
                    chunk_json = json.loads(buffer)
                    audio = base64.b64decode(chunk_json["data"])
                    yield {"audio": audio}
                except json.JSONDecodeError:
                    pass


class _AsyncTTSContext:
    """Manage a single context over an AsyncWebSocket.

    This class separates sending requests and receiving responses into two separate methods.
    This can be used for sending multiple requests without awaiting the response.
    Then you can listen to the responses in the order they were sent. See README for usage.

    Each AsyncTTSContext will close automatically when a done message is received for that context.
    This happens when the no_more_inputs method is called (equivalent to sending a request with `continue_ = False`),
    or if no requests have been sent for 5 seconds on the same context. It also closes if there is an error.

    """

    def __init__(self, context_id: str, websocket: "_AsyncWebSocket", timeout: float):
        self._context_id = context_id
        self._websocket = websocket
        self.timeout = timeout
        self._error = None

    @property
    def context_id(self) -> str:
        return self._context_id

    async def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        continue_: bool = False,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> None:
        """Send audio generation requests to the WebSocket. The response can be received using the `receive` method.

        Args:
            model_id: The ID of the model to use for generating audio.
            transcript: The text to convert to speech.
            output_format: A dictionary containing the details of the output format.
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            context_id: The context ID to use for the request. If not specified, a random context ID will be generated.
            continue_: Whether to continue the audio generation from the previous transcript or not.
            duration: The duration of the audio in seconds.
            language: The language code for the audio request. This can only be used with `model_id = sonic-multilingual`.
            add_timestamps: Whether to return word-level timestamps.
            _experimental_voice_controls: Experimental voice controls for controlling speed and emotion.
                Note: This is an experimental feature and may change rapidly in future releases.

        Returns:
            None.
        """
        if context_id is not None and context_id != self._context_id:
            raise ValueError("Context ID does not match the context ID of the current context.")
        if continue_ and transcript == "":
            raise ValueError("Transcript cannot be empty when continue_ is True.")

        await self._websocket.connect()

        voice = TTS._validate_and_construct_voice(
            voice_id, voice_embedding, experimental_voice_controls=_experimental_voice_controls
        )

        request_body = {
            "model_id": model_id,
            "transcript": transcript,
            "voice": voice,
            "output_format": {
                "container": output_format["container"],
                "encoding": output_format["encoding"],
                "sample_rate": output_format["sample_rate"],
            },
            "context_id": self._context_id,
            "continue": continue_,
            "language": language,
            "add_timestamps": add_timestamps,
        }

        if duration is not None:
            request_body["duration"] = duration

        await self._websocket.websocket.send_json(request_body)

        # Start listening for responses on the WebSocket
        self._websocket._dispatch_listener()

    async def no_more_inputs(self) -> None:
        """Send a request to the WebSocket to indicate that no more requests will be sent."""
        await self.send(
            model_id=DEFAULT_MODEL_ID,
            transcript="",
            output_format=TTS.get_output_format("raw_pcm_f32le_44100"),
            voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",  # Default voice ID since it's a required input for now
            context_id=self._context_id,
            continue_=False,
        )

    async def receive(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Receive the audio chunks from the WebSocket. This method is a generator that yields audio chunks.

        Returns:
            An async generator that yields audio chunks. Each chunk is a dictionary containing the audio as bytes.
        """
        try:
            while True:
                response = await self._websocket._get_message(
                    self._context_id, timeout=self.timeout
                )
                if "error" in response:
                    raise RuntimeError(f"Error generating audio:\n{response['error']}")
                if response["done"]:
                    break
                yield self._websocket._convert_response(response, include_context_id=True)
        except Exception as e:
            if isinstance(e, asyncio.TimeoutError):
                raise RuntimeError("Timeout while waiting for audio chunk")
            raise RuntimeError(f"Failed to generate audio:\n{e}")
        finally:
            self._close()

    def _close(self) -> None:
        """Closes the context. Automatically called when a done message is received for this context."""
        self._websocket._remove_context(self._context_id)

    def is_closed(self):
        """Check if the context is closed or not. Returns True if closed."""
        return self._context_id not in self._websocket._context_queues

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        self._close()

    def __del__(self):
        self._close()


class _AsyncWebSocket(_WebSocket):
    """This class contains methods to generate audio using WebSocket asynchronously."""

    def __init__(
        self,
        ws_url: str,
        api_key: str,
        cartesia_version: str,
        timeout: float,
        get_session: Callable[[], Optional[aiohttp.ClientSession]],
    ):
        """
        Args:
            ws_url: The WebSocket URL for the Cartesia API.
            api_key: The API key to use for authorization.
            cartesia_version: The version of the Cartesia API to use.
            timeout: The timeout for responses on the WebSocket in seconds.
            get_session: A function that returns an aiohttp.ClientSession object.
        """
        super().__init__(ws_url, api_key, cartesia_version)
        self.timeout = timeout
        self._get_session = get_session
        self.websocket = None
        self._context_queues: Dict[str, asyncio.Queue] = {}
        self._processing_task: asyncio.Task = None

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        elif loop.is_running():
            loop.create_task(self.close())

    async def connect(self):
        if self.websocket is None or self._is_websocket_closed():
            route = "tts/websocket"
            session = await self._get_session()
            try:
                self.websocket = await session.ws_connect(
                    f"{self.ws_url}/{route}?api_key={self.api_key}&cartesia_version={self.cartesia_version}"
                )
            except Exception as e:
                raise RuntimeError(f"Failed to connect to WebSocket. {e}")

    def _is_websocket_closed(self):
        return self.websocket.closed

    async def close(self):
        """This method closes the websocket connection. *Highly* recommended to call this method when done."""
        if self.websocket is not None and not self._is_websocket_closed():
            await self.websocket.close()
        if self._processing_task:
            self._processing_task.cancel()
            try:
                self._processing_task = None
            except asyncio.CancelledError:
                pass
            except TypeError as e:
                # Ignore the error if the task is already cancelled
                # For some reason we are getting None responses
                # TODO: This needs to be fixed - we need to think about why we are getting None responses.
                if "Received message 256:None" not in str(e):
                    raise e

        for context_id in list(self._context_queues.keys()):
            self._remove_context(context_id)

        self._context_queues.clear()
        self._processing_task = None
        self.websocket = None

    async def send(
        self,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        context_id: Optional[str] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        stream: bool = True,
        add_timestamps: bool = False,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Union[bytes, AsyncGenerator[bytes, None]]:
        """See :meth:`_WebSocket.send` for details."""
        if context_id is None:
            context_id = str(uuid.uuid4())

        ctx = self.context(context_id)

        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            context_id=context_id,
            duration=duration,
            language=language,
            continue_=False,
            add_timestamps=add_timestamps,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        generator = ctx.receive()

        if stream:
            return generator

        chunks = []
        word_timestamps = defaultdict(list)
        async for chunk in generator:
            if "audio" in chunk:
                chunks.append(chunk["audio"])
            if add_timestamps and "word_timestamps" in chunk:
                for k, v in chunk["word_timestamps"].items():
                    word_timestamps[k].extend(v)
        out = {"audio": b"".join(chunks), "context_id": context_id}
        if add_timestamps:
            out["word_timestamps"] = word_timestamps
        return out

    async def _process_responses(self):
        try:
            while True:
                response = await self.websocket.receive_json()
                if response["context_id"]:
                    context_id = response["context_id"]
                if context_id in self._context_queues:
                    await self._context_queues[context_id].put(response)
        except Exception as e:
            self._error = e
            raise e

    async def _get_message(self, context_id: str, timeout: float) -> Dict[str, Any]:
        if context_id not in self._context_queues:
            raise ValueError(f"Context ID {context_id} not found.")
        return await asyncio.wait_for(self._context_queues[context_id].get(), timeout=timeout)

    def _remove_context(self, context_id: str):
        if context_id in self._context_queues:
            del self._context_queues[context_id]

    def _dispatch_listener(self):
        if self._processing_task is None or self._processing_task.done():
            self._processing_task = asyncio.create_task(self._process_responses())

    def context(self, context_id: Optional[str] = None) -> _AsyncTTSContext:
        if context_id in self._context_queues:
            raise ValueError(f"AsyncContext for context ID {context_id} already exists.")
        if context_id is None:
            context_id = str(uuid.uuid4())
        if context_id not in self._context_queues:
            self._context_queues[context_id] = asyncio.Queue()
        return _AsyncTTSContext(context_id, self, self.timeout)


class AsyncTTS(TTS):
    def __init__(self, api_key, base_url, timeout, get_session):
        super().__init__(api_key, base_url, timeout)
        self._get_session = get_session
        self._sse_class = _AsyncSSE(self._http_url(), self.headers, self.timeout, get_session)
        self.sse = self._sse_class.send

    async def websocket(self) -> _AsyncWebSocket:
        ws = _AsyncWebSocket(
            self._ws_url(), self.api_key, self.cartesia_version, self.timeout, self._get_session
        )
        await ws.connect()
        return ws
