# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["WatermarkDetectResponse"]


class WatermarkDetectResponse(BaseModel):
    detected: bool
    """Whether a Cartesia watermark was detected in the audio"""
