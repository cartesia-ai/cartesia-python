import base64
import json
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

import requests

from cartesia._constants import BACKOFF_FACTOR, MAX_RETRIES
from cartesia._logger import logger
from cartesia._types import OutputFormat, VoiceControls
from cartesia.utils.retry import retry_on_connection_error
from cartesia.utils.tts import _construct_tts_request, _validate_and_construct_voice


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
        request_body = _construct_tts_request(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            duration=duration,
            language=language,
            _experimental_voice_controls=_experimental_voice_controls,
        )

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
