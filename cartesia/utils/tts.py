from typing import List, Optional

from cartesia._types import VoiceControls


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
