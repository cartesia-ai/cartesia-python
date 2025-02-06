from typing import Iterator, List, Optional, Tuple

import httpx
from cartesia._async_sse import _AsyncSSE
from cartesia._async_websocket import _AsyncWebSocket
from cartesia._types import OutputFormat, VoiceControls
from cartesia.tts import TTS
from cartesia.utils.tts import _construct_tts_request


class AsyncTTS(TTS):
    def __init__(self, api_key, base_url, timeout, get_session):
        super().__init__(api_key, base_url, timeout)
        self._get_session = get_session
        self._sse_class = _AsyncSSE(self._http_url(), self.headers, self.timeout, get_session)
        self.sse = self._sse_class.send

    async def websocket(self) -> _AsyncWebSocket:
        ws = _AsyncWebSocket(
            self._ws_url(),
            self.api_key,
            self.cartesia_version,
            self.timeout,
            self._get_session,
        )
        await ws.connect()
        return ws

    async def bytes(
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._http_url()}/tts/bytes",
                headers=self.headers,
                timeout=self.timeout,
                json=request_body,
            )

        if not response.is_success:
            raise ValueError(f"Failed to generate audio. Error: {response.text}")

        return response.content

    async def infill(
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

            async with httpx.AsyncClient() as client:
                response = await client.post(
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
