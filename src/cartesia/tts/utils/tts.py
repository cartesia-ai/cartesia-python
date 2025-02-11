import io
import typing

from pydub import AudioSegment  # type: ignore

from .types import OutputFormatMapping


def get_output_format(output_format_name: str):
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

    return output_format_obj


def concat_audio_segments(
    left_audio: typing.Optional[bytes],
    infill_audio: bytes,
    right_audio: typing.Optional[bytes],
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
        combined = AudioSegment.empty()
        if left_audio:
            combined += AudioSegment.from_file(io.BytesIO(left_audio), format=format)

        combined += AudioSegment.from_file(io.BytesIO(infill_audio), format=format)

        if right_audio:
            combined += AudioSegment.from_file(io.BytesIO(right_audio), format=format)

        output = io.BytesIO()
        combined.export(output, format=format)
        return output.getvalue()

    except Exception as e:
        raise ValueError(f"Failed to concatenate audio segments: {str(e)}")
