import asyncio
import base64
import json
import os
import uuid
from types import TracebackType
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    TypedDict,
    Union,
)

import aiohttp
import httpx
import logging
import requests
from websockets.sync.client import connect

from cartesia.utils import retry_on_connection_error, retry_on_connection_error_async
from cartesia._types import (
    AudioDataReturnType,
    AudioOutputFormat,
    AudioOutput,
    Embedding,
    VoiceMetadata,
)

try:
    import numpy as np

    _NUMPY_AVAILABLE = True
except ImportError:
    _NUMPY_AVAILABLE = False


DEFAULT_MODEL_ID = ""
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"
DEFAULT_TIMEOUT = 30  # seconds
DEFAULT_NUM_CONNECTIONS = 10  # connections per client

BACKOFF_FACTOR = 1
MAX_RETRIES = 3

logger = logging.getLogger(__name__)


def update_buffer(buffer: str, chunk_bytes: bytes) -> Tuple[str, List[Dict[str, Any]]]:
    buffer += chunk_bytes.decode("utf-8")
    outputs = []
    while "{" in buffer and "}" in buffer:
        start_index = buffer.find("{")
        end_index = buffer.find("}", start_index)
        if start_index != -1 and end_index != -1:
            try:
                chunk_json = json.loads(buffer[start_index : end_index + 1])
                audio = base64.b64decode(chunk_json["data"])
                outputs.append({"audio": audio, "sampling_rate": chunk_json["sampling_rate"]})
                buffer = buffer[end_index + 1 :]
            except json.JSONDecodeError:
                break
    return buffer, outputs


def convert_response(response: Dict[str, any], include_context_id: bool) -> Dict[str, Any]:
    audio = base64.b64decode(response["data"])

    optional_kwargs = {}
    if include_context_id:
        optional_kwargs["context_id"] = response["context_id"]

    return {
        "audio": audio,
        "sampling_rate": response["sampling_rate"],
        **optional_kwargs,
    }


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library.

    This client contains methods to interact with the Cartesia text-to-speech API.
    The client can be used to retrieve available voices, compute new voice embeddings,
    and generate speech from text.

    The client also supports generating audio using a websocket for lower latency.

    Examples:
        >>> client = CartesiaTTS()

        # Load available voices and their metadata (excluding the embeddings).
        # Embeddings are fetched with `get_voice_embedding`. This avoids preloading
        # all of the embeddings, which can be expensive if there are a lot of voices.
        >>> voices = client.get_voices()
        >>> embedding = client.get_voice_embedding(voice_id=voices["Milo"]["id"])
        >>> audio = client.generate(transcript="Hello world!", voice=embedding)

        # Preload all available voices and their embeddings if you plan on reusing
        # all of the embeddings often.
        >>> voices = client.get_voices(skip_embeddings=False)
        >>> embedding = voices["Milo"]["embedding"]
        >>> audio = client.generate(transcript="Hello world!", voice=embedding)

        # Generate audio stream
        >>> for audio_chunk in client.generate(transcript="Hello world!", voice=embedding, stream=True):
        ...     audio, sr = audio_chunk["audio"], audio_chunk["sampling_rate"]
    """

    def __init__(self, *, api_key: str = None):
        """Args:
        api_key: The API key to use for authorization.
            If not specified, the API key will be read from the environment variable
            `CARTESIA_API_KEY`.
        """
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self.api_version = os.environ.get("CARTESIA_API_VERSION", DEFAULT_API_VERSION)
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        self.websocket = None

    def get_voices(self, skip_embeddings: bool = True) -> Dict[str, VoiceMetadata]:
        """Returns a mapping from voice name -> voice metadata.

        Args:
            skip_embeddings: Whether to skip returning the embeddings.
                It is recommended to skip if you only want to see what
                voices are available, since loading embeddings for all your voices can be expensive.
                You can then use ``get_voice_embedding`` to get the embeddings for the voices you are
                interested in.

        Returns:
            A mapping from voice name -> voice metadata.

        Note:
            If the voice name is not unique, there is undefined behavior as to which
            voice will correspond to the name. To be more thorough, look at the web
            client to find the `voice_id` for the voice you are looking for.

        Usage:
            >>> client = CartesiaTTS()
            >>> voices = client.get_voices()
            >>> voices
                {
                    "Jane": {
                        "id": "c1d1d3a8-6f4e-4b3f-8b3e-2e1b3e1b3e1b",
                        "name": "Jane",
                }
            >>> embedding = client.get_voice_embedding(voice_id=voices["Jane"]["id"])
            >>> audio = client.generate(transcript="Hello world!", voice=embedding)
        """
        params = {"select": "id, name, description"} if skip_embeddings else None
        response = httpx.get(
            f"{self._http_url()}/voices",
            headers=self.headers,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )

        if not response.is_success:
            raise ValueError(f"Failed to get voices. Error: {response.text}")

        voices = response.json()
        for voice in voices:
            if "embedding" in voice and isinstance(voice["embedding"], str):
                voice["embedding"] = json.loads(voice["embedding"])
        return {voice["name"]: voice for voice in voices}

    @retry_on_connection_error(
        max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, logger=logger
    )
    def get_voice_embedding(
        self, *, voice_id: str = None, filepath: str = None, link: str = None
    ) -> Embedding:
        """Get a voice embedding from voice_id, a filepath or YouTube url.

        Args:
            voice_id: The voice id.
            filepath: Path to audio file from which to get the audio.
            link: The url to get the audio from. Currently only supports youtube shared urls.

        Returns:
            The voice embedding.

        Raises:
            ValueError: If more than one of `voice_id`, `filepath` or `link` is specified.
                Only one should be specified.
        """
        if sum(bool(x) for x in (voice_id, filepath, link)) != 1:
            raise ValueError("Exactly one of `voice_id`, `filepath` or `url` should be specified.")

        if voice_id:
            url = f"{self._http_url()}/voices/embedding/{voice_id}"
            response = httpx.get(url, headers=self.headers, timeout=DEFAULT_TIMEOUT)
        elif filepath:
            url = f"{self._http_url()}/voices/clone/clip"
            files = {"clip": open(filepath, "rb")}
            headers = self.headers.copy()
            # The default content type of JSON is incorrect for file uploads
            headers.pop("Content-Type")
            response = httpx.post(url, headers=headers, files=files, timeout=DEFAULT_TIMEOUT)
        elif link:
            url = f"{self._http_url()}/voices/clone/url"
            params = {"link": link}
            response = httpx.post(url, headers=self.headers, params=params, timeout=DEFAULT_TIMEOUT)

        if not response.is_success:
            raise ValueError(
                f"Failed to clone voice. Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        # Handle successful response
        out = response.json()
        embedding = out["embedding"]
        if isinstance(embedding, str):
            embedding = json.loads(embedding)
        return embedding

    def refresh_websocket(self):
        """Refresh the websocket connection.

        Note:
            The connection is synchronous.
        """
        if self.websocket is None or self._is_websocket_closed():
            route = "audio/websocket"
            self.websocket = connect(f"{self._ws_url()}/{route}?api_key={self.api_key}")

    def _is_websocket_closed(self):
        return self.websocket.socket.fileno() == -1

    def _check_inputs(
        self,
        transcript: str,
        duration: Optional[float],
        chunk_time: Optional[float],
        output_format: Union[str, AudioOutputFormat],
        data_rtype: Union[str, AudioDataReturnType],
    ):
        # This will try the casting and raise an error.
        _ = AudioOutputFormat(output_format)

        if AudioDataReturnType(data_rtype) == AudioDataReturnType.ARRAY and not _NUMPY_AVAILABLE:
            raise ImportError(
                "The 'numpy' package is required to use the 'array' return type. "
                "Please install 'numpy' or use 'bytes' as the return type."
            )

        if chunk_time is not None:
            if chunk_time < 0.1 or chunk_time > 0.5:
                raise ValueError("`chunk_time` must be between 0.1 and 0.5")

        if chunk_time is not None and duration is not None:
            if duration < chunk_time:
                raise ValueError("`duration` must be greater than chunk_time")

        if transcript.strip() == "":
            raise ValueError("`transcript` must be non empty")

    def _generate_request_body(
        self,
        *,
        transcript: str,
        voice: Embedding,
        model_id: str,
        output_format: AudioOutputFormat,
        duration: int = None,
        chunk_time: float = None,
    ) -> Dict[str, Any]:
        """Create the request body for a stream request.

        Note that anything that's not provided will use a default if available or be
        filtered out otherwise.
        """
        body = dict(transcript=transcript, model_id=model_id, voice=voice)
        output_format = output_format.value

        optional_body = dict(
            duration=duration,
            chunk_time=chunk_time,
            output_format=output_format,
        )
        body.update({k: v for k, v in optional_body.items() if v is not None})

        return body

    def generate(
        self,
        *,
        transcript: str,
        voice: Embedding,
        model_id: str = DEFAULT_MODEL_ID,
        duration: int = None,
        chunk_time: float = None,
        stream: bool = False,
        websocket: bool = True,
        output_format: Union[str, AudioOutputFormat] = "fp32",
        data_rtype: str = "bytes",
    ) -> Union[AudioOutput, Generator[AudioOutput, None, None]]:
        """Generate audio from a transcript.

        Args:
            transcript (str): The text to generate audio for.
            voice (Embedding (List[float])): The voice to use for generating audio.
            duration (int, optional): The maximum duration of the audio in seconds.
            chunk_time (float, optional): How long each audio segment should be in seconds.
                This should not need to be adjusted.
            stream (bool, optional): Whether to stream the audio or not.
                If True this function returns a generator. False by default.
            websocket (bool, optional): Whether to use a websocket for streaming audio.
                Using the websocket reduces latency by pre-poning the handshake. True by default.
            data_rtype: The return type for the 'data' key in the dictionary.
                One of `'byte' | 'array'`.
                Note this field is experimental and may be deprecated in the future.

        Returns:
            A generator if `stream` is True, otherwise a dictionary.
            Dictionary from both generator and non-generator return types have the following keys:
                * "audio": The audio as a bytes buffer.
                * "sampling_rate": The sampling rate of the audio.
        """
        self._check_inputs(transcript, duration, chunk_time, output_format, data_rtype)

        data_rtype = AudioDataReturnType(data_rtype)
        output_format = AudioOutputFormat(output_format)

        body = self._generate_request_body(
            transcript=transcript,
            voice=voice,
            model_id=model_id,
            duration=duration,
            chunk_time=chunk_time,
            output_format=output_format,
        )

        if websocket:
            generator = self._generate_ws(body)
        else:
            generator = self._generate_http_wrapper(body)

        generator = self._postprocess_audio(
            generator, data_rtype=data_rtype, output_format=output_format
        )
        if stream:
            return generator

        chunks = []
        sampling_rate = None
        for chunk in generator:
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        if data_rtype == AudioDataReturnType.ARRAY:
            cat = np.concatenate
        else:
            cat = b"".join

        return {"audio": cat(chunks), "sampling_rate": sampling_rate}

    def _postprocess_audio(
        self,
        generator: Generator[AudioOutput, None, None],
        *,
        data_rtype: AudioDataReturnType,
        output_format: AudioOutputFormat,
    ) -> Generator[AudioOutput, None, None]:
        """Perform postprocessing on the generator outputs.

        The postprocessing should be minimal (e.g. converting to array, casting dtype).
        This code should not perform heavy operations like changing the sampling rate.

        Args:
            generator: A generator that yields audio chunks.
            data_rtype: The data return type.
            output_format: The output format for the audio.

        Returns:
            A generator that yields audio chunks.
        """
        dtype = None
        if data_rtype == AudioDataReturnType.ARRAY:
            dtype = np.float32 if "fp32" in output_format.value else np.int16

        for chunk in generator:
            if dtype is not None:
                chunk["audio"] = np.frombuffer(chunk["audio"], dtype=dtype)
            yield chunk

    @retry_on_connection_error(
        max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, logger=logger
    )
    def _generate_http_wrapper(self, body: Dict[str, Any]):
        """Need to wrap the http generator in a function for the retry decorator to work."""
        try:
            for chunk in self._generate_http(body):
                yield chunk
        except Exception as e:
            logger.error(f"Failed to generate audio. {e}")
            raise e

    def _generate_http(self, body: Dict[str, Any]):
        response = requests.post(
            f"{self._http_url()}/audio/sse",
            stream=True,
            data=json.dumps(body),
            headers=self.headers,
            timeout=(DEFAULT_TIMEOUT, DEFAULT_TIMEOUT),
        )
        if not response.ok:
            raise ValueError(f"Failed to generate audio. {response.text}")

        buffer = ""
        for chunk_bytes in response.iter_content(chunk_size=None):
            buffer, outputs = update_buffer(buffer, chunk_bytes)
            for output in outputs:
                yield output

        if buffer:
            try:
                chunk_json = json.loads(buffer)
                audio = base64.b64decode(chunk_json["data"])
                yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
            except json.JSONDecodeError:
                pass

    def _generate_ws(self, body: Dict[str, Any], *, context_id: str = None):
        """Generate audio using the websocket connection.

        Args:
            body: The request body.
            context_id: The context id for the request.
                The context id must be globally unique for the duration this client exists.
                If this is provided, the context id that is in the response will
                also be returned as part of the dict. This is helpful for testing.
        """
        if not self.websocket or self._is_websocket_closed():
            self.refresh_websocket()

        include_context_id = bool(context_id)
        if context_id is None:
            context_id = uuid.uuid4().hex
        self.websocket.send(json.dumps({"data": body, "context_id": context_id}))
        try:
            while True:
                response = json.loads(self.websocket.recv())
                if "error" in response:
                    raise RuntimeError(f"Error generating audio:\n{response['error']}")
                if response["done"]:
                    break

                yield convert_response(response, include_context_id)
        except Exception as e:
            # Close the websocket connection if an error occurs.
            if self.websocket and not self._is_websocket_closed():
                self.websocket.close()
            raise RuntimeError(f"Failed to generate audio. {response}") from e
        finally:
            # Ensure the websocket is ultimately closed.
            if self.websocket and not self._is_websocket_closed():
                self.websocket.close()

    def prepare_audio_and_headers(
        self, raw_audio: Union[bytes, str]
    ) -> Tuple[bytes, Dict[str, Any]]:
        if isinstance(raw_audio, str):
            with open(raw_audio, "rb") as f:
                raw_audio_bytes = f.read()
        else:
            raw_audio_bytes = raw_audio
        # application/json is not the right content type for this request
        headers = {k: v for k, v in self.headers.items() if k != "Content-Type"}
        return raw_audio_bytes, headers

    def _http_url(self):
        prefix = "http" if "localhost" in self.base_url else "https"
        return f"{prefix}://{self.base_url}/{self.api_version}"

    def _ws_url(self):
        prefix = "ws" if "localhost" in self.base_url else "wss"
        return f"{prefix}://{self.base_url}/{self.api_version}"

    def close(self):
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()

    def __del__(self):
        self.close()

    def __enter__(self):
        self.refresh_websocket()
        return self

    def __exit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        self.close()


class AsyncCartesiaTTS(CartesiaTTS):
    def __init__(self, *, api_key: str = None):
        self._session = None
        self._loop = None
        super().__init__(api_key=api_key)

    async def _get_session(self):
        current_loop = asyncio.get_event_loop()
        if self._loop is not current_loop:
            # If the loop has changed, close the session and create a new one.
            await self.close()
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
            connector = aiohttp.TCPConnector(limit=DEFAULT_NUM_CONNECTIONS)
            self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
            self._loop = current_loop
        return self._session

    async def refresh_websocket(self):
        """Refresh the websocket connection."""
        if self.websocket is None or self._is_websocket_closed():
            route = "audio/websocket"
            session = await self._get_session()
            self.websocket = await session.ws_connect(
                f"{self._ws_url()}/{route}?api_key={self.api_key}"
            )

    def _is_websocket_closed(self):
        return self.websocket.closed

    async def close(self):
        """This method closes the websocket and the session.

        It is *strongly* recommended to call this method when you are done using the client.
        """
        if self.websocket is not None and not self._is_websocket_closed():
            await self.websocket.close()
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def generate(
        self,
        *,
        transcript: str,
        voice: Embedding,
        model_id: str = DEFAULT_MODEL_ID,
        duration: int = None,
        chunk_time: float = None,
        stream: bool = False,
        websocket: bool = True,
        output_format: Union[str, AudioOutputFormat] = "fp32",
        data_rtype: Union[str, AudioDataReturnType] = "bytes",
    ) -> Union[AudioOutput, AsyncGenerator[AudioOutput, None]]:
        """Asynchronously generate audio from a transcript.

        For more information on the arguments, see the synchronous :meth:`CartesiaTTS.generate`.
        """
        self._check_inputs(transcript, duration, chunk_time, output_format, data_rtype)
        data_rtype = AudioDataReturnType(data_rtype)
        output_format = AudioOutputFormat(output_format)

        body = self._generate_request_body(
            transcript=transcript,
            voice=voice,
            model_id=model_id,
            duration=duration,
            chunk_time=chunk_time,
            output_format=output_format,
        )

        if websocket:
            generator = self._generate_ws(body)
        else:
            generator = self._generate_http_wrapper(body)
        generator = self._postprocess_audio(
            generator, data_rtype=data_rtype, output_format=output_format
        )
        if stream:
            return generator

        chunks = []
        sampling_rate = None
        async for chunk in generator:
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        if data_rtype == AudioDataReturnType.ARRAY:
            cat = np.concatenate
        else:
            cat = b"".join

        return {"audio": cat(chunks), "sampling_rate": sampling_rate}

    async def _postprocess_audio(
        self,
        generator: AsyncGenerator[AudioOutput, None],
        *,
        data_rtype: AudioDataReturnType,
        output_format: AudioOutputFormat,
    ) -> AsyncGenerator[AudioOutput, None]:
        """See :meth:`CartesiaTTS._postprocess_audio`."""
        dtype = None
        if data_rtype == AudioDataReturnType.ARRAY:
            dtype = np.float32 if "fp32" in output_format.value else np.int16

        async for chunk in generator:
            if dtype is not None:
                chunk["audio"] = np.frombuffer(chunk["audio"], dtype=dtype)
            yield chunk

    @retry_on_connection_error_async(
        max_retries=MAX_RETRIES, backoff_factor=BACKOFF_FACTOR, logger=logger
    )
    async def _generate_http_wrapper(self, body: Dict[str, Any]):
        """Need to wrap the http generator in a function for the retry decorator to work."""
        try:
            async for chunk in self._generate_http(body):
                yield chunk
        except Exception as e:
            logger.error(f"Failed to generate audio. {e}")
            raise e

    async def _generate_http(self, body: Dict[str, Any]):
        session = await self._get_session()
        async with session.post(
            f"{self._http_url()}/audio/sse", data=json.dumps(body), headers=self.headers
        ) as response:
            if not response.ok:
                raise ValueError(f"Failed to generate audio. {await response.text()}")

            buffer = ""
            async for chunk_bytes in response.content.iter_any():
                buffer, outputs = update_buffer(buffer, chunk_bytes)
                for output in outputs:
                    yield output

            if buffer:
                try:
                    chunk_json = json.loads(buffer)
                    audio = base64.b64decode(chunk_json["data"])
                    yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
                except json.JSONDecodeError:
                    pass

    async def _generate_ws(self, body: Dict[str, Any], *, context_id: str = None):
        include_context_id = bool(context_id)
        if not self.websocket or self._is_websocket_closed():
            await self.refresh_websocket()

        ws = self.websocket
        if context_id is None:
            context_id = uuid.uuid4().hex
        await ws.send_json({"data": body, "context_id": context_id})
        try:
            response = None
            while True:
                response = await ws.receive_json()
                if response["done"]:
                    break

                yield convert_response(response, include_context_id)
        except Exception as e:
            if self.websocket and not self._is_websocket_closed():
                await self.websocket.close()
            error_msg_end = "" if response is None else f": {await response.text()}"
            raise RuntimeError(f"Failed to generate audio{error_msg_end}") from e
        finally:
            # Ensure the websocket is ultimately closed.
            if self.websocket and not self._is_websocket_closed():
                await self.websocket.close()

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        else:
            loop.create_task(self.close())

    async def __aenter__(self):
        await self.refresh_websocket()
        return self

    async def __aexit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        await self.close()
