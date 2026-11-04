# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .model_catalog_entry import ModelCatalogEntry

__all__ = ["ListModelsResponse"]


class ListModelsResponse(BaseModel):
    data: List[ModelCatalogEntry]
    """Callable public model ids for TTS and STT."""
