import asyncio
import base64
import json
import os
import uuid
from types import TracebackType
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Tuple, TypedDict, Union

import aiohttp
import httpx
import requests
from websockets.sync.client import connect

DEFAULT_MODEL_ID = "genial-planet-1346"
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"
DEFAULT_TIMEOUT = 60  # seconds
DEFAULT_NUM_CONNECTIONS = 10  # connections per client


class AudioOutput(TypedDict):
    audio: bytes
    sampling_rate: int


Embedding = List[float]


class VoiceMetadata(TypedDict):
    id: str
    name: str
    description: str
    embedding: Optional[Embedding]


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
    To enable interrupt handling along the websocket, set `experimental_ws_handle_interrupts=True`.

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

    def __init__(self, *, api_key: str = None, experimental_ws_handle_interrupts: bool = False):
        """
        Args:
            api_key: The API key to use for authorization.
                If not specified, the API key will be read from the environment variable
                `CARTESIA_API_KEY`.
            experimental_ws_handle_interrupts: Whether to handle interrupts when generating
                audio using the websocket. This is an experimental feature and may have bugs
                or be deprecated in the future.
        """
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self.api_version = os.environ.get("CARTESIA_API_VERSION", DEFAULT_API_VERSION)
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}
        self.websocket = None
        self.experimental_ws_handle_interrupts = experimental_ws_handle_interrupts

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
        # TODO: Update the API to return the embedding as a list of floats rather than string.
        if not skip_embeddings:
            for voice in voices:
                voice["embedding"] = json.loads(voice["embedding"])
        return {voice["name"]: voice for voice in voices}

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
        if isinstance(out["embedding"], str):
            out["embedding"] = json.loads(out["embedding"])
        return out["embedding"]

    def refresh_websocket(self):
        """Refresh the websocket connection.

        Note:
            The connection is synchronous.
        """
        if self.websocket is None or self._is_websocket_closed():
            route = "audio/websocket"
            if self.experimental_ws_handle_interrupts:
                route = f"experimental/{route}"
            self.websocket = connect(f"{self._ws_url()}/{route}?api_key={self.api_key}")

    def _is_websocket_closed(self):
        return self.websocket.socket.fileno() == -1

    def _check_inputs(
        self, transcript: str, duration: Optional[float], chunk_time: Optional[float]
    ):
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
        duration: int = None,
        chunk_time: float = None,
    ) -> Dict[str, Any]:
        """
        Create the request body for a stream request.
        Note that anything that's not provided will use a default if available or be filtered out otherwise.
        """
        body = dict(transcript=transcript, model_id=DEFAULT_MODEL_ID, voice=voice)

        optional_body = dict(
            duration=duration,
            chunk_time=chunk_time,
        )
        body.update({k: v for k, v in optional_body.items() if v is not None})

        return body

    def generate(
        self,
        *,
        transcript: str,
        voice: Embedding,
        duration: int = None,
        chunk_time: float = None,
        stream: bool = False,
        websocket: bool = True,
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

        Returns:
            A generator if `stream` is True, otherwise a dictionary.
            Dictionary from both generator and non-generator return types have the following keys:
                * "audio": The audio as a bytes buffer.
                * "sampling_rate": The sampling rate of the audio.
        """
        self._check_inputs(transcript, duration, chunk_time)

        body = self._generate_request_body(
            transcript=transcript, voice=voice, duration=duration, chunk_time=chunk_time
        )

        if websocket:
            generator = self._generate_ws(body)
        else:
            generator = self._generate_http(body)

        if stream:
            return generator

        chunks = []
        sampling_rate = None
        for chunk in generator:
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        return {"audio": b"".join(chunks), "sampling_rate": sampling_rate}

    def _generate_http(self, body: Dict[str, Any]):
        response = requests.post(
            f"{self._http_url()}/audio/stream",
            stream=True,
            data=json.dumps(body),
            headers=self.headers,
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
                if response["done"]:
                    break

                yield convert_response(response, include_context_id)

                if self.experimental_ws_handle_interrupts:
                    self.websocket.send(json.dumps({"context_id": context_id}))
        except GeneratorExit:
            # The exit is only called when the generator is garbage collected.
            # It may not be called directly after a break statement.
            # However, the generator will be automatically cancelled on the next request.
            if self.experimental_ws_handle_interrupts:
                self.websocket.send(json.dumps({"context_id": context_id, "action": "cancel"}))
        except Exception as e:
            raise RuntimeError(f"Failed to generate audio. {response}") from e

    def transcribe(self, raw_audio: Union[bytes, str]) -> str:
        raw_audio_bytes, headers = self.prepare_audio_and_headers(raw_audio)
        response = httpx.post(
            f"{self._http_url()}/audio/transcriptions",
            headers=headers,
            files={"clip": ("input.wav", raw_audio_bytes)},
            timeout=DEFAULT_TIMEOUT,
        )

        if not response.is_success:
            raise ValueError(f"Failed to transcribe audio. Error: {response.text()}")

        transcript = response.json()
        return transcript["text"]

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
    def __init__(self, *, api_key: str = None, experimental_ws_handle_interrupts: bool = False):
        self.timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
        self.connector = aiohttp.TCPConnector(limit=DEFAULT_NUM_CONNECTIONS)
        self._session = aiohttp.ClientSession(timeout=self.timeout, connector=self.connector)
        super().__init__(
            api_key=api_key, experimental_ws_handle_interrupts=experimental_ws_handle_interrupts
        )

    async def refresh_websocket(self):
        """Refresh the websocket connection."""
        if self.websocket is None or self._is_websocket_closed():
            route = "audio/websocket"
            if self.experimental_ws_handle_interrupts:
                route = f"experimental/{route}"
            self.websocket = await self._session.ws_connect(
                f"{self._ws_url()}/{route}?api_key={self.api_key}"
            )

    async def generate(
        self,
        *,
        transcript: str,
        voice: Embedding,
        duration: int = None,
        chunk_time: float = None,
        stream: bool = False,
        websocket: bool = True,
    ) -> Union[AudioOutput, AsyncGenerator[AudioOutput, None]]:
        """Asynchronously generate audio from a transcript.
        NOTE: This overrides the non-asynchronous generate method from the base class.
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

        Returns:
            A generator if `stream` is True, otherwise a dictionary.
            Dictionary from both generator and non-generator return types have the following keys:
                * "audio": The audio as a bytes buffer.
                * "sampling_rate": The sampling rate of the audio.
        """
        self._check_inputs(transcript, duration, chunk_time)

        body = self._generate_request_body(
            transcript=transcript, voice=voice, duration=duration, chunk_time=chunk_time
        )

        if websocket:
            generator = self._generate_ws(body)
        else:
            generator = self._generate_http(body)

        if stream:
            return generator

        chunks = []
        sampling_rate = None
        async for chunk in generator:
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        return {"audio": b"".join(chunks), "sampling_rate": sampling_rate}

    async def _generate_http(self, body: Dict[str, Any]):
        async with self._session.post(
            f"{self._http_url()}/audio/stream", data=json.dumps(body), headers=self.headers
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
        route = "audio/websocket"
        if self.experimental_ws_handle_interrupts:
            route = f"experimental/{route}"

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

                if self.experimental_ws_handle_interrupts:
                    await ws.send_json({"context_id": context_id})
        except GeneratorExit:
            # The exit is only called when the generator is garbage collected.
            # It may not be called directly after a break statement.
            # However, the generator will be automatically cancelled on the next request.
            if self.experimental_ws_handle_interrupts:
                await ws.send_json({"context_id": context_id, "action": "cancel"})
        except Exception as e:
            print(f"Context ID: {context_id}, Response: {response}")
            print(f"Error: {e}")
            raise RuntimeError(f"Failed to generate audio. {await response.text()}") from e

    async def transcribe(self, raw_audio: Union[bytes, str]) -> str:
        raw_audio_bytes, headers = self.prepare_audio_and_headers(raw_audio)
        data = aiohttp.FormData()
        data.add_field("clip", raw_audio_bytes, filename="input.wav", content_type="audio/wav")

        async with self._session.post(
            f"{self._http_url()}/audio/transcriptions", headers=headers, data=data
        ) as response:
            if not response.ok:
                raise ValueError(f"Failed to transcribe audio. Error: {await response.text()}")

            transcript = await response.json()
            return transcript["text"]

    def _is_websocket_closed(self):
        return self.websocket.closed

    async def close(self):
        if self.websocket is not None and not self._is_websocket_closed():
            await self.websocket.close()
        if not self._session.closed:
            await self._session.close()

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
