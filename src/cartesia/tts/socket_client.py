import typing

from ._async_websocket import AsyncTtsWebsocket
from ._websocket import TtsWebsocket
from .client import AsyncTtsClient, TtsClient
from .types import OutputFormat
from .utils.tts import get_output_format


class TtsClientWithWebsocket(TtsClient):
    """
    Extension of TtsClient that supports a synchronous WebSocket TTS connection.
    """

    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    def get_output_format(self, output_format_name: str) -> OutputFormat:
        return get_output_format(output_format_name)

    def _ws_url(self):
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    def websocket(self):
        client_headers = self._client_wrapper.get_headers()
        ws = TtsWebsocket(
            ws_url=self._ws_url(),
            cartesia_version=client_headers["Cartesia-Version"],
            api_key=client_headers["X-API-Key"],
        )
        ws.connect()
        return ws


class AsyncTtsClientWithWebsocket(AsyncTtsClient):
    """
    Extension of AsyncTtsClient that supports an asynchronous WebSocket TTS connection.
    """

    def __init__(self, *, client_wrapper, get_session):
        super().__init__(client_wrapper=client_wrapper)
        self._get_session = get_session

    def get_output_format(self, output_format_name: str) -> OutputFormat:
        return get_output_format(output_format_name)

    def _ws_url(self) -> str:
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    async def websocket(self):
        client_headers = self._client_wrapper.get_headers()
        ws = AsyncTtsWebsocket(
            ws_url=self._ws_url(),
            cartesia_version=client_headers["Cartesia-Version"],
            api_key=client_headers["X-API-Key"],
            get_session=self._get_session,
        )
        await ws.connect()
        return ws
