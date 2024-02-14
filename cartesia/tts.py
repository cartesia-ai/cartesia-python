import base64
import json
import os
from typing import List

import numpy as np
import requests

DEFAULT_MODEL_ID = "echo_tts_v0.0.6"

DEFAULT_BASE_URL = "api.cartesia.ai"


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library."""

    def __init__(self, *, model_id: str = None, api_key: str = None):
        """
        Args:
            api_key: The API key to use for authorization.
        """
        self.model_id = model_id or DEFAULT_MODEL_ID
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)

    def models(self) -> List[str]:
        """Get a list of available models."""
        raise NotImplementedError()

    def voices(self, model_id: str = None) -> List[str]:
        """Returns a list of voices for a given model."""
        model_id = model_id or self.model_id
        response = requests.get(f"{self._http_url()}/models/{model_id}/voices")

        if response.status_code != 200:
            raise ValueError(f"Failed to get voices for model {model_id}. {response.text}")

        return json.loads(response.text)

    def generate(
        self,
        *,
        model_id: str = None,
        transcript: str,
        duration: int = None,
        chunk_time: float = None,
        lookahead: int = None,
        voice: str = None,
        stream: bool = False,
    ):
        body = dict(
            transcript=transcript,
            model_id=model_id or DEFAULT_MODEL_ID,
        )

        if isinstance(voice, str):
            voice = {"sources": [voice], "weights": [1.0]}

        optional_body = dict(
            duration=duration,
            chunk_time=chunk_time,
            lookahead=lookahead,
            voice=voice,
        )
        body.update({k: v for k, v in optional_body.items() if v is not None})

        response = requests.post(f"{self._http_url()}/stream", stream=True, data=json.dumps(body))
        if response.status_code != 200:
            raise ValueError(f"Failed to generate audio. {response.text}")

        delimiter = b"}{"

        def generator():
            accumulated_data = b""
            for chunk in response.iter_content(chunk_size=None):
                if not chunk:
                    continue

                accumulated_data += chunk

                while delimiter in accumulated_data:
                    partial_data, rest = accumulated_data.split(delimiter, 1)
                    partial_data += b"}"

                    data_dict = json.loads(partial_data.decode("utf-8"))
                    data = base64.b64decode(data_dict["data"])
                    audio = np.frombuffer(data, dtype=np.float32)

                    yield {"audio": audio, "sampling_rate": data_dict["sampling_rate"]}

                    accumulated_data = b"{" + rest

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
        return f"{prefix}://{self.base_url}"
