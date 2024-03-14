import base64
import json
import os
from typing import List, TypedDict, Optional, Generator, Union, AsyncGenerator
import numpy as np
import httpx

DEFAULT_MODEL_ID = "genial-planet-1346"
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"


class AudioOutput(TypedDict):
    audio: np.ndarray
    sampling_rate: int


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library."""

    def __init__(self, *, model_id: Optional[str] = None, api_key: Optional[str] = None):
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

    def models(self) -> List[str]:
        """Get a list of available models."""
        raise NotImplementedError()

    async def voices(self, model_id: Optional[str] = None) -> List[str]:
        """Returns a list of voices for a given model.

        Args:
            model_id: The model to get voices for.
        """
        model_id = model_id or self.model_id
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._http_url()}/models/{model_id}/voices", headers=self.headers
            )

        if response.status_code != 200:
            raise ValueError(f"Failed to get voices for model {model_id}. Error: {response.text}")

        return json.loads(response.text)

    async def generate(
        self,
        *,
        model_id: Optional[str] = None,
        transcript: str,
        duration: Optional[int] = None,
        chunk_time: Optional[float] = None,
        lookahead: Optional[int] = None,
        voice: Optional[str] = None,
        stream: bool = False,
    ) -> Union[AudioOutput, AsyncGenerator[AudioOutput, None]]:
        """Generate audio from a transcript.
        ...
        """
        body = {
            "transcript": transcript,
            "model_id": model_id or self.model_id,
        }

        # Add the optional parameters to the body if they are not None
        if duration is not None:
            body["duration"] = duration
        if chunk_time is not None:
            body["chunk_time"] = chunk_time
        if lookahead is not None:
            body["lookahead"] = lookahead
        if voice is not None:
            body["voice"] = voice

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._http_url()}/stream",
                json=body,
                headers=self.headers
            )

        if response.status_code != 200:
            raise ValueError(f"Failed to generate audio. {response.text}")

        async def generator() -> AsyncGenerator[AudioOutput, None]:
            async for chunk_bytes in response.aiter_bytes():
                chunk_json = json.loads(chunk_bytes)
                data = base64.b64decode(chunk_json["data"])
                audio = np.frombuffer(data, dtype=np.float32)
                yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}

        if stream:
            return generator()

        chunks = []
        sampling_rate = None
        async for chunk in generator():
            if sampling_rate is None:
                sampling_rate = chunk["sampling_rate"]
            chunks.append(chunk["audio"])

        return {
            "audio": np.concatenate(chunks),
            "sampling_rate": sampling_rate
        }

    def _http_url(self) -> str:
        prefix = "http" if "localhost" in self.base_url else "https"
        return f"{prefix}://{self.base_url}/{self.api_version}"
