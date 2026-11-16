# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr

__all__ = [
    "ToolUpdateParams",
    "Variant0",
    "Variant0APISchema",
    "Variant0APISchemaAuthentication",
    "Variant0APISchemaAuthenticationUnionMember0",
    "Variant0APISchemaAuthenticationUnionMember0Password",
    "Variant0APISchemaAuthenticationUnionMember1",
    "Variant0APISchemaAuthenticationUnionMember1Token",
    "Variant0APISchemaPathParamsSchema",
    "Variant0APISchemaQueryParamsSchema",
    "Variant0APISchemaQueryParamsSchemaProperties",
    "Variant0APISchemaQueryParamsSchemaPropertiesItems",
    "Variant0APISchemaRequestHeaders",
    "Variant0APISchemaRequestHeadersUnionMember1",
    "Variant0APISchemaRequestHeadersUnionMember2",
    "Variant0Assignment",
    "Variant1",
    "Variant1Parameters",
    "Variant1ParametersProperties",
    "Variant1ParametersPropertiesItems",
]


class Variant0(TypedDict, total=False):
    api_schema: Variant0APISchema

    assignments: Optional[Iterable[Variant0Assignment]]
    """Replace the response assignments.

    Omit to keep them, or use `null` or `[]` to clear them.
    """

    description: str
    """What the tool does and when the agent should use it."""

    execution_mode: Literal["immediate", "async"]
    """Controls how the tool runs relative to the conversation.

    `immediate` runs it in the current turn, while `async` lets the turn finish
    while the tool runs.
    """

    name: str
    """Name the agent uses to call the tool. Names are case-sensitive."""

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    response_timeout_secs: int
    """Maximum time to wait for the endpoint to respond. Defaults to 20 seconds."""


class Variant0APISchemaAuthenticationUnionMember0Password(TypedDict, total=False):
    """A secret credential. `secret_value` is write-only and is never returned."""

    type: Required[Literal["secret"]]

    secret_description: str
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """

    secret_value: str
    """The secret to store, such as an API key.

    This field is write-only. Omit it on update to keep the existing secret.
    """


class Variant0APISchemaAuthenticationUnionMember0(TypedDict, total=False):
    """Sends an `Authorization` header using HTTP Basic authentication."""

    mode: Required[Literal["basic_auth"]]

    password: Required[Variant0APISchemaAuthenticationUnionMember0Password]
    """A secret credential. `secret_value` is write-only and is never returned."""

    username: Required[str]
    """The username. It cannot contain a colon."""


class Variant0APISchemaAuthenticationUnionMember1Token(TypedDict, total=False):
    """A secret credential. `secret_value` is write-only and is never returned."""

    type: Required[Literal["secret"]]

    secret_description: str
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """

    secret_value: str
    """The secret to store, such as an API key.

    This field is write-only. Omit it on update to keep the existing secret.
    """


class Variant0APISchemaAuthenticationUnionMember1(TypedDict, total=False):
    """Sends an `Authorization` header using a bearer token."""

    token: Required[Variant0APISchemaAuthenticationUnionMember1Token]
    """A secret credential. `secret_value` is write-only and is never returned."""

    mode: Required[Literal["bearer"]]


Variant0APISchemaAuthentication: TypeAlias = Union[
    Variant0APISchemaAuthenticationUnionMember0, Variant0APISchemaAuthenticationUnionMember1
]


class Variant0APISchemaPathParamsSchema(TypedDict, total=False):
    """A value inserted into a URL path placeholder."""

    type: Required[Literal["string", "integer", "number"]]

    constant_value: Union[str, float, bool]
    """Fixed value to send with every request.

    It must match `type`. This parameter is hidden from the model.
    """

    description: str
    """What value the agent should provide."""

    dynamic_variable: str
    """Use this variable's current value when the tool runs.

    It must match `type`. This parameter is hidden from the model. A missing or
    invalid value prevents the request and returns a tool error.
    """

    enum: SequenceNotStr[Union[str, float, bool]]
    """Allowed values."""


class Variant0APISchemaQueryParamsSchemaPropertiesItems(TypedDict, total=False):
    """The array item type. Required when `type` is `array`."""

    type: Required[Literal["string", "integer", "number", "boolean"]]


class Variant0APISchemaQueryParamsSchemaProperties(TypedDict, total=False):
    """A value sent in the query string."""

    type: Required[Literal["string", "integer", "number", "boolean", "array"]]

    constant_value: Union[str, float, bool]
    """Fixed value to send with every request.

    It must match `type`. This parameter is hidden from the model.
    """

    description: str
    """What value the agent should provide."""

    dynamic_variable: str
    """Use this variable's current value when the tool runs.

    It must match `type`. This parameter is hidden from the model. A missing or
    invalid value prevents the request and returns a tool error.
    """

    enum: SequenceNotStr[Union[str, float, bool]]
    """Allowed values."""

    items: Variant0APISchemaQueryParamsSchemaPropertiesItems
    """The array item type. Required when `type` is `array`."""


class Variant0APISchemaQueryParamsSchema(TypedDict, total=False):
    """Parameters sent in the request query string."""

    properties: Required[Dict[str, Variant0APISchemaQueryParamsSchemaProperties]]
    """Query parameters keyed by name."""

    required: SequenceNotStr[str]
    """Names of parameters the model must provide.

    Other model parameters are optional.
    """


class Variant0APISchemaRequestHeadersUnionMember1(TypedDict, total=False):
    """A secret credential. `secret_value` is write-only and is never returned."""

    type: Required[Literal["secret"]]

    secret_description: str
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """

    secret_value: str
    """The secret to store, such as an API key.

    This field is write-only. Omit it on update to keep the existing secret.
    """


class Variant0APISchemaRequestHeadersUnionMember2(TypedDict, total=False):
    """Fill this header from the variable's current value when the tool runs."""

    name: Required[str]
    """Variable to use as the header value."""

    type: Required[Literal["dynamic_variable"]]


Variant0APISchemaRequestHeaders: TypeAlias = Union[
    str, Variant0APISchemaRequestHeadersUnionMember1, Variant0APISchemaRequestHeadersUnionMember2
]


class Variant0APISchema(TypedDict, total=False):
    authentication: Optional[Variant0APISchemaAuthentication]
    """Authentication sent in the `Authorization` header."""

    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    """The HTTP method."""

    path_params_schema: Optional[Dict[str, Variant0APISchemaPathParamsSchema]]
    """Path parameters keyed by placeholder name."""

    query_params_schema: Optional[Variant0APISchemaQueryParamsSchema]
    """Parameters sent in the request query string."""

    request_body_schema: object
    """The schema for the JSON request body.

    The root must be an `object`. Only `POST`, `PUT`, and `PATCH` requests can
    include a body.
    """

    request_headers: Optional[Dict[str, Optional[Variant0APISchemaRequestHeaders]]]

    url: str
    """The HTTPS endpoint to call.

    Use `{name}` for path parameters defined in `path_params_schema`.
    """


class Variant0Assignment(TypedDict, total=False):
    """Extract a response value and assign it to a dynamic variable.

    Missing or null values leave the variable unchanged. Objects and arrays are stored as JSON strings.
    """

    dynamic_variable: Required[str]
    """Custom variable to update.

    Names starting with `system__` or `secret__` are reserved.
    """

    value_path: Required[str]
    """
    Path to a value in the JSON response, such as `order.status`, `items[0].sku`, or
    `[0].id`. For arrays, `.0` and `[0]` both select the first item. For objects,
    `.0` selects the key `0`. Spaces in keys are preserved.
    """


class Variant1(TypedDict, total=False):
    description: str
    """What the tool does and when the agent should use it."""

    execution_mode: Literal["immediate", "async"]
    """Controls how the tool runs relative to the conversation.

    `immediate` runs it in the current turn, while `async` lets the turn finish
    while the tool runs.
    """

    expects_response: bool
    """Whether the client application must return a result.

    When `false`, the tool call is dispatched without waiting for a result.
    """

    name: str
    """Name the agent uses to call the tool. Names are case-sensitive."""

    parameters: Variant1Parameters
    """Parameters the agent can pass to the client function."""

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    response_timeout_secs: int
    """Maximum time to wait for the client application to return a result.

    Defaults to 20 seconds.
    """


class Variant1ParametersPropertiesItems(TypedDict, total=False):
    """The array item type. Required when `type` is `array`."""

    type: Required[Literal["string", "integer", "number", "boolean"]]


class Variant1ParametersProperties(TypedDict, total=False):
    """One argument passed to your function."""

    type: Required[Literal["string", "integer", "number", "boolean", "array"]]
    """The parameter's JSON type."""

    description: str
    """What value the agent should provide."""

    enum: SequenceNotStr[str]
    """Allowed string values."""

    items: Variant1ParametersPropertiesItems
    """The array item type. Required when `type` is `array`."""


class Variant1Parameters(TypedDict, total=False):
    """Parameters the agent can pass to the client function."""

    type: Required[Literal["object"]]
    """The parameters schema type. Always `object`."""

    properties: Dict[str, Variant1ParametersProperties]
    """Parameters keyed by name."""

    required: SequenceNotStr[str]
    """Names of parameters the agent must provide. Other parameters are optional."""


ToolUpdateParams: TypeAlias = Union[Variant0, Variant1]
