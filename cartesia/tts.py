import base64
import json
import os
import sys
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, TypedDict

import aiohttp
import numpy as np
import requests

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
else:
    from typing import NotRequired


DEFAULT_MODEL_ID = "genial-planet-1346"
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"


class AudioOutput(TypedDict):
    audio: np.ndarray
    sampling_rate: int


Embedding = List[float]


class VoiceMetadata(TypedDict):
    id: str
    name: str
    description: str
    embedding: NotRequired[Embedding]


class GenerateOptions(TypedDict):
    """
    Options for generating audio.

    chunk_time: How long each audio segment should be in seconds.
        This should not need to be adjusted.
    duration: The maximum duration of the audio in seconds.
    lookahead: The number of seconds to look ahead for each chunk.
        This should not need to be adjusted.
    """

    chunk_time: Optional[float]
    duration: Optional[int]
    lookahead: Optional[int]


DEFAULT_TIMEOUT = 60  # 60 seconds
DEFAULT_NUM_CONNECTIONS = 10  # 10 connections


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library.

    This client contains methods to interact with the Cartesia text-to-speech API.
    The API offers

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
        """
        Args:
            api_key: The API key to use for authorization.
                If not specified, the API key will be read from the environment variable
                `CARTESIA_API_KEY`.
        """
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self.api_version = os.environ.get("CARTESIA_API_VERSION", DEFAULT_API_VERSION)
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

        # Mapping from id -> embedding
        self._voices: Dict[str, List[float]] = {}
        self._downloaded_voices = False

        # Instantiate an AIOHTTP session
        self.timeout = aiohttp.ClientTimeout(total=DEFAULT_TIMEOUT)
        self.connector = aiohttp.TCPConnector(limit=DEFAULT_NUM_CONNECTIONS)
        self._session = None

    # Allows users to use the CartesiaTTS object as an async context manager
    async def __aenter__(self):
        self._session = aiohttp.ClientSession(timeout=self.timeout, connector=self.connector)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session is not None:
            await self._session.close()

    def models(self) -> List[str]:
        """Get a list of available models."""
        raise NotImplementedError()

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
        response = requests.get(f"{self._http_url()}/voices", headers=self.headers, params=params)

        if response.status_code != 200:
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
            response = requests.get(url, headers=self.headers)
        elif filepath:
            url = f"{self._http_url()}/voices/clone/clip"
            files = {"clip": open(filepath, "rb")}
            headers = self.headers.copy()
            # The default content type of JSON is incorrect for file uploads
            headers.pop("Content-Type")
            response = requests.post(url, headers=headers, files=files)
        elif link:
            url = f"{self._http_url()}/voices/clone/url"
            params = {"link": link}
            response = requests.post(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise ValueError(
                f"Failed to clone voice. Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        # Handle successful response
        out = response.json()
        return json.loads(out["embedding"])

    def _generate_request_body(
        self,
        *,
        transcript: str,
        voice: Embedding = None,
        options: Optional[GenerateOptions] = None,
    ) -> Dict[str, Any]:
        """
        Create the request body for a stream request.

        Note that anything that's not provided will use a default if available or be filtered out otherwise.
        """
        body = dict(transcript=transcript, model_id=DEFAULT_MODEL_ID, voice=voice)

        # Clone options
        if options:
            additional_options = {k: v for k, v in options.items() if v is not None}
            body.update(additional_options)

        return body

    def _extract_json_helper(self, buffer):
        try:
            obj, end = json.JSONDecoder().raw_decode(buffer)
            return obj, buffer[end:]
        except json.JSONDecodeError:
            return {}, buffer

    async def async_generate(
        self,
        *,
        transcript: str,
        voice: Embedding = None,
        options: Optional[GenerateOptions] = None,
    ) -> AudioOutput:
        """Asynchronously generate audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            voice: The embedding to use for generating audio.
            options: The options to use for generating audio. See :class:`GenerateOptions`.

        Returns:
            A dictionary containing the following:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript=transcript, voice=voice, options=options)
        print(self.headers)

        async with self._session.post(
            f"{self._http_url()}/audio/stream", data=json.dumps(body), headers=self.headers
        ) as response:
            if response.status != 200:
                raise ValueError(f"Failed to generate audio. {response.text}")

            chunks = []
            sampling_rate = None
            buffer = ""

            async for chunk_bytes in response.content.iter_any():
                buffer += chunk_bytes.decode("utf-8")
                try:
                    chunk_json, buffer = self._extract_json_helper(buffer)
                    data = base64.b64decode(chunk_json["data"])
                    audio = np.frombuffer(data, dtype=np.float32)
                    if sampling_rate is None:
                        sampling_rate = chunk_json.get("sampling_rate")
                    chunks.append(audio)
                except (json.JSONDecodeError, KeyError):
                    continue

            return {"audio": np.concatenate(chunks), "sampling_rate": sampling_rate}

    async def async_generate_stream(
        self,
        *,
        transcript: str,
        voice: Embedding = None,
        options: Optional[GenerateOptions] = None,
    ) -> AsyncGenerator[AudioOutput, None]:
        """Asynchronously generate an async generator of audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            voice: The embedding to use for generating audio.
            options: The options to use for generating audio. See :class:`GenerateOptions`.

        Returns:
            An async generator containing dictionaries with the following:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript=transcript, voice=voice, options=options)

        async def async_generator(request_body: dict, headers: dict):
            async with self._session.post(
                f"{self._http_url()}/audio/stream", data=json.dumps(request_body), headers=headers
            ) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to generate audio. {response.text}")
                buffer = ""
                async for chunk_bytes in response.content.iter_any():
                    buffer += chunk_bytes.decode("utf-8")
                    try:
                        chunk_json, buffer = self._extract_json_helper(buffer)
                        data = base64.b64decode(chunk_json["data"])
                        audio = np.frombuffer(data, dtype=np.float32)
                        yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
                    except (json.JSONDecodeError, KeyError):
                        continue

        return async_generator(request_body=body, headers=self.headers)

    def generate(
        self,
        *,
        transcript: str,
        voice: Embedding = None,
        options: Optional[GenerateOptions] = None,
    ) -> AudioOutput:
        """Generate audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            voice: The embedding to use for generating audio.
            options: The options to use for generating audio. See :class:`GenerateOptions`.

        Returns:
            A dictionary containing:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript=transcript, voice=voice, options=options)
        print(body)

        response = requests.post(
            f"{self._http_url()}/audio/stream",
            stream=True,
            data=json.dumps(body),
            headers=self.headers,
        )
        if response.status_code != 200:
            raise ValueError(f"Failed to generate audio. {response.text}")

        chunks = []
        sampling_rate = None
        for chunk_bytes in response.iter_content(chunk_size=None):
            chunk_json = json.loads(chunk_bytes)
            data = base64.b64decode(chunk_json["data"])
            audio = np.frombuffer(data, dtype=np.float32)
            if sampling_rate is None:
                sampling_rate = chunk_json.get("sampling_rate")
            chunks.append(audio)

        return {"audio": np.concatenate(chunks), "sampling_rate": sampling_rate}

    def generate_stream(
        self,
        *,
        transcript: str,
        voice: Embedding = None,
        options: Optional[GenerateOptions] = None,
    ) -> Generator[AudioOutput, None, None]:
        """Generate a generator of audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            voice: The embedding to use for generating audio.
            options: The options to use for generating audio. See :class:`GenerateOptions`.

        Returns:
            A generator for dictionaries containing:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript=transcript, voice=voice, options=options)

        response = requests.post(
            f"{self._http_url()}/audio/stream",
            stream=True,
            data=json.dumps(body),
            headers=self.headers,
        )
        if response.status_code != 200:
            raise ValueError(f"Failed to generate audio. {response.text}")

        def generator():
            for chunk_bytes in response.iter_content(chunk_size=None):
                chunk_json = json.loads(chunk_bytes)
                data = base64.b64decode(chunk_json["data"])
                audio = np.frombuffer(data, dtype=np.float32)
                yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}

        return generator()

    def _http_url(self):
        prefix = "http" if "localhost" in self.base_url else "https"
        return f"{prefix}://{self.base_url}/{self.api_version}"
