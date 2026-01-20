# Cartesia

Types:

```python
from cartesia.types import GetStatusResponse
```

Methods:

- <code title="get /">client.<a href="./src/cartesia/_client.py">get_status</a>() -> <a href="./src/cartesia/types/get_status_response.py">GetStatusResponse</a></code>

# Agents

Types:

```python
from cartesia.types import (
    AgentSummary,
    AgentListResponse,
    AgentListPhoneNumbersResponse,
    AgentListTemplatesResponse,
)
```

Methods:

- <code title="get /agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">retrieve</a>(agent_id) -> <a href="./src/cartesia/types/agent_summary.py">AgentSummary</a></code>
- <code title="patch /agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">update</a>(agent_id, \*\*<a href="src/cartesia/types/agent_update_params.py">params</a>) -> <a href="./src/cartesia/types/agent_summary.py">AgentSummary</a></code>
- <code title="get /agents">client.agents.<a href="./src/cartesia/resources/agents/agents.py">list</a>() -> <a href="./src/cartesia/types/agent_list_response.py">AgentListResponse</a></code>
- <code title="delete /agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">delete</a>(agent_id) -> None</code>
- <code title="get /agents/{agent_id}/phone-numbers">client.agents.<a href="./src/cartesia/resources/agents/agents.py">list_phone_numbers</a>(agent_id) -> <a href="./src/cartesia/types/agent_list_phone_numbers_response.py">AgentListPhoneNumbersResponse</a></code>
- <code title="get /agents/templates">client.agents.<a href="./src/cartesia/resources/agents/agents.py">list_templates</a>() -> <a href="./src/cartesia/types/agent_list_templates_response.py">AgentListTemplatesResponse</a></code>

## Calls

Types:

```python
from cartesia.types.agents import AgentCall, AgentTranscript
```

Methods:

- <code title="get /agents/calls/{call_id}">client.agents.calls.<a href="./src/cartesia/resources/agents/calls.py">retrieve</a>(call_id) -> <a href="./src/cartesia/types/agents/agent_call.py">AgentCall</a></code>
- <code title="get /agents/calls">client.agents.calls.<a href="./src/cartesia/resources/agents/calls.py">list</a>(\*\*<a href="src/cartesia/types/agents/call_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/agent_call.py">SyncCursorIDPage[AgentCall]</a></code>
- <code title="get /agents/calls/{call_id}/audio">client.agents.calls.<a href="./src/cartesia/resources/agents/calls.py">download_audio</a>(call_id) -> BinaryAPIResponse</code>

## Metrics

Types:

```python
from cartesia.types.agents import Metric, MetricListResponse
```

Methods:

- <code title="post /agents/metrics">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">create</a>(\*\*<a href="src/cartesia/types/agents/metric_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/metric.py">Metric</a></code>
- <code title="get /agents/metrics/{metric_id}">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">retrieve</a>(metric_id) -> <a href="./src/cartesia/types/agents/metric.py">Metric</a></code>
- <code title="get /agents/metrics">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">list</a>(\*\*<a href="src/cartesia/types/agents/metric_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/metric_list_response.py">MetricListResponse</a></code>
- <code title="post /agents/{agent_id}/metrics/{metric_id}">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">add_to_agent</a>(metric_id, \*, agent_id) -> None</code>
- <code title="delete /agents/{agent_id}/metrics/{metric_id}">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">remove_from_agent</a>(metric_id, \*, agent_id) -> None</code>

### Results

Types:

```python
from cartesia.types.agents.metrics import ResultListResponse, ResultExportResponse
```

Methods:

- <code title="get /agents/metrics/results">client.agents.metrics.results.<a href="./src/cartesia/resources/agents/metrics/results.py">list</a>(\*\*<a href="src/cartesia/types/agents/metrics/result_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/metrics/result_list_response.py">SyncCursorIDPage[ResultListResponse]</a></code>
- <code title="get /agents/metrics/results/export">client.agents.metrics.results.<a href="./src/cartesia/resources/agents/metrics/results.py">export</a>(\*\*<a href="src/cartesia/types/agents/metrics/result_export_params.py">params</a>) -> str</code>

## Deployments

Types:

```python
from cartesia.types.agents import Deployment, DeploymentListResponse
```

Methods:

- <code title="get /agents/deployments/{deployment_id}">client.agents.deployments.<a href="./src/cartesia/resources/agents/deployments.py">retrieve</a>(deployment_id) -> <a href="./src/cartesia/types/agents/deployment.py">Deployment</a></code>
- <code title="get /agents/{agent_id}/deployments">client.agents.deployments.<a href="./src/cartesia/resources/agents/deployments.py">list</a>(agent_id) -> <a href="./src/cartesia/types/agents/deployment_list_response.py">DeploymentListResponse</a></code>

# AccessToken

Types:

```python
from cartesia.types import AccessTokenCreateResponse
```

Methods:

- <code title="post /access-token">client.access_token.<a href="./src/cartesia/resources/access_token.py">create</a>(\*\*<a href="src/cartesia/types/access_token_create_params.py">params</a>) -> <a href="./src/cartesia/types/access_token_create_response.py">AccessTokenCreateResponse</a></code>

# Datasets

Types:

```python
from cartesia.types import Dataset
```

Methods:

- <code title="post /datasets/">client.datasets.<a href="./src/cartesia/resources/datasets/datasets.py">create</a>(\*\*<a href="src/cartesia/types/dataset_create_params.py">params</a>) -> <a href="./src/cartesia/types/dataset.py">Dataset</a></code>
- <code title="get /datasets/{id}">client.datasets.<a href="./src/cartesia/resources/datasets/datasets.py">retrieve</a>(id) -> <a href="./src/cartesia/types/dataset.py">Dataset</a></code>
- <code title="patch /datasets/{id}">client.datasets.<a href="./src/cartesia/resources/datasets/datasets.py">update</a>(id, \*\*<a href="src/cartesia/types/dataset_update_params.py">params</a>) -> None</code>
- <code title="get /datasets/">client.datasets.<a href="./src/cartesia/resources/datasets/datasets.py">list</a>(\*\*<a href="src/cartesia/types/dataset_list_params.py">params</a>) -> <a href="./src/cartesia/types/dataset.py">SyncCursorIDPage[Dataset]</a></code>
- <code title="delete /datasets/{id}">client.datasets.<a href="./src/cartesia/resources/datasets/datasets.py">delete</a>(id) -> None</code>

## Files

Types:

```python
from cartesia.types.datasets import FileListResponse
```

Methods:

- <code title="get /datasets/{id}/files">client.datasets.files.<a href="./src/cartesia/resources/datasets/files.py">list</a>(id, \*\*<a href="src/cartesia/types/datasets/file_list_params.py">params</a>) -> <a href="./src/cartesia/types/datasets/file_list_response.py">SyncCursorIDPage[FileListResponse]</a></code>
- <code title="delete /datasets/{id}/files/{fileID}">client.datasets.files.<a href="./src/cartesia/resources/datasets/files.py">delete</a>(file_id, \*, id) -> None</code>
- <code title="post /datasets/{id}/files">client.datasets.files.<a href="./src/cartesia/resources/datasets/files.py">upload</a>(id, \*\*<a href="src/cartesia/types/datasets/file_upload_params.py">params</a>) -> None</code>

# FineTunes

Types:

```python
from cartesia.types import FineTune
```

Methods:

- <code title="post /fine-tunes/">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">create</a>(\*\*<a href="src/cartesia/types/fine_tune_create_params.py">params</a>) -> <a href="./src/cartesia/types/fine_tune.py">FineTune</a></code>
- <code title="get /fine-tunes/{id}">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">retrieve</a>(id) -> <a href="./src/cartesia/types/fine_tune.py">FineTune</a></code>
- <code title="get /fine-tunes/">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">list</a>(\*\*<a href="src/cartesia/types/fine_tune_list_params.py">params</a>) -> <a href="./src/cartesia/types/fine_tune.py">SyncCursorIDPage[FineTune]</a></code>
- <code title="delete /fine-tunes/{id}">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">delete</a>(id) -> None</code>
- <code title="get /fine-tunes/{id}/voices">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">list_voices</a>(id, \*\*<a href="src/cartesia/types/fine_tune_list_voices_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">SyncCursorIDPage[Voice]</a></code>

# Infill

Types:

```python
from cartesia.types import OutputFormatContainer, RawEncoding
```

Methods:

- <code title="post /infill/bytes">client.infill.<a href="./src/cartesia/resources/infill.py">create</a>(\*\*<a href="src/cartesia/types/infill_create_params.py">params</a>) -> BinaryAPIResponse</code>

# PronunciationDicts

Types:

```python
from cartesia.types import PronunciationDict, PronunciationDictItem
```

Methods:

- <code title="post /pronunciation-dicts/">client.pronunciation_dicts.<a href="./src/cartesia/resources/pronunciation_dicts.py">create</a>(\*\*<a href="src/cartesia/types/pronunciation_dict_create_params.py">params</a>) -> <a href="./src/cartesia/types/pronunciation_dict.py">PronunciationDict</a></code>
- <code title="get /pronunciation-dicts/{id}">client.pronunciation_dicts.<a href="./src/cartesia/resources/pronunciation_dicts.py">retrieve</a>(id) -> <a href="./src/cartesia/types/pronunciation_dict.py">PronunciationDict</a></code>
- <code title="patch /pronunciation-dicts/{id}">client.pronunciation_dicts.<a href="./src/cartesia/resources/pronunciation_dicts.py">update</a>(id, \*\*<a href="src/cartesia/types/pronunciation_dict_update_params.py">params</a>) -> <a href="./src/cartesia/types/pronunciation_dict.py">PronunciationDict</a></code>
- <code title="get /pronunciation-dicts/">client.pronunciation_dicts.<a href="./src/cartesia/resources/pronunciation_dicts.py">list</a>(\*\*<a href="src/cartesia/types/pronunciation_dict_list_params.py">params</a>) -> <a href="./src/cartesia/types/pronunciation_dict.py">SyncCursorIDPage[PronunciationDict]</a></code>
- <code title="delete /pronunciation-dicts/{id}">client.pronunciation_dicts.<a href="./src/cartesia/resources/pronunciation_dicts.py">delete</a>(id) -> None</code>

# Stt

Types:

```python
from cartesia.types import SttTranscribeResponse
```

Methods:

- <code title="post /stt">client.stt.<a href="./src/cartesia/resources/stt.py">transcribe</a>(\*\*<a href="src/cartesia/types/stt_transcribe_params.py">params</a>) -> <a href="./src/cartesia/types/stt_transcribe_response.py">SttTranscribeResponse</a></code>

# TTS

Types:

```python
from cartesia.types import (
    GenerationConfig,
    GenerationRequest,
    ModelSpeed,
    RawOutputFormat,
    VoiceSpecifier,
    WebsocketClientEvent,
    WebsocketResponse,
)
```

Methods:

- <code title="post /tts/bytes">client.tts.<a href="./src/cartesia/resources/tts.py">generate</a>(\*\*<a href="src/cartesia/types/tts_generate_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /tts/sse">client.tts.<a href="./src/cartesia/resources/tts.py">generate_sse</a>(\*\*<a href="src/cartesia/types/tts_generate_sse_params.py">params</a>) -> None</code>

# VoiceChanger

Methods:

- <code title="post /voice-changer/bytes">client.voice_changer.<a href="./src/cartesia/resources/voice_changer.py">change_voice_bytes</a>(\*\*<a href="src/cartesia/types/voice_changer_change_voice_bytes_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /voice-changer/sse">client.voice_changer.<a href="./src/cartesia/resources/voice_changer.py">change_voice_sse</a>(\*\*<a href="src/cartesia/types/voice_changer_change_voice_sse_params.py">params</a>) -> None</code>

# Voices

Types:

```python
from cartesia.types import GenderPresentation, SupportedLanguage, Voice, VoiceMetadata
```

Methods:

- <code title="patch /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">update</a>(id, \*\*<a href="src/cartesia/types/voice_update_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="get /voices">client.voices.<a href="./src/cartesia/resources/voices.py">list</a>(\*\*<a href="src/cartesia/types/voice_list_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">SyncCursorIDPage[Voice]</a></code>
- <code title="delete /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">delete</a>(id) -> None</code>
- <code title="post /voices/clone">client.voices.<a href="./src/cartesia/resources/voices.py">clone</a>(\*\*<a href="src/cartesia/types/voice_clone_params.py">params</a>) -> <a href="./src/cartesia/types/voice_metadata.py">VoiceMetadata</a></code>
- <code title="get /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">get</a>(id, \*\*<a href="src/cartesia/types/voice_get_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="post /voices/localize">client.voices.<a href="./src/cartesia/resources/voices.py">localize</a>(\*\*<a href="src/cartesia/types/voice_localize_params.py">params</a>) -> <a href="./src/cartesia/types/voice_metadata.py">VoiceMetadata</a></code>
