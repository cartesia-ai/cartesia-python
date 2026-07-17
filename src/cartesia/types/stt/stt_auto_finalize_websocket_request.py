# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import TypeAlias

from .stt_auto_finalize_close_command import STTAutoFinalizeCloseCommand
from .stt_auto_finalize_config_command import STTAutoFinalizeConfigCommand

__all__ = ["STTAutoFinalizeWebsocketRequest"]

STTAutoFinalizeWebsocketRequest: TypeAlias = Union[STTAutoFinalizeCloseCommand, STTAutoFinalizeConfigCommand]
