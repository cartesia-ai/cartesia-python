import base64
import json
import os
import uuid
from typing import Any, Dict, Generator, List, Optional, TypedDict, Union

import numpy as np
import requests
from websockets.sync.client import connect

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
    embedding: Optional[Embedding]


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
        self.websocket = None
        self.refresh_websocket()

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
        if isinstance(out["embedding"], str):
            out["embedding"] = json.loads(out["embedding"])
        return out["embedding"]

    def refresh_websocket(self):
        """Refresh the websocket connection.

        Note:
            The connection is synchronous.
        """
        if self.websocket and not self._is_websocket_closed():
            self.websocket.close()
        self.websocket = connect(
            f"{self._ws_url()}/audio/websocket?api_key={self.api_key}",
            close_timeout=None,
        )

    def _is_websocket_closed(self):
        return self.websocket.socket.fileno() == -1

    def generate(
        self,
        *,
        transcript: str,
        duration: int = None,
        chunk_time: float = None,
        lookahead: int = None,
        voice: Embedding = None,
        stream: bool = False,
        websocket: bool = True,
    ) -> Union[AudioOutput, Generator[AudioOutput, None, None]]:
        """Generate audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            duration: The maximum duration of the audio in seconds.
            chunk_time: How long each audio segment should be in seconds.
                This should not need to be adjusted.
            lookahead: The number of seconds to look ahead for each chunk.
                This should not need to be adjusted.
            voice: The voice to use for generating audio.
                This can either be a voice id (string) or an embedding vector (List[float]).
            stream: Whether to stream the audio or not.
                If ``True`` this function returns a generator.
            websocket: Whether to use a websocket for streaming audio.
                Using the websocket reduces latency by pre-poning the handshake.

        Returns:
            A generator if `stream` is True, otherwise a dictionary.
            Dictionary from both generator and non-generator return types have the following keys:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = dict(transcript=transcript, model_id=DEFAULT_MODEL_ID)

        if isinstance(voice, str):
            voice = self._voices[voice]

        optional_body = dict(
            duration=duration,
            chunk_time=chunk_time,
            lookahead=lookahead,
            voice=voice,
        )
        body.update({k: v for k, v in optional_body.items() if v is not None})

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

        return {"audio": np.concatenate(chunks), "sampling_rate": sampling_rate}

    def _generate_http(self, body: Dict[str, Any]):
        response = requests.post(
            f"{self._http_url()}/audio/stream",
            stream=True,
            data=json.dumps(body),
            headers=self.headers,
        )
        if response.status_code != 200:
            raise ValueError(f"Failed to generate audio. {response.text}")

        buffer = ""
        for chunk_bytes in response.iter_content(chunk_size=None):
            buffer += chunk_bytes.decode("utf-8")
            while "{" in buffer and "}" in buffer:
                start_index = buffer.find("{")
                end_index = buffer.find("}", start_index)
                if start_index != -1 and end_index != -1:
                    try:
                        chunk_json = json.loads(buffer[start_index : end_index + 1])
                        data = base64.b64decode(chunk_json["data"])
                        audio = np.frombuffer(data, dtype=np.float32)
                        yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
                        buffer = buffer[end_index + 1 :]
                    except json.JSONDecodeError:
                        break

        if buffer:
            try:
                chunk_json = json.loads(buffer)
                data = base64.b64decode(chunk_json["data"])
                audio = np.frombuffer(data, dtype=np.float32)
                yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
            except json.JSONDecodeError:
                pass

    def _generate_ws(self, body: Dict[str, Any]):
        if not self.websocket or self._is_websocket_closed():
            self.refresh_websocket()

        self.websocket.send(json.dumps({"data": body, "context_id": uuid.uuid4().hex}))
        try:
            response = json.loads(self.websocket.recv())
            while not response["done"]:
                data = base64.b64decode(response["data"])
                audio = np.frombuffer(data, dtype=np.float32)
                # print("timing", time.perf_counter() - start)
                yield {"audio": audio, "sampling_rate": response["sampling_rate"]}

                response = json.loads(self.websocket.recv())
        except Exception:
            raise RuntimeError(f"Failed to generate audio. {response}")

    def _http_url(self):
        prefix = "http" if "localhost" in self.base_url else "https"
        return f"{prefix}://{self.base_url}/{self.api_version}"

    def _ws_url(self):
        prefix = "ws" if "localhost" in self.base_url else "wss"
        return f"{prefix}://{self.base_url}/{self.api_version}"

    def __del__(self):
        if self.websocket.socket.fileno() > -1:
            self.websocket.close()
