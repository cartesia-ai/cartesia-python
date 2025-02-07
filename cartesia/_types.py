from typing import List, Optional, TypedDict, Union

from cartesia.utils.deprecated import deprecated


class OutputFormatMapping:
    _format_mapping = {
        "raw_pcm_f32le_44100": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        "raw_pcm_s16le_44100": {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        "raw_pcm_f32le_24000": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 24000},
        "raw_pcm_s16le_24000": {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 24000},
        "raw_pcm_f32le_22050": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 22050},
        "raw_pcm_s16le_22050": {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 22050},
        "raw_pcm_f32le_16000": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 16000},
        "raw_pcm_s16le_16000": {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 16000},
        "raw_pcm_f32le_8000": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 8000},
        "raw_pcm_s16le_8000": {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 8000},
        "raw_pcm_mulaw_8000": {"container": "raw", "encoding": "pcm_mulaw", "sample_rate": 8000},
        "raw_pcm_alaw_8000": {"container": "raw", "encoding": "pcm_alaw", "sample_rate": 8000},
    }

    @classmethod
    def get_format(cls, format_name):
        if format_name in cls._format_mapping:
            return cls._format_mapping[format_name]
        else:
            raise ValueError(f"Unsupported format: {format_name}")


class VoiceMetadata(TypedDict):
    id: str
    name: str
    description: str
    embedding: List[float]
    is_public: bool
    user_id: str
    created_at: str
    language: str


class VoiceControls(TypedDict):
    """Defines different voice control parameters for voice synthesis.

    For a complete list of supported parameters, refer to the Cartesia API documentation.
    https://docs.cartesia.ai/reference/api-reference

    Examples:
        >>> {"speed": "fastest"}
        >>> {"speed": "slow", "emotion": ["sadness:high"]}
        >>> {"emotion": ["surprise:highest", "curiosity"]}

    Note:
        This is an experimental class and is subject to rapid change in future versions.
    """

    speed: Union[str, float] = ""
    emotion: List[str] = []


class OutputFormat(TypedDict):
    container: str
    encoding: str
    sample_rate: int
    bit_rate: Optional[int] = None


class EventType:
    NULL = ""
    AUDIO = "chunk"
    TIMESTAMPS = "timestamps"
