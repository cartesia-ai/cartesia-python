# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Union, Literal, TypeAlias

__all__ = ["STTBatchModel"]

_STTBatchModel = Literal["ink-whisper", "ink-whisper-2025-06-04"]

STTBatchModel: TypeAlias = Union[_STTBatchModel, str]
