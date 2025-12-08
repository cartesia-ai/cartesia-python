# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["GenerationConfigParam", "Experimental"]


class Experimental(TypedDict, total=False):
    """These controls are **experimental** and subject to breaking changes."""

    accent_localization: Optional[int]
    """
    Toggle accent localization: 0 (disabled, default) or 1 (enabled). When enabled,
    the voice adapts to match the transcript language's accent while preserving
    vocal characteristics. When disabled, maintains the original voice accent. For
    more information, see
    [Localize Voices](/build-with-sonic/capabilities/localize-voices).
    """


class GenerationConfigParam(TypedDict, total=False):
    """Configure the various attributes of the generated speech.

    These controls are only available for `sonic-3-preview` and will have no effect on earlier models.
    """

    experimental: Optional[Experimental]
    """These controls are **experimental** and subject to breaking changes."""

    speed: Optional[float]
    """Adjust the speed of the generated speech between -1.0 (slower) and 1.0 (faster).

    0.0 is the default speed.
    """

    volume: Optional[float]
    """Adjust the volume of the generated speech between -1.0 (softer) and 1.0
    (louder).

    0.0 is the default volume.
    """
