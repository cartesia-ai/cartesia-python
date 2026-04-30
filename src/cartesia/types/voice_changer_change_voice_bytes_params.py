"""Aliases for backward compatibility."""

from __future__ import annotations

from .voice_changer_generate_params import VoiceChangerGenerateParams

__all__ = ["VoiceChangerChangeVoiceBytesParams"]

VoiceChangerChangeVoiceBytesParams = VoiceChangerGenerateParams  # Alias for backward compatibility
