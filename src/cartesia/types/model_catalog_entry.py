# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .stt_mode import STTMode
from .model_capability import ModelCapability

__all__ = ["ModelCatalogEntry"]


class ModelCatalogEntry(BaseModel):
    id: str
    """Value clients send as TTS `model_id` or STT `model`."""

    capability: ModelCapability
    """Which speech API family the model belongs to."""

    modes: Optional[List[STTMode]] = None
    """STT transport paths. Omitted on TTS rows."""

    supported_languages: Optional[List[str]] = None
    """Language codes supported by this TTS model. Omitted on STT rows."""
