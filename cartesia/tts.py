import json
from typing import Iterator, List, Optional, Tuple

import httpx
import io
from pydub import AudioSegment

from cartesia._sse import _SSE
from cartesia._types import (
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

    def infill(
        self,
        *,
        model_id: str,
        language: str,
        transcript: str,
        voice_id: str,
        output_format: OutputFormat,
        left_audio_path: Optional[str] = None,
        right_audio_path: Optional[str] = None,
        experimental_voice_controls: Optional[VoiceControls] = None,
    ) -> Tuple[bytes, bytes]:
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
            raise ValueError("Must specify at least one of left_audio_path or right_audio_path")

        headers = self.headers.copy()
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
                "voice_id": voice_id,
                "output_format[container]": output_format["container"],
                "output_format[encoding]": output_format["encoding"],
                "output_format[sample_rate]": output_format["sample_rate"],
            }

            # Add bit_rate for mp3 container
            if "bit_rate" in output_format:
                data["output_format[bit_rate]"] = output_format["bit_rate"]

            # Add voice controls if specified
            if experimental_voice_controls:
                if "speed" in experimental_voice_controls:
                    data["voice[__experimental_controls][speed]"] = experimental_voice_controls[
                        "speed"
                    ]
                if "emotion" in experimental_voice_controls:
                    # Pass emotions as a list instead of individual values
                    data["voice[__experimental_controls][emotion][]"] = experimental_voice_controls[
                        "emotion"
                    ]

            response = httpx.post(
                f"{self._http_url()}/infill/bytes",
                headers=headers,
                timeout=self.timeout,
                files=files,
                data=data,
            )

            if not response.is_success:
                raise ValueError(
                    f"Failed to infill audio. Status Code: {response.status_code}\n"
                    f"Error: {response.text}"
                )

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

            infill_audio = response.content
            format = output_format["container"].lower()
            total_audio = self._concat_audio_segments(
                left_audio, infill_audio, right_audio, format=format
            )
            return infill_audio, total_audio

        finally:
            if left_audio_file:
                left_audio_file.close()
            if right_audio_file:
                right_audio_file.close()

    @staticmethod
    def _concat_audio_segments(
        left_audio: Optional[bytes],
        infill_audio: bytes,
        right_audio: Optional[bytes],
        format: str = "wav",
    ) -> bytes:
        """Helper method to concatenate three audio segments while preserving audio format and headers.

        Args:
            left_audio: The audio segment that comes before the infill
            infill_audio: The generated infill audio segment
            right_audio: The audio segment that comes after the infill
            format: The audio format (e.g., 'wav', 'mp3'). Defaults to 'wav'

        Returns:
            bytes: The concatenated audio as bytes

        Raises:
            ValueError: If the audio segments cannot be loaded or concatenated
        """
        try:
            # Convert bytes to AudioSegment objects
            combined = AudioSegment.empty()
            if left_audio:
                combined += AudioSegment.from_file(io.BytesIO(left_audio), format=format)

            combined += AudioSegment.from_file(io.BytesIO(infill_audio), format=format)

            if right_audio:
                combined += AudioSegment.from_file(io.BytesIO(right_audio), format=format)

            # Export to bytes
            output = io.BytesIO()
            combined.export(output, format=format)
            return output.getvalue()

        except Exception as e:
            raise ValueError(f"Failed to concatenate audio segments: {str(e)}")
