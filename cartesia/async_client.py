import asyncio
from types import TracebackType
from typing import Optional, Union

import aiohttp

from cartesia._constants import DEFAULT_NUM_CONNECTIONS, DEFAULT_TIMEOUT
from cartesia.async_tts import AsyncTTS
from cartesia.client import Cartesia


class AsyncCartesia(Cartesia):
    """The asynchronous version of the Cartesia client."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_num_connections: int = DEFAULT_NUM_CONNECTIONS,
    ):
        """
        Args:
            api_key: See :class:`Cartesia`.
            base_url: See :class:`Cartesia`.
            timeout: See :class:`Cartesia`.
            max_num_connections: The maximum number of concurrent connections to use for the client.
                This is used to limit the number of connections that can be made to the server.
        """
        self._session = None
        self._loop = None
        super().__init__(api_key=api_key, base_url=base_url, timeout=timeout)
        self.max_num_connections = max_num_connections
        self.tts = AsyncTTS(
            api_key=self.api_key,
            base_url=self._base_url,
            timeout=self.timeout,
            get_session=self._get_session,
        )

    async def _get_session(self):
        current_loop = asyncio.get_event_loop()
        if self._loop is not current_loop:
            # If the loop has changed, close the session and create a new one.
            await self.close()
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            connector = aiohttp.TCPConnector(limit=self.max_num_connections)
            self._session = aiohttp.ClientSession(timeout=timeout, connector=connector)
            self._loop = current_loop
        return self._session

    async def close(self):
        """This method closes the session.

        It is *strongly* recommended to call this method when you are done using the client.
        """
        if self._session is not None and not self._session.closed:
            await self._session.close()

    def __del__(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop is None:
            asyncio.run(self.close())
        elif loop.is_running():
            loop.create_task(self.close())

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        await self.close()
