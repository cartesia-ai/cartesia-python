# This file was auto-generated by Fern from our API Definition.

import typing
from ..core.client_wrapper import SyncClientWrapper
from .. import core
from ..voice_changer.types.output_format_container import OutputFormatContainer
from ..tts.types.raw_encoding import RawEncoding
from ..tts.types.speed import Speed
from ..tts.types.emotion import Emotion
from ..core.request_options import RequestOptions
from json.decoder import JSONDecodeError
from ..core.api_error import ApiError
from ..core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class InfillClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def bytes(
        self,
        *,
        left_audio: core.File,
        right_audio: core.File,
        model_id: str,
        language: str,
        transcript: str,
        voice_id: str,
        output_format_container: OutputFormatContainer,
        output_format_sample_rate: int,
        output_format_encoding: typing.Optional[RawEncoding] = OMIT,
        output_format_bit_rate: typing.Optional[int] = OMIT,
        voice_experimental_controls_speed: typing.Optional[Speed] = OMIT,
        voice_experimental_controls_emotion: typing.Optional[typing.List[Emotion]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[bytes]:
        """
        Generate audio that smoothly connects two existing audio segments. This is useful for inserting new speech between existing speech segments while maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300 credits.**

        Only the `sonic-2` model is supported for infill at this time.

        At least one of `left_audio` or `right_audio` must be provided.

        As with all generative models, there's some inherent variability, but here's some tips we recommend to get the best results from infill:
        - Use longer infill transcripts
          - This gives the model more flexibility to adapt to the rest of the audio
        - Target natural pauses in the audio when deciding where to clip
          - This means you don't need word-level timestamps to be as precise
        - Clip right up to the start and end of the audio segment you want infilled, keeping as much silence in the left/right audio segments as possible
          - This helps the model generate more natural transitions

        Parameters
        ----------
        left_audio : core.File
            See core.File for more documentation

        right_audio : core.File
            See core.File for more documentation

        model_id : str
            The ID of the model to use for generating audio

        language : str
            The language of the transcript

        transcript : str
            The infill text to generate

        voice_id : str
            The ID of the voice to use for generating audio

        output_format_container : OutputFormatContainer
            The format of the output audio

        output_format_sample_rate : int
            The sample rate of the output audio

        output_format_encoding : typing.Optional[RawEncoding]
            Required for `raw` and `wav` containers.


        output_format_bit_rate : typing.Optional[int]
            Required for `mp3` containers.


        voice_experimental_controls_speed : typing.Optional[Speed]
            Either a number between -1.0 and 1.0 or a natural language description of speed.

            If you specify a number, 0.0 is the default speed, -1.0 is the slowest speed, and 1.0 is the fastest speed.


        voice_experimental_controls_emotion : typing.Optional[typing.List[Emotion]]
            An array of emotion:level tags.

            Supported emotions are: anger, positivity, surprise, sadness, and curiosity.

            Supported levels are: lowest, low, (omit), high, highest.


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
        client.infill.bytes(
            model_id="sonic-2",
            language="en",
            transcript="middle segment",
            voice_id="694f9389-aac1-45b6-b726-9d9369183238",
            output_format_container="mp3",
            output_format_sample_rate=44100,
            output_format_bit_rate=128000,
            voice_experimental_controls_speed="slowest",
            voice_experimental_controls_emotion=["surprise:high", "curiosity:high"],
        )
        """
        with self._client_wrapper.httpx_client.stream(
            "infill/bytes",
            method="POST",
            data={
                "model_id": model_id,
                "language": language,
                "transcript": transcript,
                "voice_id": voice_id,
                "output_format[container]": output_format_container,
                "output_format[sample_rate]": output_format_sample_rate,
                "output_format[encoding]": output_format_encoding,
                "output_format[bit_rate]": output_format_bit_rate,
                "voice[__experimental_controls][speed]": voice_experimental_controls_speed,
                "voice[__experimental_controls][emotion][]": voice_experimental_controls_emotion,
            },
            files={
                "left_audio": left_audio,
                "right_audio": right_audio,
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


class AsyncInfillClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def bytes(
        self,
        *,
        left_audio: core.File,
        right_audio: core.File,
        model_id: str,
        language: str,
        transcript: str,
        voice_id: str,
        output_format_container: OutputFormatContainer,
        output_format_sample_rate: int,
        output_format_encoding: typing.Optional[RawEncoding] = OMIT,
        output_format_bit_rate: typing.Optional[int] = OMIT,
        voice_experimental_controls_speed: typing.Optional[Speed] = OMIT,
        voice_experimental_controls_emotion: typing.Optional[typing.List[Emotion]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[bytes]:
        """
        Generate audio that smoothly connects two existing audio segments. This is useful for inserting new speech between existing speech segments while maintaining natural transitions.

        **The cost is 1 credit per character of the infill text plus a fixed cost of 300 credits.**

        Only the `sonic-2` model is supported for infill at this time.

        At least one of `left_audio` or `right_audio` must be provided.

        As with all generative models, there's some inherent variability, but here's some tips we recommend to get the best results from infill:
        - Use longer infill transcripts
          - This gives the model more flexibility to adapt to the rest of the audio
        - Target natural pauses in the audio when deciding where to clip
          - This means you don't need word-level timestamps to be as precise
        - Clip right up to the start and end of the audio segment you want infilled, keeping as much silence in the left/right audio segments as possible
          - This helps the model generate more natural transitions

        Parameters
        ----------
        left_audio : core.File
            See core.File for more documentation

        right_audio : core.File
            See core.File for more documentation

        model_id : str
            The ID of the model to use for generating audio

        language : str
            The language of the transcript

        transcript : str
            The infill text to generate

        voice_id : str
            The ID of the voice to use for generating audio

        output_format_container : OutputFormatContainer
            The format of the output audio

        output_format_sample_rate : int
            The sample rate of the output audio

        output_format_encoding : typing.Optional[RawEncoding]
            Required for `raw` and `wav` containers.


        output_format_bit_rate : typing.Optional[int]
            Required for `mp3` containers.


        voice_experimental_controls_speed : typing.Optional[Speed]
            Either a number between -1.0 and 1.0 or a natural language description of speed.

            If you specify a number, 0.0 is the default speed, -1.0 is the slowest speed, and 1.0 is the fastest speed.


        voice_experimental_controls_emotion : typing.Optional[typing.List[Emotion]]
            An array of emotion:level tags.

            Supported emotions are: anger, positivity, surprise, sadness, and curiosity.

            Supported levels are: lowest, low, (omit), high, highest.


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
            await client.infill.bytes(
                model_id="sonic-2",
                language="en",
                transcript="middle segment",
                voice_id="694f9389-aac1-45b6-b726-9d9369183238",
                output_format_container="mp3",
                output_format_sample_rate=44100,
                output_format_bit_rate=128000,
                voice_experimental_controls_speed="slowest",
                voice_experimental_controls_emotion=["surprise:high", "curiosity:high"],
            )


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            "infill/bytes",
            method="POST",
            data={
                "model_id": model_id,
                "language": language,
                "transcript": transcript,
                "voice_id": voice_id,
                "output_format[container]": output_format_container,
                "output_format[sample_rate]": output_format_sample_rate,
                "output_format[encoding]": output_format_encoding,
                "output_format[bit_rate]": output_format_bit_rate,
                "voice[__experimental_controls][speed]": voice_experimental_controls_speed,
                "voice[__experimental_controls][emotion][]": voice_experimental_controls_emotion,
            },
            files={
                "left_audio": left_audio,
                "right_audio": right_audio,
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
