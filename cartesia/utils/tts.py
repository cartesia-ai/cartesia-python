from typing import List, Optional

from cartesia._types import OutputFormat, VoiceControls


def _validate_and_construct_voice(
    voice_id: Optional[str] = None,
    voice_embedding: Optional[List[float]] = None,
    experimental_voice_controls: Optional[VoiceControls] = None,
) -> dict:
    if voice_id is None and voice_embedding is None:
        raise ValueError("Either voice_id or voice_embedding must be specified.")

    voice = {}

    if voice_id is not None:
        voice["id"] = voice_id

    if voice_embedding is not None:
        voice["embedding"] = voice_embedding

    if experimental_voice_controls is not None:
        voice["__experimental_controls"] = experimental_voice_controls

    return voice


def _construct_tts_request(
    *,
    model_id: str,
    output_format: OutputFormat,
    transcript: Optional[str] = None,
    voice_id: Optional[str] = None,
    voice_embedding: Optional[List[float]] = None,
    duration: Optional[int] = None,
    language: Optional[str] = None,
    add_timestamps: bool = False,
    context_id: Optional[str] = None,
    continue_: bool = False,
    _experimental_voice_controls: Optional[VoiceControls] = None,
):
    tts_request = {
        "model_id": model_id,
        "voice": _validate_and_construct_voice(
            voice_id,
            voice_embedding=voice_embedding,
            experimental_voice_controls=_experimental_voice_controls,
        ),
        "output_format": {
            "container": output_format["container"],
            "encoding": output_format["encoding"],
            "sample_rate": output_format["sample_rate"],
        },
    }

    if language is not None:
        tts_request["language"] = language

    if transcript is not None:
        tts_request["transcript"] = transcript

    if duration is not None:
        tts_request["duration"] = duration

    if add_timestamps:
        tts_request["add_timestamps"] = add_timestamps

    if context_id is not None:
        tts_request["context_id"] = context_id

    if continue_:
        tts_request["continue"] = continue_

    return tts_request
