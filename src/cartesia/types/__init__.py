# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .voice import Voice as Voice
from .shared import WordTimestamps as WordTimestamps, PhonemeTimestamps as PhonemeTimestamps
from .dataset import Dataset as Dataset
from .fine_tune import FineTune as FineTune
from .tts_model import TTSModel as TTSModel
from .model_speed import ModelSpeed as ModelSpeed
from .infill_model import InfillModel as InfillModel
from .raw_encoding import RawEncoding as RawEncoding
from .stt_encoding import STTEncoding as STTEncoding
from .agent_summary import AgentSummary as AgentSummary
from .tts_sse_event import TTSSSEEvent as TTSSSEEvent
from .voice_metadata import VoiceMetadata as VoiceMetadata
from .stt_batch_model import STTBatchModel as STTBatchModel
from .voice_specifier import VoiceSpecifier as VoiceSpecifier
from .voice_get_params import VoiceGetParams as VoiceGetParams
from .generation_config import GenerationConfig as GenerationConfig
from .tts_infill_params import TTSInfillParams as TTSInfillParams
from .voice_list_params import VoiceListParams as VoiceListParams
from .generation_request import GenerationRequest as GenerationRequest
from .pronunciation_dict import PronunciationDict as PronunciationDict
from .stt_error_response import STTErrorResponse as STTErrorResponse
from .emotion import Emotion as Emotion
from .gender import Gender as Gender
from .localize_dialect import LocalizeDialect as LocalizeDialect
from .localize_target_language import LocalizeTargetLanguage as LocalizeTargetLanguage
from .supported_language import SupportedLanguage as SupportedLanguage
from .voice_clone_params import VoiceCloneParams as VoiceCloneParams
from .websocket_response import WebsocketResponse as WebsocketResponse
from .agent_list_response import AgentListResponse as AgentListResponse
from .agent_update_params import AgentUpdateParams as AgentUpdateParams
from .dataset_list_params import DatasetListParams as DatasetListParams
from .gender_presentation import GenderPresentation as GenderPresentation
from .get_status_response import GetStatusResponse as GetStatusResponse
from .tts_generate_params import TTSGenerateParams as TTSGenerateParams
from .voice_update_params import VoiceUpdateParams as VoiceUpdateParams
from .fine_tune_base_model import FineTuneBaseModel as FineTuneBaseModel
from .dataset_create_params import DatasetCreateParams as DatasetCreateParams
from .dataset_update_params import DatasetUpdateParams as DatasetUpdateParams
from .fine_tune_list_params import FineTuneListParams as FineTuneListParams
from .stt_transcribe_params import (
    STTTranscribeParams as STTTranscribeParams,
    SttTranscribeParams as SttTranscribeParams,
)
from .voice_localize_params import VoiceLocalizeParams as VoiceLocalizeParams
from .voice_specifier_param import VoiceSpecifierParam as VoiceSpecifierParam
from .websocket_client_event import WebsocketClientEvent as WebsocketClientEvent
from .websocket_reconnection import (
    ReconnectingEvent as ReconnectingEvent,
    ReconnectingOverrides as ReconnectingOverrides,
)
from .fine_tune_create_params import FineTuneCreateParams as FineTuneCreateParams
from .generation_config_param import GenerationConfigParam as GenerationConfigParam
from .mp3_output_format_param import MP3OutputFormatParam as MP3OutputFormatParam
from .output_format_container import OutputFormatContainer as OutputFormatContainer
from .pronunciation_dict_item import PronunciationDictItem as PronunciationDictItem
from .raw_output_format_param import RawOutputFormatParam as RawOutputFormatParam
from .stt_transcribe_response import (
    STTTranscribeResponse as STTTranscribeResponse,
    SttTranscribeResponse as SttTranscribeResponse,
)
from .tts_generate_sse_params import (
    TTSGenerateSSEParams as TTSGenerateSSEParams,
    TTSGenerateSseParams as TTSGenerateSseParams,
)
from .voice_changer_sse_event import VoiceChangerSSEEvent as VoiceChangerSSEEvent
from .wav_output_format_param import WAVOutputFormatParam as WAVOutputFormatParam
from .generation_request_param import GenerationRequestParam as GenerationRequestParam
from .access_token_create_params import AccessTokenCreateParams as AccessTokenCreateParams
from .access_token_create_response import AccessTokenCreateResponse as AccessTokenCreateResponse
from .fine_tune_list_voices_params import FineTuneListVoicesParams as FineTuneListVoicesParams
from .websocket_client_event_param import WebsocketClientEventParam as WebsocketClientEventParam
from .websocket_connection_options import (
    WebSocketConnectionOptions as WebSocketConnectionOptions,
    WebsocketConnectionOptions as WebsocketConnectionOptions,
)
from .agent_list_templates_response import AgentListTemplatesResponse as AgentListTemplatesResponse
from .pronunciation_dict_item_param import PronunciationDictItemParam as PronunciationDictItemParam
from .voice_changer_generate_params import VoiceChangerGenerateParams as VoiceChangerGenerateParams
from .pronunciation_dict_list_params import PronunciationDictListParams as PronunciationDictListParams
from .pronunciation_dict_create_params import PronunciationDictCreateParams as PronunciationDictCreateParams
from .pronunciation_dict_update_params import PronunciationDictUpdateParams as PronunciationDictUpdateParams
from .agent_list_phone_numbers_response import AgentListPhoneNumbersResponse as AgentListPhoneNumbersResponse
from .voice_changer_generate_sse_params import VoiceChangerGenerateSSEParams as VoiceChangerGenerateSSEParams
from .voice_changer_change_voice_sse_params import (
    VoiceChangerChangeVoiceSseParams as VoiceChangerChangeVoiceSseParams,
)
from .voice_changer_change_voice_bytes_params import (
    VoiceChangerChangeVoiceBytesParams as VoiceChangerChangeVoiceBytesParams,
)
