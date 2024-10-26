import base64
import json
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional, Union

import aiohttp

from cartesia._constants import BACKOFF_FACTOR, MAX_RETRIES
from cartesia._logger import logger
from cartesia._sse import _SSE
from cartesia._types import OutputFormat, VoiceControls
from cartesia.utils.retry import retry_on_connection_error_async
from cartesia.utils.tts import _construct_tts_request


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
            f"{self.http_url}/tts/sse",
            data=json.dumps(request_body),
            headers=self.headers,
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
