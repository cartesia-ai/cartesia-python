import io
import typing
from json.decoder import JSONDecodeError

from pydub import AudioSegment  # type: ignore

from ..core.api_error import ApiError
from ._async_websocket import AsyncTtsWebsocket
from ._websocket import TtsWebsocket
from .client import AsyncTtsClient, TtsClient
from .requests import TtsRequestVoiceSpecifierParams
from .requests.output_format import OutputFormatParams
from .utils.tts import concat_audio_segments, get_output_format


class TtsClientWithWebsocket(TtsClient):
    """
    Extension of TtsClient that supports a synchronous WebSocket TTS connection.
    """

    def __init__(self, *, client_wrapper):
        super().__init__(client_wrapper=client_wrapper)

    def get_output_format(self, output_format_name: str) -> OutputFormatParams:
        return get_output_format(output_format_name)

    def _ws_url(self):
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    def infill(
        self,
        *,
        model_id: str,
        language: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        left_audio_path: typing.Optional[str] = None,
        right_audio_path: typing.Optional[str] = None,
    ) -> typing.Tuple[bytes, bytes]:
        """Generate infill audio between two existing audio segments.

        Args:
            model_id: The ID of the model to use for generating audio
            language: The language of the transcript
            transcript: The text to synthesize
            voice: The voice to use for generating audio
            output_format: The desired audio output format
            left_audio_path: Path to the audio file that comes before the infill
            right_audio_path: Path to the audio file that comes after the infill

        Returns:
            A tuple containing:
            - The generated infill audio (bytes)
            - The complete concatenated audio (bytes)
        """
        if not left_audio_path and not right_audio_path:
            raise ValueError(
                "Must specify at least one of left_audio_path or right_audio_path"
            )

        if voice["mode"] != "id":
            raise ValueError("Infill is only supported for id-based voice specifiers")

        if output_format["container"] == "raw":
            raise ValueError(
                "Raw format is not supported for infill. Use wav or mp3 format instead."
            )

        headers = self._client_wrapper.get_headers()
        headers.pop("Content-Type", None)

        left_audio_file = None
        right_audio_file = None
        try:
            files = {}
            if left_audio_path:
                left_audio_file = open(left_audio_path, "rb")
                files["left_audio"] = left_audio_file
            if right_audio_path:
                right_audio_file = open(right_audio_path, "rb")
                files["right_audio"] = right_audio_file

            # Construct form data with output_format fields directly
            data = {
                "model_id": model_id,
                "language": language,
                "transcript": transcript,
                "voice_id": voice["id"],
                "output_format[container]": output_format["container"],
                "output_format[sample_rate]": output_format["sample_rate"],
            }

            # Add bit_rate for mp3 container
            if "bit_rate" in output_format and output_format["bit_rate"] is not None:
                data["output_format[bit_rate]"] = output_format["bit_rate"]
            if (
                output_format["container"] != "mp3"
                and "encoding" in output_format
                and output_format["encoding"] is not None
            ):
                data["output_format[encoding]"] = output_format["encoding"]

            _response = self._client_wrapper.httpx_client.request(
                "infill/bytes",
                method="POST",
                files=files,  # type: ignore
                data=data,
                headers=headers,
            )
            try:
                if 200 <= _response.status_code < 300:
                    if left_audio_file:
                        left_audio_file.seek(0)
                        left_audio = left_audio_file.read()
                    else:
                        left_audio = None

                    if right_audio_file:
                        right_audio_file.seek(0)
                        right_audio = right_audio_file.read()
                    else:
                        right_audio = None

                    infill_audio = _response.content
                    format = output_format["container"].lower()
                    total_audio = concat_audio_segments(
                        left_audio, infill_audio, right_audio, format=format
                    )
                    return infill_audio, total_audio

                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

        finally:
            if left_audio_file:
                left_audio_file.close()
            if right_audio_file:
                right_audio_file.close()

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

    def get_output_format(self, output_format_name: str) -> OutputFormatParams:
        return get_output_format(output_format_name)

    def _ws_url(self) -> str:
        base_url = self._client_wrapper.get_base_url()
        if base_url.startswith("ws://") or base_url.startswith("wss://"):
            return base_url
        else:
            prefix = "ws" if "localhost" in base_url else "wss"
            base_url_without_protocol = base_url.split("://")[-1]
            return f"{prefix}://{base_url_without_protocol}"

    async def infill(
        self,
        *,
        model_id: str,
        language: str,
        transcript: str,
        voice: TtsRequestVoiceSpecifierParams,
        output_format: OutputFormatParams,
        left_audio_path: typing.Optional[str] = None,
        right_audio_path: typing.Optional[str] = None,
    ) -> typing.Tuple[bytes, bytes]:
        """Generate infill audio between two existing audio segments.
        Args:
            model_id: The ID of the model to use for generating audio
            language: The language of the transcript
            transcript: The text to synthesize
            voice_id: The ID of the voice to use for generating audio
            output_format: The desired audio output format
            left_audio_path: Path to the audio file that comes before the infill
            right_audio_path: Path to the audio file that comes after the infill
            experimental_voice_controls: Optional voice control parameters
        Returns:
            A tuple containing:
            - The generated infill audio (bytes)
            - The complete concatenated audio (bytes)
        """
        if not left_audio_path and not right_audio_path:
            raise ValueError(
                "Must specify at least one of left_audio_path or right_audio_path"
            )

        if voice["mode"] != "id":
            raise ValueError("Infill is only supported for id-based voice specifiers")

        if output_format["container"] == "raw":
            raise ValueError(
                "Raw format is not supported for infill. Use wav or mp3 format instead."
            )

        headers = self._client_wrapper.get_headers()
        headers.pop("Content-Type", None)

        left_audio_file = None
        right_audio_file = None
        try:
            files = {}
            if left_audio_path:
                left_audio_file = open(left_audio_path, "rb")
                files["left_audio"] = left_audio_file
            if right_audio_path:
                right_audio_file = open(right_audio_path, "rb")
                files["right_audio"] = right_audio_file

            data = {
                "model_id": model_id,
                "language": language,
                "transcript": transcript,
                "voice_id": voice["id"],
                "output_format[container]": output_format["container"],
                "output_format[sample_rate]": output_format["sample_rate"],
            }

            if "bit_rate" in output_format and output_format["bit_rate"] is not None:
                data["output_format[bit_rate]"] = output_format["bit_rate"]
            if (
                output_format["container"] != "mp3"
                and "encoding" in output_format
                and output_format["encoding"] is not None
            ):
                data["output_format[encoding]"] = output_format["encoding"]

            _response = await self._client_wrapper.httpx_client.request(
                "infill/bytes",
                method="POST",
                files=files,  # type: ignore
                headers=headers,
                data=data,
                request_options=None,
            )

            try:
                if 200 <= _response.status_code < 300:
                    if left_audio_file:
                        left_audio_file.seek(0)
                        left_audio = left_audio_file.read()
                    else:
                        left_audio = None

                    if right_audio_file:
                        right_audio_file.seek(0)
                        right_audio = right_audio_file.read()
                    else:
                        right_audio = None

                    infill_audio = _response.content
                    audio_format = output_format["container"].lower()
                    total_audio = concat_audio_segments(
                        left_audio, infill_audio, right_audio, format=audio_format
                    )
                    return infill_audio, total_audio

                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

        finally:
            if left_audio_file:
                left_audio_file.close()
            if right_audio_file:
                right_audio_file.close()

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
