# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["WebhookBodyParam"]


class WebhookBodyParam(BaseModel):
    """A value sent in the JSON request body."""

    type: Literal["string", "integer", "number", "boolean", "object", "array"]

    constant_value: Union[str, float, bool, None] = None
    """Fixed value to send with every request.

    It must match `type`. This parameter is hidden from the model.
    """

    description: Optional[str] = None
    """What value the agent should provide."""

    dynamic_variable: Optional[str] = None
    """Use this variable's current value when the tool runs.

    It must match `type`. This parameter is hidden from the model. A missing or
    invalid value prevents the request and returns a tool error.
    """

    enum: Optional[List[Union[str, float, bool]]] = None
    """Allowed values."""

    items: Optional["WebhookBodyParam"] = None
    """A value sent in the JSON request body."""

    properties: Optional[Dict[str, "WebhookBodyParam"]] = None
    """Object properties keyed by name."""

    required: Optional[List[str]] = None
    """Names of properties the model must provide.

    Other model properties are optional.
    """
