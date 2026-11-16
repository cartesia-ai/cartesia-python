# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "AgentUpdateParams",
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
    "ConfigModelCustomLlm",
    "ConfigModelCustomLlmAuthentication",
    "ConfigModelCustomLlmAuthenticationUnionMember0",
    "ConfigModelCustomLlmAuthenticationUnionMember0Password",
    "ConfigModelCustomLlmAuthenticationUnionMember1",
    "ConfigModelCustomLlmAuthenticationUnionMember1Token",
    "ConfigModelCustomLlmRequestHeaders",
    "ConfigModelCustomLlmRequestHeadersUnionMember1",
    "ConfigModelFallbackStrategy",
    "ConfigModelFallbackStrategyType",
    "ConfigModelFallbackStrategyUnionMember1",
    "ConfigSystemTools",
    "ConfigSystemToolsEndCall",
    "ConfigSystemToolsSendDtmf",
    "ConfigSystemToolsSkipTurn",
    "ConfigSystemToolsTransferToNumber",
    "ConfigSystemToolsTransferToNumberTransfer",
    "ConfigSystemToolsTransferToNumberTransferDestination",
    "ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0",
    "ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1",
    "ConfigSystemToolsVoicemailDetection",
    "ConfigTool",
    "ConfigTurn",
]


class AgentUpdateParams(TypedDict, total=False):
    config: Config

    description: Optional[str]
    """Description of the agent."""

    name: str
    """Name shown for the agent. It does not need to be unique."""

    version_description: Optional[str]
    """Description to attach to the new configuration version.

    Allowed only when this request changes `config`.
    """


class ConfigAudioInput(TypedDict, total=False):
    asr_model: Literal["auto", "ink-2", "ink-preview", "original"]

    keyterms: SequenceNotStr[str]
    """Words or phrases that the speech recognizer should prioritize.

    At most 100 keyterms, totaling at most 1200 characters.
    """

    noise_suppression: Literal["off", "auto", "max"]
    """Noise suppression applied to incoming audio.

    Use `off` to disable it, `auto` for the default level, or `max` for stronger
    suppression.
    """


class ConfigAudioOutputBackgroundSound(TypedDict, total=False):
    """Background audio played during the conversation. Set to `null` to disable it."""

    file_id: str
    """ID of the audio file to play in the background."""

    volume: float
    """Background audio volume, from `0` to `2`."""


class ConfigAudioOutput(TypedDict, total=False):
    background_sound: Optional[ConfigAudioOutputBackgroundSound]
    """Background audio played during the conversation. Set to `null` to disable it."""

    emotion: Optional[str]
    """
    Text-to-speech emotion supported by the selected voice and model, such as
    `calm`, `happy`, or `sad`.
    """

    pronunciation_dictionary_id: Optional[str]
    """ID of the pronunciation dictionary used for agent speech."""

    speed: Optional[float]
    """Speech speed multiplier, from `0.6` to `1.5`.

    Set to `null` to use the default speed.
    """

    tts_model: Optional[str]

    voice_id: str
    """ID of the voice used for agent speech."""

    volume: Optional[float]
    """Speech volume multiplier, from `0.5` to `2`.

    Set to `null` to use the default volume.
    """


class ConfigAudio(TypedDict, total=False):
    input: ConfigAudioInput

    output: ConfigAudioOutput


class ConfigKnowledgeBaseDocument(TypedDict, total=False):
    id: Required[str]
    """ID of a document from the Knowledge Base API."""


class ConfigKnowledgeBaseFolder(TypedDict, total=False):
    id: Required[str]
    """ID of a folder from the Knowledge Base API."""


class ConfigLanguagePresets(TypedDict, total=False):
    normalization: str
    """
    Locale the agent uses to read this language's numbers, dates and currencies,
    such as en-IN. Omit to use the language's own rules.
    """

    voice_id: str
    """
    ID of the voice the agent speaks this language with, instead of
    audio.output.voice_id.
    """


class ConfigLanguage(TypedDict, total=False):
    additional: SequenceNotStr[str]
    """Other languages the caller can switch to, in order.

    Each is a language, such as fr, or a locale, such as es-MX. Omit to preserve the
    current list; [] clears it. Each base language may appear only once, except that
    the primary may repeat here.
    """

    presets: Dict[str, ConfigLanguagePresets]
    """
    Settings for each language, keyed by a language, such as es, or a locale, such
    as es-MX. A preset applies whenever the agent speaks exactly its tag, the
    primary included, so a preset for es doesn't apply to es-MX. Keys need not be
    the agent's languages. Omit to preserve the current presets; {} clears them. A
    map you send replaces the current one.
    """

    primary: Optional[str]
    """Primary language or locale, such as en-US.

    Null saves en. Supported values:
    https://docs.cartesia.ai/api-reference/agents/create#body-config-language-primary-one-of-0
    """


class ConfigModelCustomLlmAuthenticationUnionMember0Password(TypedDict, total=False):
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


class ConfigModelCustomLlmAuthenticationUnionMember0(TypedDict, total=False):
    """Sends an `Authorization` header using HTTP Basic authentication."""

    mode: Required[Literal["basic_auth"]]

    password: Required[ConfigModelCustomLlmAuthenticationUnionMember0Password]
    """A secret credential. `secret_value` is write-only and is never returned."""

    username: Required[str]
    """The username. It cannot contain a colon."""


class ConfigModelCustomLlmAuthenticationUnionMember1Token(TypedDict, total=False):
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


class ConfigModelCustomLlmAuthenticationUnionMember1(TypedDict, total=False):
    """Sends an `Authorization` header using a bearer token."""

    token: Required[ConfigModelCustomLlmAuthenticationUnionMember1Token]
    """A secret credential. `secret_value` is write-only and is never returned."""

    mode: Required[Literal["bearer"]]


ConfigModelCustomLlmAuthentication: TypeAlias = Union[
    ConfigModelCustomLlmAuthenticationUnionMember0, ConfigModelCustomLlmAuthenticationUnionMember1
]


class ConfigModelCustomLlmRequestHeadersUnionMember1(TypedDict, total=False):
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


ConfigModelCustomLlmRequestHeaders: TypeAlias = Union[str, ConfigModelCustomLlmRequestHeadersUnionMember1]


class ConfigModelCustomLlm(TypedDict, total=False):
    """
    The Chat Completions compatible endpoint the agent uses instead of a managed model. A create or PATCH that sends it replaces the whole object.
    """

    url: Required[str]
    """
    The HTTPS base URL of the Chat Completions compatible API, such as
    `https://api.example.com/v1`. Requests go to its `/chat/completions` path.
    """

    authentication: Optional[ConfigModelCustomLlmAuthentication]
    """The bearer token or Basic auth credential sent in the `Authorization` header.

    Omit it if the endpoint needs none. For an API key sent in a different header,
    such as `api-key`, add it to `request_headers` as a secret instead.
    """

    model_id: Optional[str]
    """Optional model ID sent as `model` in requests to your endpoint.

    If unset, the `model` field is omitted.
    """

    request_headers: Dict[str, ConfigModelCustomLlmRequestHeaders]
    """Headers included in each request. Secret values are never returned."""

    send_call_context: bool
    """
    Whether each request includes the call's dynamic variables in
    `cartesia_extra_body.dynamic_variables`. Defaults to `false`.
    """


class ConfigModelFallbackStrategyType(TypedDict, total=False):
    type: Required[Literal["auto"]]


class ConfigModelFallbackStrategyUnionMember1(TypedDict, total=False):
    ids: Required[SequenceNotStr[str]]

    type: Required[Literal["explicit"]]


ConfigModelFallbackStrategy: TypeAlias = Union[ConfigModelFallbackStrategyType, ConfigModelFallbackStrategyUnionMember1]


class ConfigModel(TypedDict, total=False):
    id: str
    """
    Model ID from `GET /v1/agents/models`, or `custom_llm` to use the endpoint in
    `custom_llm`.
    """

    custom_llm: ConfigModelCustomLlm
    """
    The Chat Completions compatible endpoint the agent uses instead of a managed
    model. A create or PATCH that sends it replaces the whole object.
    """

    fallback_strategy: Optional[ConfigModelFallbackStrategy]
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

    max_output_tokens: Optional[int]
    """Maximum number of tokens the model can generate, from `1` to `4096`.

    Set to `null` for no limit.
    """

    temperature: Optional[float]
    """Controls the randomness of model responses, from `0` to `1`."""


class ConfigSystemToolsEndCall(TypedDict, total=False):
    """Configuration for ending the call.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    description: Optional[str]
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemToolsSendDtmf(TypedDict, total=False):
    """Configuration for sending DTMF tones.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    description: Optional[str]
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemToolsSkipTurn(TypedDict, total=False):
    """
    Skip the agent's turn when the user asks for time to think or perform an action, such as "Give me a second" or "Let me check". Existing check-in timing stays unchanged unless `wait_timeout_secs` is configured. A configured timeout temporarily changes the check-in timer; user speech or DTMF restores the original timeout. Set this tool to `null` to disable it.
    """

    description: Optional[str]
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    wait_timeout_secs: Optional[int]
    """Temporary check-in timeout in seconds after skipping a turn.

    Set a longer timeout to give the caller more time, `-1` to disable check-ins, or
    `null` to keep normal timing. User speech or DTMF restores the original timeout.
    Requires check-ins to be enabled. The inactivity end-call timer keeps running.
    Omit to keep the current setting.
    """


class ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0(TypedDict, total=False):
    phone_number: Required[str]
    """An E.164 phone number or a variable such as `{{transfer_number}}`.

    The variable must contain a valid E.164 number when the transfer runs.
    """

    type: Required[Literal["phone"]]


class ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1(TypedDict, total=False):
    sip_uri: Required[str]
    """
    A SIP URI beginning with lowercase `sip:` or `sips:`, or a single dynamic
    variable such as `{{sip_uri}}`. The variable must contain a valid SIP URI when
    the transfer runs.
    """

    type: Required[Literal["sip_uri"]]


ConfigSystemToolsTransferToNumberTransferDestination: TypeAlias = Union[
    ConfigSystemToolsTransferToNumberTransferDestinationUnionMember0,
    ConfigSystemToolsTransferToNumberTransferDestinationUnionMember1,
]


class ConfigSystemToolsTransferToNumberTransfer(TypedDict, total=False):
    condition: Required[str]
    """When the agent should transfer the call to this destination."""

    destination: Required[ConfigSystemToolsTransferToNumberTransferDestination]
    """Where to transfer the call."""


class ConfigSystemToolsTransferToNumber(TypedDict, total=False):
    """Configuration for transferring the call.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    description: Optional[str]
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """

    transfers: Iterable[ConfigSystemToolsTransferToNumberTransfer]
    """Destinations the agent can transfer calls to."""


class ConfigSystemToolsVoicemailDetection(TypedDict, total=False):
    """Configuration for detecting voicemail.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    description: Optional[str]
    """What the tool does and when the agent should use it.

    Set to `null` to use the default system-optimized description.
    """

    message: Optional[str]
    """Message spoken after voicemail is detected.

    Set to `null` for no configured message.
    """

    pre_tool_speech: Literal["auto", "force", "off"]
    """Controls whether the agent speaks before using the tool.

    `auto` lets the agent decide, `force` always makes the agent speak first, and
    `off` never asks it to.
    """


class ConfigSystemTools(TypedDict, total=False):
    """Built-in tools available to the agent."""

    end_call: Optional[ConfigSystemToolsEndCall]
    """Configuration for ending the call.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    send_dtmf: Optional[ConfigSystemToolsSendDtmf]
    """Configuration for sending DTMF tones.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    skip_turn: Optional[ConfigSystemToolsSkipTurn]
    """
    Skip the agent's turn when the user asks for time to think or perform an action,
    such as "Give me a second" or "Let me check". Existing check-in timing stays
    unchanged unless `wait_timeout_secs` is configured. A configured timeout
    temporarily changes the check-in timer; user speech or DTMF restores the
    original timeout. Set this tool to `null` to disable it.
    """

    transfer_to_number: Optional[ConfigSystemToolsTransferToNumber]
    """Configuration for transferring the call.

    Omit to keep the current setting or set to `null` to disable this tool.
    """

    voicemail_detection: Optional[ConfigSystemToolsVoicemailDetection]
    """Configuration for detecting voicemail.

    Omit to keep the current setting or set to `null` to disable this tool.
    """


class ConfigTool(TypedDict, total=False):
    id: Required[str]
    """ID of a tool from the Tools API."""


class ConfigTurn(TypedDict, total=False):
    inactivity_check_in_secs: Optional[int]
    """Seconds of inactivity before the agent checks in, from `5` to `60`.

    Defaults to `8`. Set to `null` to disable check-ins. When enabled, it must be
    less than `inactivity_end_call_secs`.
    """

    inactivity_end_call_secs: int
    """
    Seconds of inactivity before the agent says a farewell message and ends the
    call, from `20` to `240`. Defaults to `240`; cannot be `null`.
    """


class Config(TypedDict, total=False):
    audio: ConfigAudio

    dynamic_variable_placeholders: Dict[str, Union[str, float, bool]]
    """Sample values for test calls, keyed by custom variable name.

    These are not used in production. PATCH replaces the whole map; omit it to keep
    existing samples or use `{}` to clear them.
    """

    event_webhook_id: Optional[str]
    """ID of the event webhook that receives events from this agent."""

    initial_message: Optional[str]
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

    knowledge_base_documents: Iterable[ConfigKnowledgeBaseDocument]
    """Knowledge base documents attached to the agent."""

    knowledge_base_folders: Iterable[ConfigKnowledgeBaseFolder]
    """Knowledge base folders attached to the agent."""

    language: ConfigLanguage

    model: ConfigModel

    prompt_optimization: bool
    """When enabled, the prompt is optimized with Cartesia's voice guidelines.

    Defaults to `true`.
    """

    speculative_generation: bool
    """
    When enabled, starts generating an LLM response eagerly to reduce perceived
    latency, before confirming that the user’s turn has ended. May increase LLM
    costs. Defaults to `true`.
    """

    system_tools: ConfigSystemTools
    """Built-in tools available to the agent."""

    timezone: str
    """Time zone for `{{system__time}}`, such as `America/New_York`.

    Defaults to `UTC`.
    """

    tools: Iterable[ConfigTool]
    """Tools available to the agent."""

    turn: ConfigTurn
