# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .stt_auto_finalize_close_command_param import STTAutoFinalizeCloseCommandParam
from .stt_auto_finalize_config_command_param import STTAutoFinalizeConfigCommandParam

__all__ = ["STTAutoFinalizeWebsocketRequestParam"]

STTAutoFinalizeWebsocketRequestParam: TypeAlias = Union[
    STTAutoFinalizeCloseCommandParam, STTAutoFinalizeConfigCommandParam
]
