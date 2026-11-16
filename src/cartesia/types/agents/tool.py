# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from ..agent_summary import AgentSummary

__all__ = [
    "Tool",
    "UnionMember0",
    "UnionMember0APISchema",
    "UnionMember0APISchemaAuthentication",
    "UnionMember0APISchemaAuthenticationUnionMember0",
    "UnionMember0APISchemaAuthenticationUnionMember0Password",
    "UnionMember0APISchemaAuthenticationUnionMember1",
    "UnionMember0APISchemaAuthenticationUnionMember1Token",
    "UnionMember0APISchemaPathParamsSchema",
    "UnionMember0APISchemaQueryParamsSchema",
    "UnionMember0APISchemaQueryParamsSchemaProperties",
    "UnionMember0APISchemaQueryParamsSchemaPropertiesItems",
    "UnionMember0APISchemaRequestHeaders",
    "UnionMember0APISchemaRequestHeadersUnionMember1",
    "UnionMember0APISchemaRequestHeadersUnionMember2",
    "UnionMember0Assignment",
    "UnionMember0UnmanagedAgent",
    "UnionMember1",
    "UnionMember1Parameters",
    "UnionMember1ParametersProperties",
    "UnionMember1ParametersPropertiesItems",
    "UnionMember1UnmanagedAgent",
]


class UnionMember0APISchemaAuthenticationUnionMember0Password(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


class UnionMember0APISchemaAuthenticationUnionMember0(BaseModel):
    """Sends an `Authorization` header using HTTP Basic authentication."""

    mode: Literal["basic_auth"]

    password: UnionMember0APISchemaAuthenticationUnionMember0Password
    """A stored credential. `secret_value` is not returned."""

    username: str
    """The username. It cannot contain a colon."""


class UnionMember0APISchemaAuthenticationUnionMember1Token(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


class UnionMember0APISchemaAuthenticationUnionMember1(BaseModel):
    """Sends an `Authorization` header using a bearer token."""

    token: UnionMember0APISchemaAuthenticationUnionMember1Token
    """A stored credential. `secret_value` is not returned."""

    mode: Literal["bearer"]


UnionMember0APISchemaAuthentication: TypeAlias = Union[
    UnionMember0APISchemaAuthenticationUnionMember0, UnionMember0APISchemaAuthenticationUnionMember1
]


class UnionMember0APISchemaPathParamsSchema(BaseModel):
    """A value inserted into a URL path placeholder."""

    type: Literal["string", "integer", "number"]

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


class UnionMember0APISchemaQueryParamsSchemaPropertiesItems(BaseModel):
    """The array item type. Required when `type` is `array`."""

    type: Literal["string", "integer", "number", "boolean"]


class UnionMember0APISchemaQueryParamsSchemaProperties(BaseModel):
    """A value sent in the query string."""

    type: Literal["string", "integer", "number", "boolean", "array"]

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

    items: Optional[UnionMember0APISchemaQueryParamsSchemaPropertiesItems] = None
    """The array item type. Required when `type` is `array`."""


class UnionMember0APISchemaQueryParamsSchema(BaseModel):
    """Parameters sent in the request query string."""

    properties: Dict[str, UnionMember0APISchemaQueryParamsSchemaProperties]
    """Query parameters keyed by name."""

    required: Optional[List[str]] = None
    """Names of parameters the model must provide.

    Other model parameters are optional.
    """


class UnionMember0APISchemaRequestHeadersUnionMember1(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


class UnionMember0APISchemaRequestHeadersUnionMember2(BaseModel):
    """Fill this header from the variable's current value when the tool runs."""

    name: str
    """Variable to use as the header value."""

    type: Literal["dynamic_variable"]


UnionMember0APISchemaRequestHeaders: TypeAlias = Union[
    str, UnionMember0APISchemaRequestHeadersUnionMember1, UnionMember0APISchemaRequestHeadersUnionMember2
]


class UnionMember0APISchema(BaseModel):
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
    """The HTTP method."""

    url: str
    """The HTTPS endpoint to call.

    Use `{name}` for path parameters defined in `path_params_schema`.
    """

    authentication: Optional[UnionMember0APISchemaAuthentication] = None
    """Authentication sent in the `Authorization` header."""

    path_params_schema: Optional[Dict[str, UnionMember0APISchemaPathParamsSchema]] = None
    """Path parameters keyed by placeholder name."""

    query_params_schema: Optional[UnionMember0APISchemaQueryParamsSchema] = None
    """Parameters sent in the request query string."""

    request_body_schema: Optional["WebhookBodyParam"] = None
    """A value sent in the JSON request body."""

    request_headers: Optional[Dict[str, UnionMember0APISchemaRequestHeaders]] = None
    """Headers sent with every request."""


class UnionMember0Assignment(BaseModel):
    """Extract a response value and assign it to a dynamic variable.

    Missing or null values leave the variable unchanged. Objects and arrays are stored as JSON strings.
    """

    dynamic_variable: str
    """Custom variable to update.

    Names starting with `system__` or `secret__` are reserved.
    """

    value_path: str
    """
    Path to a value in the JSON response, such as `order.status`, `items[0].sku`, or
    `[0].id`. For arrays, `.0` and `[0]` both select the first item. For objects,
    `.0` selects the key `0`. Spaces in keys are preserved.
    """


class UnionMember0UnmanagedAgent(BaseModel):
    """An agent using this tool."""

    id: str
    """The ID of the agent."""

    name: str
    """The name of the agent."""


class UnionMember0(BaseModel):
    id: str
    """Unique identifier for the tool."""

    api_schema: UnionMember0APISchema

    assignments: List[UnionMember0Assignment]
    """
    Configure how to extract values from successful JSON tool responses and assign
    them to dynamic variables for this call.
    """

    created_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
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

    type: Literal["webhook"]
    """Runs an HTTP request from Cartesia's servers."""

    updated_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
    """

    agents: Optional[List[AgentSummary]] = None
    """Managed agents that currently use this tool.

    Included when `expand[]=agents` is requested.
    """

    unmanaged_agents: Optional[List[UnionMember0UnmanagedAgent]] = None
    """Non-managed agents that currently use this tool.

    They block deletion and must be updated outside the managed-agent API. Included
    when `expand[]=agents` is requested.
    """


class UnionMember1ParametersPropertiesItems(BaseModel):
    """The array item type. Required when `type` is `array`."""

    type: Literal["string", "integer", "number", "boolean"]


class UnionMember1ParametersProperties(BaseModel):
    """One argument passed to your function."""

    type: Literal["string", "integer", "number", "boolean", "array"]
    """The parameter's JSON type."""

    description: Optional[str] = None
    """What value the agent should provide."""

    enum: Optional[List[str]] = None
    """Allowed string values."""

    items: Optional[UnionMember1ParametersPropertiesItems] = None
    """The array item type. Required when `type` is `array`."""


class UnionMember1Parameters(BaseModel):
    """Parameters the agent can pass to the client function."""

    type: Literal["object"]
    """The parameters schema type. Always `object`."""

    properties: Optional[Dict[str, UnionMember1ParametersProperties]] = None
    """Parameters keyed by name."""

    required: Optional[List[str]] = None
    """Names of parameters the agent must provide. Other parameters are optional."""


class UnionMember1UnmanagedAgent(BaseModel):
    """An agent using this tool."""

    id: str
    """The ID of the agent."""

    name: str
    """The name of the agent."""


class UnionMember1(BaseModel):
    id: str
    """Unique identifier for the tool."""

    created_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
    """

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

    parameters: UnionMember1Parameters
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

    type: Literal["client"]
    """Runs a function in the connected client application."""

    updated_at: datetime
    """An RFC 3339 / ISO 8601 date-time string with timezone (e.g.

    `2025-04-16T12:34:56.789Z`).
    """

    agents: Optional[List[AgentSummary]] = None
    """Managed agents that currently use this tool.

    Included when `expand[]=agents` is requested.
    """

    unmanaged_agents: Optional[List[UnionMember1UnmanagedAgent]] = None
    """Non-managed agents that currently use this tool.

    They block deletion and must be updated outside the managed-agent API. Included
    when `expand[]=agents` is requested.
    """


Tool: TypeAlias = Union[UnionMember0, UnionMember1]

from .webhook_body_param import WebhookBodyParam
