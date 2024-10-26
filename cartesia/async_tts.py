from typing import Iterator, List, Optional

import httpx
from cartesia._async_sse import _AsyncSSE
from cartesia._async_websocket import _AsyncWebSocket
from cartesia._types import OutputFormat, VoiceControls
from cartesia.tts import TTS
from cartesia.utils.tts import _construct_tts_request


class AsyncTTS(TTS):
    def __init__(self, api_key, base_url, timeout, get_session):
        super().__init__(api_key, base_url, timeout)
        self._get_session = get_session
        self._sse_class = _AsyncSSE(self._http_url(), self.headers, self.timeout, get_session)
        self.sse = self._sse_class.send

    async def websocket(self) -> _AsyncWebSocket:
        ws = _AsyncWebSocket(
            self._ws_url(),
            self.api_key,
            self.cartesia_version,
            self.timeout,
            self._get_session,
        )
        await ws.connect()
        return ws

    async def bytes(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> bytes:
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._http_url()}/tts/bytes",
                headers=self.headers,
                timeout=self.timeout,
                json=request_body,
            )

        if not response.is_success:
            raise ValueError(f"Failed to generate audio. Error: {response.text}")

        return response.content
