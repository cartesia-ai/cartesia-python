import asyncio
import typing
from types import TracebackType
from typing import Union

import aiohttp
import httpx

from .base_client import AsyncBaseCartesia, BaseCartesia
from .environment import CartesiaEnvironment
from .tts.socket_client import AsyncTtsClientWithWebsocket, TtsClientWithWebsocket


class Cartesia(BaseCartesia):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : CartesiaEnvironment
        The environment to use for requests from the client. from .environment import CartesiaEnvironment



        Defaults to CartesiaEnvironment.PRODUCTION



    api_key : str
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from cartesia import Cartesia

    client = Cartesia(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: CartesiaEnvironment = CartesiaEnvironment.PRODUCTION,
        api_key: str,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )
        self.tts = TtsClientWithWebsocket(client_wrapper=self._client_wrapper)

    def __enter__(self):
        return self

    def __exit__(
        self,
        exc_type: Union[type, None],
        exc: Union[BaseException, None],
        exc_tb: Union[TracebackType, None],
    ):
        pass

    def __del__(self):
        pass


class AsyncCartesia(AsyncBaseCartesia):
    """
    Use this class to access the different functions within the SDK. You can instantiate any number of clients with different configuration that will propagate to these functions.

    Parameters
    ----------
    base_url : typing.Optional[str]
        The base url to use for requests from the client.

    environment : CartesiaEnvironment
        The environment to use for requests from the client. from .environment import CartesiaEnvironment



        Defaults to CartesiaEnvironment.PRODUCTION



    api_key : str
    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests. By default the timeout is 60 seconds, unless a custom httpx client is used, in which case this default is not enforced.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not, this is irrelevant if a custom httpx client is passed in.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests, a preconfigured client is used by default, however this is useful should you want to pass in any custom httpx configuration.

    Examples
    --------
    from cartesia import AsyncCartesia

    client = AsyncCartesia(
        api_key="YOUR_API_KEY",
    )
    """

    def __init__(
        self,
        *,
        base_url: typing.Optional[str] = None,
        environment: CartesiaEnvironment = CartesiaEnvironment.PRODUCTION,
        api_key: str,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
        timeout: typing.Optional[float] = 30,
        max_num_connections: typing.Optional[int] = 10,
    ):
        super().__init__(
            base_url=base_url,
            environment=environment,
            api_key=api_key,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )
        self.timeout = timeout
        self._session = None
        self._loop = None
        self.max_num_connections = max_num_connections
        self.tts = AsyncTtsClientWithWebsocket(
            client_wrapper=self._client_wrapper, get_session=self._get_session
        )

    async def _get_session(self):
        """
        This method is used to get a session for the client.
        """
        current_loop = asyncio.get_event_loop()
        if self._loop is not current_loop:
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
