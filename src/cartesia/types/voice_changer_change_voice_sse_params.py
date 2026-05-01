"""Aliases for backward compatibility."""

from __future__ import annotations

from .voice_changer_generate_sse_params import VoiceChangerGenerateSSEParams

__all__ = ["VoiceChangerChangeVoiceSseParams"]

VoiceChangerChangeVoiceSseParams = VoiceChangerGenerateSSEParams  # Alias for backward compatibility
