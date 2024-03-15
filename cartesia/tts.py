import base64
import json
import os
from typing import AsyncGenerator, Dict, Generator, List, Optional, TypedDict
import wave

import aiohttp
import numpy as np
import requests

DEFAULT_MODEL_ID = "genial-planet-1346"
DEFAULT_BASE_URL = "api.cartesia.ai"
DEFAULT_API_VERSION = "v0"


class AudioOutput(TypedDict):
    audio: np.ndarray
    sampling_rate: int


class VoiceOutput(TypedDict):
    id: str
    embedding: List[float]

class GenerateOptions(TypedDict):
    chunk_time: Optional[float]
    duration: Optional[int]
    lookahead: Optional[int]
    model_id: Optional[str]
    voice: Optional[str]


class CartesiaTTS:
    """The client for Cartesia's text-to-speech library."""

    def __init__(self, *, api_key: str = None):
        """
        Args:
            api_key: The API key to use for authorization.
                The api key is not currently enforced.
                TODO: Set the API key.
        """
        self.base_url = os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self.api_version = os.environ.get("CARTESIA_API_VERSION", DEFAULT_API_VERSION)
        self.headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

        # Mapping from id -> embedding
        self._voices: Dict[str, List[float]] = {}
        self._downloaded_voices = False

    def models(self) -> List[str]:
        """Get a list of available models."""
        raise NotImplementedError()

    def voices(self, *, refresh: bool = False) -> List[str]:
        """Returns a list of voices for a given model.

        These voices can be used with :method:`CartesiaTTS.generate` to generate audio.

        Args:
            refresh: If ``True``, the API will be pinged if the voices for the model
                are not already cached. Otherwise, default to the cached voices.

        Returns:
            List[str]: The list of voice ids for the model.
        """
        if self._downloaded_voices and not refresh:
            return self._voices

        response = requests.get(f"{self._http_url()}/voices", headers=self.headers)

        if response.status_code != 200:
            raise ValueError(f"Failed to get voices. Error: {response.text}")

        # Map from the table rows to a dict with key: "id" and value: "embedding"
        # TODO: Remove the eval once the API returns a list of floats instead of a string
        downloaded_voices = {voice["id"]: eval(voice["embedding"]) for voice in response.json()}
        self._voices.update(downloaded_voices)
        self._downloaded_voices = True

        return self._voices

    def clone_voice(self, *, filepath: str = None, link: str = None) -> VoiceOutput:
        """Clone a voice from a filepath or YouTube url.

        Args:
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
            A dictionary containing:
                * "id": The id of the cloned voice.
                * "embedding": The embedding of the cloned voice.
        """
        if filepath and link:
            raise ValueError("Only one of `filepath` or `url` should be specified.")

        if filepath:
            url = f"{self._http_url()}/voices/clone/clip"
            files = {"clip": open(filepath, "rb")}
            headers = self.headers.copy()
            # The default content type of JSON is incorrect for file uploads
            headers.pop("Content-Type")
            response = requests.post(url, headers=headers, files=files)
        else:
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
        embedding = out["embedding"]
        voice_id = out["id"]
        self._voices[voice_id] = embedding

        return {"id": voice_id, "embedding": embedding}

    def _generate_request_body(
        self,
        transcript: str,
        options: Optional[GenerateOptions] = None,
    ) -> dict:
        """
        Create the request body for a stream request.
        """

        body = dict(
            transcript=transcript,
            model_id=(options and options.get("model_id")) or self.model_id,
        )

        # Clone options
        if options:
            if isinstance(options.get("voice"), str):
                voice = self._voices.get(options["voice"])
                body.update(voice)

            additional_options = {
                k: v for k, v in options.items() if k not in ["model_id", "voice"]
            }
            body.update(additional_options)

        return body

    async def async_generate(
        self,
        *,
        transcript: str,
        options: Optional[GenerateOptions] = None,
    ) -> AudioOutput:
        """Asynchronously generate audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            options: The options to use for generating audio.
                chunk_time: How long each audio segment should be in seconds.
                    This should not need to be adjusted.
                duration: The maximum duration of the audio in seconds.
                lookahead: The number of seconds to look ahead for each chunk.
                    This should not need to be adjusted.
                model_id: The model to use for generating audio. If not provided, the default model is used.
                voice: The voice to use for generating audio.

        Returns:
            A dictionary containing the following:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript, options)

        async with aiohttp.request(
            "POST", f"{self._http_url()}/stream", data=json.dumps(body), headers=self.headers
        ) as response:
            if response.status != 200:
                raise ValueError(f"Failed to generate audio. {response.text}")

            chunks = []
            sampling_rate = None
            async for chunk_bytes in response.content.iter_any():
                chunk_json = json.loads(chunk_bytes)
                data = base64.b64decode(chunk_json["data"])
                audio = np.frombuffer(data, dtype=np.float32)
                if sampling_rate is None:
                    sampling_rate = chunk_json.get("sampling_rate")
                chunks.append(audio)

            return {"audio": np.concatenate(chunks), "sampling_rate": sampling_rate}

    async def async_generate_stream(
        self,
        *,
        session: aiohttp.ClientSession,
        transcript: str,
        options: Optional[GenerateOptions] = None,
    ) -> AsyncGenerator[AudioOutput, None]:
        """Asynchronously generate an async generator of audio from a transcript.

        Note that this pattern relies on the consumer for session and resource management.
        If the generator is not fully consumed, the resource may not be released unless the consumer
        explicitly closes the generator. This is mitigated by having the consumer provide the session.

        Args:
            session: The aiohttp session to use for the request.
            transcript: The text to generate audio for.
            options: The options to use for generating audio.
                chunk_time: How long each audio segment should be in seconds.
                    This should not need to be adjusted.
                duration: The maximum duration of the audio in seconds.
                lookahead: The number of seconds to look ahead for each chunk.
                    This should not need to be adjusted.
                model_id: The model to use for generating audio. If not provided, the default model is used.
                voice: The voice to use for generating audio.

        Returns:
            An async generator containing dictionaries with the following:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript, options)
        response = await session.post(
            f"{self._http_url()}/stream", data=json.dumps(body), headers=self.headers
        )
        try:
            if response.status != 200:
                raise ValueError(f"Failed to generate audio. {response.text}")

            async def async_generator():
                try:
                    async for chunk_bytes in response.content.iter_any():
                        chunk_json = json.loads(chunk_bytes)
                        data = base64.b64decode(chunk_json["data"])
                        audio = np.frombuffer(data, dtype=np.float32)
                        yield {"audio": audio, "sampling_rate": chunk_json["sampling_rate"]}
                finally:
                    if not response.closed:
                        response.close()

            return async_generator()
        except Exception as e:
            if not response.closed:
                response.close()
            raise e

    def generate(
        self,
        *,
        transcript: str,
        options: Optional[GenerateOptions] = None,
    ) -> AudioOutput:
        """Generate audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            options: The options to use for generating audio.
                chunk_time: How long each audio segment should be in seconds.
                    This should not need to be adjusted.
                duration: The maximum duration of the audio in seconds.
                lookahead: The number of seconds to look ahead for each chunk.
                    This should not need to be adjusted.
                model_id: The model to use for generating audio. If not provided, the default model is used.
                voice: The voice to use for generating audio.
                    This can either be a voice id (string) or an embedding vector (List[float]).

        Returns:
            A dictionary containing:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript, options)

        response = requests.post(
            f"{self._http_url()}/stream", stream=True, data=json.dumps(body), headers=self.headers
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
        options: Optional[GenerateOptions] = None,
    ) -> Generator[AudioOutput, None, None]:
        """Generate a generator of audio from a transcript.

        Args:
            transcript: The text to generate audio for.
            options: The options to use for generating audio.
                chunk_time: How long each audio segment should be in seconds.
                    This should not need to be adjusted.
                duration: The maximum duration of the audio in seconds.
                lookahead: The number of seconds to look ahead for each chunk.
                    This should not need to be adjusted.
                model_id: The model to use for generating audio. If not provided, the default model is used.
                voice: The voice to use for generating audio.
                    This can either be a voice id (string) or an embedding vector (List[float]).

        Returns:
            A generator for dictionaries containing:
                * "audio": The audio as a 1D numpy array.
                * "sampling_rate": The sampling rate of the audio.
        """
        body = self._generate_request_body(transcript, options)

        response = requests.post(
            f"{self._http_url()}/stream", stream=True, data=json.dumps(body), headers=self.headers
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

    # Primarily used for testing
    def _pcm_to_wav(self, pcm_data, output_file, sample_rate=44100, sample_width=2, num_channels=1):
        # Convert float32 PCM data to int16
        pcm_data = (pcm_data * 32767).astype(np.int16)

        # Open a new WAV file for writing
        wav_file = wave.open(output_file, "wb")

        # Set the WAV file parameters
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)  # 2 bytes for int16
        wav_file.setframerate(sample_rate)

        # Write the PCM data to the WAV file
        wav_file.writeframes(pcm_data.tobytes())

        # Close the WAV file
        wav_file.close()
