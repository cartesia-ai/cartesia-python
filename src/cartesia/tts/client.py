# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .requests.tts_request_voice_specifier import TtsRequestVoiceSpecifierParams
from .requests.output_format import OutputFormatParams
from .types.supported_language import SupportedLanguage
from .types.model_speed import ModelSpeed
from ..core.request_options import RequestOptions
from ..core.serialization import convert_and_respect_annotation_metadata
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from .types.web_socket_response import WebSocketResponse
import httpx_sse
from ..core.pydantic_utilities import parse_obj_as
import json
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TtsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def bytes(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        language: typing.Optional[SupportedLanguage] = OMIT,
        duration: typing.Optional[float] = OMIT,
        speed: typing.Optional[ModelSpeed] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Parameters
        ----------
        model_id : str
            The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.

        transcript : str

        voice : TtsRequestVoiceSpecifierParams

        output_format : OutputFormatParams

        language : typing.Optional[SupportedLanguage]

        duration : typing.Optional[float]
            The maximum duration of the audio in seconds. You do not usually need to specify this.
            If the duration is not appropriate for the length of the transcript, the output audio may be truncated.

        speed : typing.Optional[ModelSpeed]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.Iterator[bytes]

        Examples
        --------
        from cartesia import Cartesia

        client = Cartesia(
            api_key="YOUR_API_KEY",
        )
        client.tts.bytes(
            model_id="sonic-2",
            transcript="Hello, world!",
            voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
            language="en",
            output_format={
                "sample_rate": 44100,
                "bit_rate": 128000,
                "container": "mp3",
            },
        )
        """
        with self._client_wrapper.httpx_client.stream(
            "tts/bytes",
            method="POST",
            json={
                "model_id": model_id,
                "transcript": transcript,
                "voice": convert_and_respect_annotation_metadata(
                    object_=voice, annotation=TtsRequestVoiceSpecifierParams, direction="write"
                ),
                "language": language,
                "output_format": convert_and_respect_annotation_metadata(
                    object_=output_format, annotation=OutputFormatParams, direction="write"
                ),
                "duration": duration,
                "speed": speed,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", None) if request_options is not None else None
                    for _chunk in _response.iter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                _response.read()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def sse(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        language: typing.Optional[SupportedLanguage] = OMIT,
        duration: typing.Optional[float] = OMIT,
        speed: typing.Optional[ModelSpeed] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[WebSocketResponse]:
        """
        Parameters
        ----------
        model_id : str
            The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.

        transcript : str

        voice : TtsRequestVoiceSpecifierParams

        output_format : OutputFormatParams

        language : typing.Optional[SupportedLanguage]

        duration : typing.Optional[float]
            The maximum duration of the audio in seconds. You do not usually need to specify this.
            If the duration is not appropriate for the length of the transcript, the output audio may be truncated.

        speed : typing.Optional[ModelSpeed]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[WebSocketResponse]

        Examples
        --------
        from cartesia import Cartesia

        client = Cartesia(
            api_key="YOUR_API_KEY",
        )
        response = client.tts.sse(
            model_id="sonic-2",
            transcript="Hello, world!",
            voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
            language="en",
            output_format={
                "sample_rate": 44100,
                "encoding": "pcm_f32le",
                "container": "raw",
            },
        )
        for chunk in response:
            yield chunk
        """
        with self._client_wrapper.httpx_client.stream(
            "tts/sse",
            method="POST",
            json={
                "model_id": model_id,
                "transcript": transcript,
                "voice": convert_and_respect_annotation_metadata(
                    object_=voice, annotation=TtsRequestVoiceSpecifierParams, direction="write"
                ),
                "language": language,
                "output_format": convert_and_respect_annotation_metadata(
                    object_=output_format, annotation=OutputFormatParams, direction="write"
                ),
                "duration": duration,
                "speed": speed,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _event_source = httpx_sse.EventSource(_response)
                    for _sse in _event_source.iter_sse():
                        try:
                            yield typing.cast(
                                WebSocketResponse,
                                parse_obj_as(
                                    type_=WebSocketResponse,  # type: ignore
                                    object_=json.loads(_sse.data),
                                ),
                            )
                        except:
                            pass
                    return
                _response.read()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncTtsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def bytes(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        language: typing.Optional[SupportedLanguage] = OMIT,
        duration: typing.Optional[float] = OMIT,
        speed: typing.Optional[ModelSpeed] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Parameters
        ----------
        model_id : str
            The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.

        transcript : str

        voice : TtsRequestVoiceSpecifierParams

        output_format : OutputFormatParams

        language : typing.Optional[SupportedLanguage]

        duration : typing.Optional[float]
            The maximum duration of the audio in seconds. You do not usually need to specify this.
            If the duration is not appropriate for the length of the transcript, the output audio may be truncated.

        speed : typing.Optional[ModelSpeed]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.

        Yields
        ------
        typing.AsyncIterator[bytes]

        Examples
        --------
        import asyncio

        from cartesia import AsyncCartesia

        client = AsyncCartesia(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.tts.bytes(
                model_id="sonic-2",
                transcript="Hello, world!",
                voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
                language="en",
                output_format={
                    "sample_rate": 44100,
                    "bit_rate": 128000,
                    "container": "mp3",
                },
            )


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            "tts/bytes",
            method="POST",
            json={
                "model_id": model_id,
                "transcript": transcript,
                "voice": convert_and_respect_annotation_metadata(
                    object_=voice, annotation=TtsRequestVoiceSpecifierParams, direction="write"
                ),
                "language": language,
                "output_format": convert_and_respect_annotation_metadata(
                    object_=output_format, annotation=OutputFormatParams, direction="write"
                ),
                "duration": duration,
                "speed": speed,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _chunk_size = request_options.get("chunk_size", None) if request_options is not None else None
                    async for _chunk in _response.aiter_bytes(chunk_size=_chunk_size):
                        yield _chunk
                    return
                await _response.aread()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def sse(
        self,
        *,
        model_id: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        language: typing.Optional[SupportedLanguage] = OMIT,
        duration: typing.Optional[float] = OMIT,
        speed: typing.Optional[ModelSpeed] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[WebSocketResponse]:
        """
        Parameters
        ----------
        model_id : str
            The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.

        transcript : str

        voice : TtsRequestVoiceSpecifierParams

        output_format : OutputFormatParams

        language : typing.Optional[SupportedLanguage]

        duration : typing.Optional[float]
            The maximum duration of the audio in seconds. You do not usually need to specify this.
            If the duration is not appropriate for the length of the transcript, the output audio may be truncated.

        speed : typing.Optional[ModelSpeed]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[WebSocketResponse]

        Examples
        --------
        import asyncio

        from cartesia import AsyncCartesia

        client = AsyncCartesia(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            response = await client.tts.sse(
                model_id="sonic-2",
                transcript="Hello, world!",
                voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
                language="en",
                output_format={
                    "sample_rate": 44100,
                    "encoding": "pcm_f32le",
                    "container": "raw",
                },
            )
            async for chunk in response:
                yield chunk


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            "tts/sse",
            method="POST",
            json={
                "model_id": model_id,
                "transcript": transcript,
                "voice": convert_and_respect_annotation_metadata(
                    object_=voice, annotation=TtsRequestVoiceSpecifierParams, direction="write"
                ),
                "language": language,
                "output_format": convert_and_respect_annotation_metadata(
                    object_=output_format, annotation=OutputFormatParams, direction="write"
                ),
                "duration": duration,
                "speed": speed,
            },
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    _event_source = httpx_sse.EventSource(_response)
                    async for _sse in _event_source.aiter_sse():
                        try:
                            yield typing.cast(
                                WebSocketResponse,
                                parse_obj_as(
                                    type_=WebSocketResponse,  # type: ignore
                                    object_=json.loads(_sse.data),
                                ),
                            )
                        except:
                            pass
                    return
                await _response.aread()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)
