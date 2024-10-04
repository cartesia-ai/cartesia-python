from cartesia._constants import DEFAULT_CARTESIA_VERSION


class Resource:
    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float,
    ):
        """Constructor for the Resource class. Used by the Voices and TTS classes."""
        self.api_key = api_key
        self.timeout = timeout
        self._base_url = base_url
        self.cartesia_version = DEFAULT_CARTESIA_VERSION
        self.headers = {
            "X-API-Key": self.api_key,
            "Cartesia-Version": self.cartesia_version,
            "Content-Type": "application/json",
        }

    @property
    def base_url(self):
        return self._base_url

    def _http_url(self):
        """Returns the HTTP URL for the Cartesia API.
        If the base URL is localhost, the URL will start with 'http'. Otherwise, it will start with 'https'.
        """
        if self._base_url.startswith("http://") or self._base_url.startswith("https://"):
            return self._base_url
        else:
            prefix = "http" if "localhost" in self._base_url else "https"
            return f"{prefix}://{self._base_url}"

    def _ws_url(self):
        """Returns the WebSocket URL for the Cartesia API.
        If the base URL is localhost, the URL will start with 'ws'. Otherwise, it will start with 'wss'.
        """
        if self._base_url.startswith("ws://") or self._base_url.startswith("wss://"):
            return self._base_url
        else:
            prefix = "ws" if "localhost" in self._base_url else "wss"
            return f"{prefix}://{self._base_url}"
