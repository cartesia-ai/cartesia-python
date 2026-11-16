# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = [
    "Version",
    "Config",
    "ConfigAudio",
    "ConfigAudioInput",
    "ConfigAudioOutput",
    "ConfigAudioOutputBackgroundSound",
    "ConfigKnowledgeBaseDocument",
    "ConfigKnowledgeBaseFolder",
    "ConfigLanguage",
    "ConfigLanguagePresets",
    "ConfigModel",
    "ConfigModelFallbackStrategy",
    "ConfigModelFallbackStrategyType",
    "ConfigModelFallbackStrategyUnionMember1",
    "ConfigModelCustomLlm",
    "ConfigModelCustomLlmAuthentication",
    "ConfigModelCustomLlmAuthenticationUnionMember0",
    "ConfigModelCustomLlmAuthenticationUnionMember0Password",
    "ConfigModelCustomLlmAuthenticationUnionMember1",
    "ConfigModelCustomLlmAuthenticationUnionMember1Token",
    "ConfigModelCustomLlmRequestHeaders",
    "ConfigModelCustomLlmRequestHeadersUnionMember1",
    "ConfigSystemTools",
    "ConfigSystemToolsEndCall",
    "ConfigSystemToolsSendDtmf",
    "ConfigSystemToolsTransferToNumber",
    "ConfigSystemToolsTransferToNumberTransfer",
    "ConfigSystemToolsTransferToNumberTransferDestination",
    "ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0",
    "ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1",
    "ConfigSystemToolsSkipTurn",
    "ConfigSystemToolsVoicemailDetection",
    "ConfigTool",
    "ConfigTurn",
]


class ConfigAudioInput(BaseModel):
    keyterms: List[str]
    """Words or phrases that the speech recognizer should prioritize."""

    noise_suppression: Literal["off", "auto", "max"]
    """Noise suppression applied to incoming audio.

    Use `off` to disable it, `auto` for the default level, or `max` for stronger
    suppression.
    """


class ConfigAudioOutputBackgroundSound(BaseModel):
    """Background audio played during the conversation."""

    file_id: str
    """ID of the audio file to play in the background."""

    volume: float
    """Background audio volume, from `0` to `2`."""


class ConfigAudioOutput(BaseModel):
    background_sound: Optional[ConfigAudioOutputBackgroundSound] = None
    """Background audio played during the conversation."""

    emotion: Optional[str] = None
    """
    Text-to-speech emotion supported by the selected voice and model, such as
    `calm`, `happy`, or `sad`.
    """

    pronunciation_dictionary_id: Optional[str] = None
    """ID of the pronunciation dictionary used for agent speech."""

    speed: Optional[float] = None
    """Speech speed multiplier, from `0.6` to `1.5`.

    Set to `null` to use the default speed.
    """

    voice_id: str
    """ID of the voice used for agent speech."""

    volume: Optional[float] = None
    """Speech volume multiplier, from `0.5` to `2`.

    Set to `null` to use the default volume.
    """


class ConfigAudio(BaseModel):
    input: ConfigAudioInput

    output: ConfigAudioOutput


class ConfigKnowledgeBaseDocument(BaseModel):
    id: str
    """ID of a document from the Knowledge Base API."""


class ConfigKnowledgeBaseFolder(BaseModel):
    id: str
    """ID of a folder from the Knowledge Base API."""


class ConfigLanguagePresets(BaseModel):
    normalization: Optional[str] = None

    voice_id: Optional[str] = None


class ConfigLanguage(BaseModel):
    additional: List[str]
    """Other languages the caller can switch to, in order.

    Each is a language, such as fr, or a locale, such as es-MX. May repeat the
    primary.
    """

    presets: Dict[str, ConfigLanguagePresets]
    """
    Settings for each language, keyed by a language, such as es, or a locale, such
    as es-MX. A preset applies whenever the agent speaks exactly its tag, the
    primary included, so a preset for es doesn't apply to es-MX. presets.voice_id is
    the voice the agent speaks the language with, and presets.normalization the
    locale it uses to read the language's numbers, dates and currencies.
    presets.voice_id is absent when the language uses the agent's voice, and
    presets.normalization when it uses the language's own rules.
    """

    primary: str
    """Primary language or locale for the conversation, such as en-US. Defaults to en."""


class ConfigModelFallbackStrategyType(BaseModel):
    type: Literal["auto"]


class ConfigModelFallbackStrategyUnionMember1(BaseModel):
    ids: List[str]

    type: Literal["explicit"]


ConfigModelFallbackStrategy: TypeAlias = Union[
    ConfigModelFallbackStrategyType, ConfigModelFallbackStrategyUnionMember1, None
]


class ConfigModelCustomLlmAuthenticationUnionMember0Password(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


class ConfigModelCustomLlmAuthenticationUnionMember0(BaseModel):
    """Sends an `Authorization` header using HTTP Basic authentication."""

    mode: Literal["basic_auth"]

    password: ConfigModelCustomLlmAuthenticationUnionMember0Password
    """A stored credential. `secret_value` is not returned."""

    username: str
    """The username. It cannot contain a colon."""


class ConfigModelCustomLlmAuthenticationUnionMember1Token(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


class ConfigModelCustomLlmAuthenticationUnionMember1(BaseModel):
    """Sends an `Authorization` header using a bearer token."""

    token: ConfigModelCustomLlmAuthenticationUnionMember1Token
    """A stored credential. `secret_value` is not returned."""

    mode: Literal["bearer"]


ConfigModelCustomLlmAuthentication: TypeAlias = Union[
    ConfigModelCustomLlmAuthenticationUnionMember0, ConfigModelCustomLlmAuthenticationUnionMember1, None
]


class ConfigModelCustomLlmRequestHeadersUnionMember1(BaseModel):
    """A stored credential. `secret_value` is not returned."""

    type: Literal["secret"]

    secret_description: Optional[str] = None
    """A label for this credential.

    Do not include the secret itself because this field is stored as plain text.
    """


ConfigModelCustomLlmRequestHeaders: TypeAlias = Union[str, ConfigModelCustomLlmRequestHeadersUnionMember1]


class ConfigModelCustomLlm(BaseModel):
    """The customer-hosted completion endpoint.

    Present only when `id` is `custom_llm`.
    """

    llm_model_id: Optional[str] = FieldInfo(alias="model_id", default=None)
    """Optional model ID sent as `model` in requests to your endpoint.

    If unset, the `model` field is omitted.
    """

    send_call_context: bool
    """
    Whether each request includes the call's dynamic variables in
    `cartesia_extra_body.dynamic_variables`.
    """

    url: str
    """
    The HTTPS base URL of the Chat Completions compatible API, such as
    `https://api.example.com/v1`. Requests go to its `/chat/completions` path.
    """

    authentication: Optional[ConfigModelCustomLlmAuthentication] = None
    """The bearer token or Basic auth credential sent in the `Authorization` header.

    Omit it if the endpoint needs none. For an API key sent in a different header,
    such as `api-key`, add it to `request_headers` as a secret instead.
    """

    request_headers: Optional[Dict[str, ConfigModelCustomLlmRequestHeaders]] = None
    """Headers included in each request. Secret values are never returned."""


class ConfigModel(BaseModel):
    id: str
    """
    Model ID from `GET /v1/agents/models`, or `custom_llm` to use the endpoint in
    `custom_llm`.
    """

    fallback_strategy: Optional[ConfigModelFallbackStrategy] = None
    """
    Fallback strategy: type auto uses Cartesia-managed fallback models in priority
    order; the models and their order may change over time. Type explicit uses up to
    three model IDs in the supplied order. Set fallback_strategy itself to null to
    disable fallback. Fallback models use their own reasoning defaults. When
    omitted, an agent keeps its current strategy; a new agent starts with auto, and
    an agent created with or switched to custom_llm starts with none. Switching back
    to a managed model restores auto. Fallback models are billed like any managed
    model, including on an agent that uses custom_llm.
    """

    max_output_tokens: Optional[int] = None
    """Maximum number of tokens the model can generate, from `1` to `4096`.

    Set to `null` for no limit.
    """

    temperature: Optional[float] = None
    """Controls the randomness of model responses, from `0` to `1`."""

    custom_llm: Optional[ConfigModelCustomLlm] = None
    """The customer-hosted completion endpoint.

    Present only when `id` is `custom_llm`.
    """


class ConfigSystemToolsEndCall(BaseModel):
    """Configuration for ending the call. Set to `null` to disable this tool."""

    description: Optional[str] = None
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemToolsSendDtmf(BaseModel):
    """Configuration for sending DTMF tones. Set to `null` to disable this tool."""

    description: Optional[str] = None
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0(BaseModel):
    phone_number: str
    """An E.164 phone number or a variable such as `{{transfer_number}}`.

    The variable must contain a valid E.164 number when the transfer runs.
    """

    type: Literal["phone"]


class ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1(BaseModel):
    sip_uri: str
    """
    A SIP URI beginning with lowercase `sip:` or `sips:`, or a single dynamic
    variable such as `{{sip_uri}}`. The variable must contain a valid SIP URI when
    the transfer runs.
    """

    type: Literal["sip_uri"]


ConfigSystemToolsTransferToNumberTransferDestination: TypeAlias = Union[
    ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0,
    ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1,
]


class ConfigSystemToolsTransferToNumberTransfer(BaseModel):
    condition: str
    """When the agent should transfer the call to this destination."""

    destination: ConfigSystemToolsTransferToNumberTransferDestination
    """Where to transfer the call."""


class ConfigSystemToolsTransferToNumber(BaseModel):
    """Configuration for transferring the call. Set to `null` to disable this tool."""

    description: Optional[str] = None
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    transfers: List[ConfigSystemToolsTransferToNumberTransfer]
    """Destinations the agent can transfer calls to."""


class ConfigSystemToolsSkipTurn(BaseModel):
    """
    Skip the agent's turn when the user asks for time to think or perform an action, such as "Give me a second" or "Let me check". Existing check-in timing stays unchanged unless `wait_timeout_secs` is configured. A configured timeout temporarily changes the check-in timer; user speech or DTMF restores the original timeout. Set this tool to `null` to disable it.
    """

    description: Optional[str] = None
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    wait_timeout_secs: Optional[int] = None
    """Temporary check-in timeout in seconds after skipping a turn.

    Set a longer timeout to give the caller more time, `-1` to disable check-ins, or
    `null` to keep normal timing. User speech or DTMF restores the original timeout.
    Requires check-ins to be enabled. The inactivity end-call timer keeps running.
    """


class ConfigSystemToolsVoicemailDetection(BaseModel):
    """Configuration for detecting voicemail, speaking a message, and ending the call.

    Set to `null` to disable this tool.
    """

    description: Optional[str] = None
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    message: Optional[str] = None
    """Message spoken after voicemail is detected.

    Set to `null` for no configured message.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemTools(BaseModel):
    """Built-in tools available to the agent."""

    end_call: Optional[ConfigSystemToolsEndCall] = None
    """Configuration for ending the call. Set to `null` to disable this tool."""

    send_dtmf: Optional[ConfigSystemToolsSendDtmf] = None
    """Configuration for sending DTMF tones. Set to `null` to disable this tool."""

    transfer_to_number: Optional[ConfigSystemToolsTransferToNumber] = None
    """Configuration for transferring the call. Set to `null` to disable this tool."""

    skip_turn: Optional[ConfigSystemToolsSkipTurn] = None
    """
    Skip the agent's turn when the user asks for time to think or perform an action,
    such as "Give me a second" or "Let me check". Existing check-in timing stays
    unchanged unless `wait_timeout_secs` is configured. A configured timeout
    temporarily changes the check-in timer; user speech or DTMF restores the
    original timeout. Set this tool to `null` to disable it.
    """

    voicemail_detection: Optional[ConfigSystemToolsVoicemailDetection] = None
    """Configuration for detecting voicemail, speaking a message, and ending the call.

    Set to `null` to disable this tool.
    """


class ConfigTool(BaseModel):
    id: str
    """ID of a tool from the Tools API."""


class ConfigTurn(BaseModel):
    inactivity_check_in_secs: Optional[int] = None
    """Seconds of inactivity before the agent checks in, from `5` to `60`.

    Defaults to `8`. Set to `null` to disable check-ins. When enabled, it must be
    less than `inactivity_end_call_secs`.
    """

    inactivity_end_call_secs: int
    """
    Seconds of inactivity before the agent says a farewell message and ends the
    call, from `20` to `240`. Defaults to `240`; cannot be `null`.
    """


class Config(BaseModel):
    """Complete agent configuration."""

    audio: ConfigAudio

    dynamic_variable_placeholders: Dict[str, Union[str, float, bool]]
    """Sample values for test calls, keyed by custom variable name.

    These are not used in production. PATCH replaces the whole map; omit it to keep
    existing samples or use `{}` to clear them.
    """

    event_webhook_id: Optional[str] = None
    """ID of the event webhook that receives events from this agent."""

    initial_message: Optional[str] = None
    """Message the agent says first.

    Set to `null` to wait for the user to speak. All `{{name}}` references must have
    values before the call starts.
    """

    initial_message_interruptions: Literal["allow", "ignore", "respond_after"]
    """Controls how the agent handles interruptions while `initial_message` plays.

    `allow` lets the caller interrupt it, `ignore` plays it in full without
    replying, and `respond_after` plays it in full, then replies. Defaults to
    `allow`.
    """

    instructions: str
    """Instructions that define the agent's behavior.

    Supports `{{name}}` references; missing values leave the reference unchanged.
    """

    knowledge_base_documents: List[ConfigKnowledgeBaseDocument]
    """Knowledge base documents attached to the agent."""

    knowledge_base_folders: List[ConfigKnowledgeBaseFolder]
    """Knowledge base folders attached to the agent."""

    language: ConfigLanguage

    model: ConfigModel

    prompt_optimization: bool
    """When enabled, the prompt is optimized with Cartesia's voice guidelines."""

    speculative_generation: bool
    """
    When enabled, starts generating an LLM response eagerly to reduce perceived
    latency, before confirming that the user’s turn has ended. May increase LLM
    costs.
    """

    system_tools: ConfigSystemTools
    """Built-in tools available to the agent."""

    timezone: str
    """Time zone for `{{system__time}}`, such as `America/New_York`.

    Defaults to `UTC`.
    """

    tools: List[ConfigTool]
    """Tools available to the agent."""

    turn: ConfigTurn


class Version(BaseModel):
    """An immutable snapshot of an agent's configuration."""

    id: str
    """Unique identifier for an immutable agent configuration version."""

    config: Config
    """Complete agent configuration."""

    created_at: datetime
    """Time when this version was created."""

    created_by: Optional[str] = None
    """ID of the user or API key that created this version.

    `null` when no creator was recorded.
    """

    description: Optional[str] = None
    """Description supplied when this version was created.

    `null` if none was provided.
    """
