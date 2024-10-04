import os
from types import TracebackType
from typing import Optional, Union

from cartesia._constants import DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from cartesia.tts import TTS
from cartesia.voices import Voices


class BaseClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Constructor for the BaseClient. Used by the Cartesia and AsyncCartesia clients."""
        self.api_key = api_key or os.environ.get("CARTESIA_API_KEY")
        self._base_url = base_url or os.environ.get("CARTESIA_BASE_URL", DEFAULT_BASE_URL)
        self.timeout = timeout

    @property
    def base_url(self):
        return self._base_url


class Cartesia(BaseClient):
    """
    The client for Cartesia's text-to-speech library.

    This client contains methods to interact with the Cartesia text-to-speech API.
    The client can be used to manage your voice library and generate speech from text.

    The client supports generating audio using both Server-Sent Events and WebSocket for lower latency.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """Constructor for the Cartesia client.

        Args:
            api_key: The API key to use for authorization.
                If not specified, the API key will be read from the environment variable
                `CARTESIA_API_KEY`.
            base_url: The base URL for the Cartesia API.
                If not specified, the base URL will be read from the enviroment variable
                `CARTESIA_BASE_URL`. Defaults to `api.cartesia.ai`.
            timeout: The timeout for HTTP and WebSocket requests in seconds. Defaults to 30 seconds.
        """
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.voices = Voices(api_key=self.api_key, base_url=self._base_url, timeout=self.timeout)
        self.tts = TTS(api_key=self.api_key, base_url=self._base_url, timeout=self.timeout)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        pass
