from cartesia._async_sse import _AsyncSSE
from cartesia._async_websocket import _AsyncWebSocket
from cartesia.tts import TTS


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
