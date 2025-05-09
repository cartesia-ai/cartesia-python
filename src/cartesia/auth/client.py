# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .requests.token_grant import TokenGrantParams
from ..core.request_options import RequestOptions
from .types.token_response import TokenResponse
from ..core.serialization import convert_and_respect_annotation_metadata
from ..core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AuthClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def access_token(
        self,
        *,
        grants: TokenGrantParams,
        expires_in: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TokenResponse:
        """
        Generates a new Access Token for the client. These tokens are short-lived and should be used to make requests to the API from authenticated clients.

        Parameters
        ----------
        grants : TokenGrantParams
            The permissions to be granted via the token.

        expires_in : typing.Optional[int]
            The number of seconds the token will be valid for since the time of generation. The maximum is 1 hour (3600 seconds).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TokenResponse

        Examples
        --------
        from cartesia import Cartesia

        client = Cartesia(
            api_key="YOUR_API_KEY",
        )
        client.auth.access_token(
            grants={"tts": True},
            expires_in=60,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "access-token",
            method="POST",
            json={
                "grants": convert_and_respect_annotation_metadata(
                    object_=grants, annotation=TokenGrantParams, direction="write"
                ),
                "expires_in": expires_in,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TokenResponse,
                    parse_obj_as(
                        type_=TokenResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncAuthClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def access_token(
        self,
        *,
        grants: TokenGrantParams,
        expires_in: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TokenResponse:
        """
        Generates a new Access Token for the client. These tokens are short-lived and should be used to make requests to the API from authenticated clients.

        Parameters
        ----------
        grants : TokenGrantParams
            The permissions to be granted via the token.

        expires_in : typing.Optional[int]
            The number of seconds the token will be valid for since the time of generation. The maximum is 1 hour (3600 seconds).

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TokenResponse

        Examples
        --------
        import asyncio

        from cartesia import AsyncCartesia

        client = AsyncCartesia(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.auth.access_token(
                grants={"tts": True},
                expires_in=60,
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            "access-token",
            method="POST",
            json={
                "grants": convert_and_respect_annotation_metadata(
                    object_=grants, annotation=TokenGrantParams, direction="write"
                ),
                "expires_in": expires_in,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TokenResponse,
                    parse_obj_as(
                        type_=TokenResponse,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
