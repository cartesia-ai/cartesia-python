# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["Model", "Pricing"]


class Pricing(BaseModel):
    cache_read_per_million_tokens: str
    """Price in USD per one million tokens, represented as a decimal string."""

    cache_write_per_million_tokens: str
    """Price in USD per one million tokens, represented as a decimal string."""

    currency: Literal["USD"]

    input_per_million_tokens: str
    """Price in USD per one million tokens, represented as a decimal string."""

    output_per_million_tokens: str
    """Price in USD per one million tokens, represented as a decimal string."""


class Model(BaseModel):
    id: str
    """Model ID used in agent configuration."""

    average_latency_ms: Optional[int] = None
    """Average response latency in milliseconds."""

    description: Optional[str] = None
    """Description of the model."""

    display_name: str
    """Display name of the model."""

    fixed_temperature: Optional[float] = None
    """The model's fixed temperature, or null if temperature is adjustable."""

    pricing: Pricing

    provider: str
    """Company that provides the model."""
