# This file was auto-generated by Fern from our API Definition.

import typing
from .environment import CartesiaEnvironment
import httpx
from .core.client_wrapper import SyncClientWrapper
from .api_status.client import ApiStatusClient
from .infill.client import InfillClient
from .tts.client import TtsClient
from .voice_changer.client import VoiceChangerClient
from .voices.client import VoicesClient
from .core.client_wrapper import AsyncClientWrapper
from .api_status.client import AsyncApiStatusClient
from .infill.client import AsyncInfillClient
from .tts.client import AsyncTtsClient
from .voice_changer.client import AsyncVoiceChangerClient
from .voices.client import AsyncVoicesClient


class BaseCartesia:
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
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = SyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.Client(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.Client(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.api_status = ApiStatusClient(client_wrapper=self._client_wrapper)
        self.infill = InfillClient(client_wrapper=self._client_wrapper)
        self.tts = TtsClient(client_wrapper=self._client_wrapper)
        self.voice_changer = VoiceChangerClient(client_wrapper=self._client_wrapper)
        self.voices = VoicesClient(client_wrapper=self._client_wrapper)


class AsyncBaseCartesia:
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
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        _defaulted_timeout = timeout if timeout is not None else 60 if httpx_client is None else None
        self._client_wrapper = AsyncClientWrapper(
            base_url=_get_base_url(base_url=base_url, environment=environment),
            api_key=api_key,
            httpx_client=httpx_client
            if httpx_client is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout, follow_redirects=follow_redirects)
            if follow_redirects is not None
            else httpx.AsyncClient(timeout=_defaulted_timeout),
            timeout=_defaulted_timeout,
        )
        self.api_status = AsyncApiStatusClient(client_wrapper=self._client_wrapper)
        self.infill = AsyncInfillClient(client_wrapper=self._client_wrapper)
        self.tts = AsyncTtsClient(client_wrapper=self._client_wrapper)
        self.voice_changer = AsyncVoiceChangerClient(client_wrapper=self._client_wrapper)
        self.voices = AsyncVoicesClient(client_wrapper=self._client_wrapper)


def _get_base_url(*, base_url: typing.Optional[str] = None, environment: CartesiaEnvironment) -> str:
    if base_url is not None:
        return base_url
    elif environment is not None:
        return environment.value
    else:
        raise Exception("Please pass in either base_url or environment to construct the client")
