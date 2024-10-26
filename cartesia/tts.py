from typing import Iterator, List, Optional

import httpx

from cartesia._sse import _SSE
from cartesia._types import (
    DeprecatedOutputFormatMapping,
    OutputFormat,
    OutputFormatMapping,
    VoiceControls,
)
from cartesia._websocket import _WebSocket
from cartesia.resource import Resource
from cartesia.utils.tts import _construct_tts_request, _validate_and_construct_voice


class TTS(Resource):
    """This resource contains methods to generate audio using Cartesia's text-to-speech API."""

    def __init__(self, api_key: str, base_url: str, timeout: float):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
        )
        self._sse_class = _SSE(self._http_url(), self.headers, self.timeout)
        self.sse = self._sse_class.send

    def websocket(self) -> _WebSocket:
        """This method returns a WebSocket object that can be used to generate audio using WebSocket.

        Returns:
            _WebSocket: A WebSocket object that can be used to generate audio using WebSocket.
        """
        ws = _WebSocket(self._ws_url(), self.api_key, self.cartesia_version)
        ws.connect()
        return ws

    def bytes(
        self,
        *,
        model_id: str,
        transcript: str,
        output_format: OutputFormat,
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        duration: Optional[int] = None,
        language: Optional[str] = None,
        _experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> bytes:
        request_body = _construct_tts_request(
            model_id=model_id,
            transcript=transcript,
            output_format=output_format,
            voice_id=voice_id,
            voice_embedding=voice_embedding,
            duration=duration,
            language=language,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        response = httpx.post(
            f"{self._http_url()}/tts/bytes",
            headers=self.headers,
            timeout=self.timeout,
            json=request_body,
        )

        if not response.is_success:
            raise ValueError(f"Failed to generate audio. Error: {response.text}")

        return response.content

    @staticmethod
    def get_output_format(output_format_name: str) -> OutputFormat:
        """Convenience method to get the output_format dictionary from a given output format name.

        Args:
            output_format_name (str): The name of the output format.

        Returns:
            OutputFormat: A dictionary containing the details of the output format to be passed into tts.sse() or tts.websocket().send()

        Raises:
            ValueError: If the output_format name is not supported
        """
        if output_format_name in OutputFormatMapping._format_mapping:
            output_format_obj = OutputFormatMapping.get_format(output_format_name)
        elif output_format_name in DeprecatedOutputFormatMapping._format_mapping:
            output_format_obj = DeprecatedOutputFormatMapping.get_format_deprecated(
                output_format_name
            )
        else:
            raise ValueError(f"Unsupported format: {output_format_name}")

        return OutputFormat(
            container=output_format_obj["container"],
            encoding=output_format_obj["encoding"],
            sample_rate=output_format_obj["sample_rate"],
        )

    @staticmethod
    def get_sample_rate(output_format_name: str) -> int:
        """Convenience method to get the sample rate for a given output format.

        Args:
            output_format_name (str): The name of the output format.

        Returns:
            int: The sample rate for the output format.

        Raises:
            ValueError: If the output_format name is not supported
        """
        if output_format_name in OutputFormatMapping._format_mapping:
            output_format_obj = OutputFormatMapping.get_format(output_format_name)
        elif output_format_name in DeprecatedOutputFormatMapping._format_mapping:
            output_format_obj = DeprecatedOutputFormatMapping.get_format_deprecated(
                output_format_name
            )
        else:
            raise ValueError(f"Unsupported format: {output_format_name}")

        return output_format_obj["sample_rate"]

    @staticmethod
    def _validate_and_construct_voice(
        voice_id: Optional[str] = None,
        voice_embedding: Optional[List[float]] = None,
        experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> dict:
        """Validate and construct the voice dictionary for the request.

        Args:
            voice_id: The ID of the voice to use for generating audio.
            voice_embedding: The embedding of the voice to use for generating audio.
            experimental_voice_controls: Voice controls for emotion and speed.
                Note: This is an experimental feature and may rapidly change in the future.

        Returns:
            A dictionary representing the voice configuration.

        Raises:
            ValueError: If neither or both voice_id and voice_embedding are specified.
        """
        return _validate_and_construct_voice(voice_id, voice_embedding, experimental_voice_controls)
