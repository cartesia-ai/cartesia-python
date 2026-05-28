# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Union, Literal, TypeAlias

__all__ = ["STTManualFinalizeModel"]

_STTManualFinalizeModel = Literal["ink-2", "ink-whisper", "ink-whisper-2025-06-04"]

STTManualFinalizeModel: TypeAlias = Union[_STTManualFinalizeModel, str]
