import base64
import json
import os
from collections import defaultdict
from typing import Dict, List, TypedDict, Union

import numpy as np
import requests

DEFAULT_MODEL_ID = "genial-planet-1346"
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"


class AudioOutput(TypedDict):
    audio: np.ndarray
    sampling_rate: int


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library."""

    def __init__(self, *, model_id: str = None, api_key: str = None):
        """
        Args:
            api_key: The API key to use for authorization.
                The api key is not currently enforced.
                TODO: Set the API key.
        """
        self.model_id = model_id or DEFAULT_MODEL_ID
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self.api_version = os.environ.get("CARTESIA_API_VERSION", DEFAULT_API_VERSION)
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

        # Mapping from model_id -> {voice_id: embedding}
        self._voices: Dict[str, Dict[str, List[float]]] = defaultdict(defaultdict)

    def models(self) -> List[str]:
        """Get a list of available models."""
        raise NotImplementedError()

    def voices(self, model_id: str = None, *, refresh: bool = False) -> List[str]:
        """Returns a list of voices for a given model.

        These voices can be used with :method:`CartesiaTTS.generate` to generate audio.

        Args:
            model_id: The model to get voices for.
            refresh: If ``True``, the API will be pinged if the voices for the model
                are not already cached. Otherwise, default to the cached voices.

        Returns:
            List[str]: The list of voice ids for the model.
        """
        model_id = model_id or self.model_id
        if model_id in self._voices:
            return self._voices[model_id]

        response = requests.get(
            f"{self._http_url()}/models/{model_id}/voices", headers=self.headers
        )

        if response.status_code != 200:
            raise ValueError(f"Failed to get voices for model {model_id}. Error: {response.text}")

        return json.loads(response.text)

    def clone_voice(self, voice_id: str, *, filepath: str = None, link: str = None) -> List[float]:
        """Clone a voice from a filepath or YouTube url.

        Args:
            voice_id: The id to give to the voice.
            filepath: Path to audio file from which to get the audio.
            link: The url to get the audio from. Currently only supports youtube shared urls.

        Note:
            Only one of `filepath` or `link` should be specified.

        Note:
            This voice will not persist over different clients. If you would like to reuse
            the voice, you will have to save the voice embedding.

        Note:
            Voice cloning is only supported for the latest model.

        Returns:
            Dict[str, Any]: The voice embedding.
        """
        if filepath and link:
            raise ValueError("Only one of `filepath` or `url` should be specified.")

        if filepath:
            url = f"{self._http_url()}/voices/clone/clip"
            params = {"clip": open(filepath, "rb")}
            response = requests.post(url, headers=self.headers, params=params)
        else:
            url = f"{self._http_url()}/voices/clone/url"
            params = {"link": link}
            print(f"params: {params}, url: {url}, headers: {self.headers}")
            response = requests.post(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise ValueError(
                f"Failed to clone voice. Status Code: {response.status_code}\n"
                f"Error: {response.text}"
            )

        # Handle successful response
        out = response.json()
        model_id = out["model_id"]
        embedding = out["embedding"]
        self._voices[model_id][voice_id] = embedding

        return embedding

    def generate(
        self,
        model_id: str = None,
        *,
        transcript: str,
        duration: int = None,
        chunk_time: float = None,
        lookahead: int = None,
        voice: Union[str, List[float]] = None,
        stream: bool = False,
    ) -> AudioOutput:
        """Generate audio from a transcript.

        Args:
            model_id: The model to use for generating audio.
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

        Returns:
            A dictionary containing:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        model_id = model_id or DEFAULT_MODEL_ID
        body = dict(transcript=transcript, model_id=model_id)

        if isinstance(voice, str):
            voice = self._voices[model_id][voice]

        optional_body = dict(
            duration=duration,
            chunk_time=chunk_time,
            lookahead=lookahead,
            voice=voice,
        )
        body.update({k: v for k, v in optional_body.items() if v is not None})

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

        if stream:
            return generator()

        chunks = []
        sampling_rate = None
        for chunk in generator():
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        return {"audio": np.concatenate(chunks), "sampling_rate": sampling_rate}

    def _http_url(self):
        prefix = "http" if "localhost" in self.base_url else "https"
        return f"{prefix}://{self.base_url}/{self.api_version}"
