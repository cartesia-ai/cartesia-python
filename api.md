# Shared Types

```python
from cartesia.types import PhonemeTimestamps, WordTimestamps
```

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
from cartesia.types import Agent, AgentSummary
```

Methods:

- <code title="post /v1/agents">client.agents.<a href="./src/cartesia/resources/agents/agents.py">create</a>(\*\*<a href="src/cartesia/types/agent_create_params.py">params</a>) -> <a href="./src/cartesia/types/agent.py">Agent</a></code>
- <code title="get /v1/agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">retrieve</a>(agent_id) -> <a href="./src/cartesia/types/agent.py">Agent</a></code>
- <code title="patch /v1/agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">update</a>(agent_id, \*\*<a href="src/cartesia/types/agent_update_params.py">params</a>) -> <a href="./src/cartesia/types/agent.py">Agent</a></code>
- <code title="get /v1/agents">client.agents.<a href="./src/cartesia/resources/agents/agents.py">list</a>(\*\*<a href="src/cartesia/types/agent_list_params.py">params</a>) -> <a href="./src/cartesia/types/agent_summary.py">SyncCursorIDPage[AgentSummary]</a></code>
- <code title="delete /v1/agents/{agent_id}">client.agents.<a href="./src/cartesia/resources/agents/agents.py">delete</a>(agent_id) -> None</code>

## Models

Types:

```python
from cartesia.types.agents import Model
```

Methods:

- <code title="get /v1/agents/models/{model_id}">client.agents.models.<a href="./src/cartesia/resources/agents/models.py">retrieve</a>(model_id) -> <a href="./src/cartesia/types/agents/model.py">Model</a></code>
- <code title="get /v1/agents/models">client.agents.models.<a href="./src/cartesia/resources/agents/models.py">list</a>(\*\*<a href="src/cartesia/types/agents/model_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/model.py">SyncCursorIDPage[Model]</a></code>

## Tools

Types:

```python
from cartesia.types.agents import Tool, WebhookBodyParam, ToolListResponse
```

Methods:

- <code title="post /v1/agents/tools">client.agents.tools.<a href="./src/cartesia/resources/agents/tools.py">create</a>(\*\*<a href="src/cartesia/types/agents/tool_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/tool.py">Tool</a></code>
- <code title="get /v1/agents/tools/{tool_id}">client.agents.tools.<a href="./src/cartesia/resources/agents/tools.py">retrieve</a>(tool_id, \*\*<a href="src/cartesia/types/agents/tool_retrieve_params.py">params</a>) -> <a href="./src/cartesia/types/agents/tool.py">Tool</a></code>
- <code title="patch /v1/agents/tools/{tool_id}">client.agents.tools.<a href="./src/cartesia/resources/agents/tools.py">update</a>(tool_id, \*\*<a href="src/cartesia/types/agents/tool_update_params.py">params</a>) -> <a href="./src/cartesia/types/agents/tool.py">Tool</a></code>
- <code title="get /v1/agents/tools">client.agents.tools.<a href="./src/cartesia/resources/agents/tools.py">list</a>(\*\*<a href="src/cartesia/types/agents/tool_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/tool_list_response.py">ToolListResponse</a></code>
- <code title="delete /v1/agents/tools/{tool_id}">client.agents.tools.<a href="./src/cartesia/resources/agents/tools.py">delete</a>(tool_id) -> None</code>

## Versions

Types:

```python
from cartesia.types.agents import Version
```

Methods:

- <code title="get /v1/agents/{agent_id}/versions/{version_id}">client.agents.versions.<a href="./src/cartesia/resources/agents/versions.py">retrieve</a>(version_id, \*, agent_id) -> <a href="./src/cartesia/types/agents/version.py">Version</a></code>
- <code title="get /v1/agents/{agent_id}/versions">client.agents.versions.<a href="./src/cartesia/resources/agents/versions.py">list</a>(agent_id, \*\*<a href="src/cartesia/types/agents/version_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/version.py">SyncCursorIDPage[Version]</a></code>

## Calls

Types:

```python
from cartesia.types.agents import (
    AgentCall,
    AgentTranscript,
    CallBatch,
    CallCreateResponse,
    CallCancelResponse,
    CallLogsResponse,
)
```

Methods:

- <code title="post /agents/calls">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">create</a>(\*\*<a href="src/cartesia/types/agents/call_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/call_create_response.py">CallCreateResponse</a></code>
- <code title="get /agents/calls/{call_id}">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">retrieve</a>(call_id) -> <a href="./src/cartesia/types/agents/agent_call.py">AgentCall</a></code>
- <code title="get /agents/calls">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">list</a>(\*\*<a href="src/cartesia/types/agents/call_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/agent_call.py">SyncCursorIDPage[AgentCall]</a></code>
- <code title="delete /agents/calls/{call_id}">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">delete</a>(call_id) -> <a href="./src/cartesia/types/agents/agent_call.py">AgentCall</a></code>
- <code title="post /agents/calls/{call_id}/cancel">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">cancel</a>(call_id) -> <a href="./src/cartesia/types/agents/call_cancel_response.py">CallCancelResponse</a></code>
- <code title="get /agents/calls/{call_id}/audio">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">download_audio</a>(call_id) -> None</code>
- <code title="get /agents/calls/{call_id}/logs">client.agents.calls.<a href="./src/cartesia/resources/agents/calls/calls.py">logs</a>(call_id) -> <a href="./src/cartesia/types/agents/call_logs_response.py">CallLogsResponse</a></code>

### Batches

Methods:

- <code title="post /agents/calls/batches">client.agents.calls.batches.<a href="./src/cartesia/resources/agents/calls/batches.py">create</a>(\*\*<a href="src/cartesia/types/agents/calls/batch_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/call_batch.py">CallBatch</a></code>
- <code title="get /agents/calls/batches/{batch_id}">client.agents.calls.batches.<a href="./src/cartesia/resources/agents/calls/batches.py">retrieve</a>(batch_id) -> <a href="./src/cartesia/types/agents/call_batch.py">CallBatch</a></code>
- <code title="get /agents/calls/batches">client.agents.calls.batches.<a href="./src/cartesia/resources/agents/calls/batches.py">list</a>(\*\*<a href="src/cartesia/types/agents/calls/batch_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/call_batch.py">SyncCursorIDPage[CallBatch]</a></code>
- <code title="post /agents/calls/batches/{batch_id}/cancel">client.agents.calls.batches.<a href="./src/cartesia/resources/agents/calls/batches.py">cancel</a>(batch_id) -> <a href="./src/cartesia/types/agents/call_batch.py">CallBatch</a></code>
- <code title="post /agents/calls/batches/{batch_id}/retry">client.agents.calls.batches.<a href="./src/cartesia/resources/agents/calls/batches.py">retry</a>(batch_id) -> <a href="./src/cartesia/types/agents/call_batch.py">CallBatch</a></code>

## Metrics

Types:

```python
from cartesia.types.agents import Metric, MetricListResponse
```

Methods:

- <code title="post /agents/metrics">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">create</a>(\*\*<a href="src/cartesia/types/agents/metric_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/metric.py">Metric</a></code>
- <code title="get /agents/metrics/{metric_id}">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">retrieve</a>(metric_id) -> <a href="./src/cartesia/types/agents/metric.py">Metric</a></code>
- <code title="get /agents/metrics">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">list</a>(\*\*<a href="src/cartesia/types/agents/metric_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/metric_list_response.py">MetricListResponse</a></code>
- <code title="delete /agents/metrics/{metric_id}">client.agents.metrics.<a href="./src/cartesia/resources/agents/metrics/metrics.py">delete</a>(metric_id) -> None</code>
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

## Webhooks

Types:

```python
from cartesia.types.agents import (
    Webhook,
    WebhookRetrieveResponse,
    WebhookUpdateResponse,
    WebhookListResponse,
    WebhookDeleteResponse,
)
```

Methods:

- <code title="post /agents/webhooks">client.agents.webhooks.<a href="./src/cartesia/resources/agents/webhooks.py">create</a>(\*\*<a href="src/cartesia/types/agents/webhook_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/webhook.py">Webhook</a></code>
- <code title="get /agents/webhooks/{webhook_id}">client.agents.webhooks.<a href="./src/cartesia/resources/agents/webhooks.py">retrieve</a>(webhook_id) -> <a href="./src/cartesia/types/agents/webhook_retrieve_response.py">WebhookRetrieveResponse</a></code>
- <code title="patch /agents/webhooks/{webhook_id}">client.agents.webhooks.<a href="./src/cartesia/resources/agents/webhooks.py">update</a>(webhook_id, \*\*<a href="src/cartesia/types/agents/webhook_update_params.py">params</a>) -> str</code>
- <code title="get /agents/webhooks">client.agents.webhooks.<a href="./src/cartesia/resources/agents/webhooks.py">list</a>(\*\*<a href="src/cartesia/types/agents/webhook_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/webhook_list_response.py">SyncCursorIDPage[WebhookListResponse]</a></code>
- <code title="delete /agents/webhooks/{webhook_id}">client.agents.webhooks.<a href="./src/cartesia/resources/agents/webhooks.py">delete</a>(webhook_id) -> str</code>

## PhoneNumbers

Types:

```python
from cartesia.types.agents import PhoneNumber, PhoneNumberListResponse, PhoneNumberProvisionResponse
```

Methods:

- <code title="get /agents/phone-numbers/{id}">client.agents.phone_numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">retrieve</a>(id) -> <a href="./src/cartesia/types/agents/phone_number.py">PhoneNumber</a></code>
- <code title="patch /agents/phone-numbers/{id}">client.agents.phone_numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">update</a>(id, \*\*<a href="src/cartesia/types/agents/phone_number_update_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_number.py">PhoneNumber</a></code>
- <code title="get /agents/phone-numbers">client.agents.phone_numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">list</a>(\*\*<a href="src/cartesia/types/agents/phone_number_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_number_list_response.py">PhoneNumberListResponse</a></code>
- <code title="delete /agents/phone-numbers/{id}">client.agents.phone_numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">delete</a>(id) -> None</code>
- <code title="post /agents/phone-numbers">client.agents.phone*numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">import*</a>(\*\*<a href="src/cartesia/types/agents/phone_number_import_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_number.py">PhoneNumber</a></code>
- <code title="post /agents/phone-numbers/provision">client.agents.phone_numbers.<a href="./src/cartesia/resources/agents/phone_numbers/phone_numbers.py">provision</a>(\*\*<a href="src/cartesia/types/agents/phone_number_provision_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_number_provision_response.py">PhoneNumberProvisionResponse</a></code>

### Providers

Types:

```python
from cartesia.types.agents.phone_numbers import (
    ProviderCreateResponse,
    ProviderRetrieveResponse,
    ProviderUpdateResponse,
    ProviderListResponse,
)
```

Methods:

- <code title="post /agents/phone-numbers/providers">client.agents.phone_numbers.providers.<a href="./src/cartesia/resources/agents/phone_numbers/providers.py">create</a>(\*\*<a href="src/cartesia/types/agents/phone_numbers/provider_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_numbers/provider_create_response.py">ProviderCreateResponse</a></code>
- <code title="get /agents/phone-numbers/providers/{id}">client.agents.phone_numbers.providers.<a href="./src/cartesia/resources/agents/phone_numbers/providers.py">retrieve</a>(id) -> <a href="./src/cartesia/types/agents/phone_numbers/provider_retrieve_response.py">ProviderRetrieveResponse</a></code>
- <code title="patch /agents/phone-numbers/providers/{id}">client.agents.phone_numbers.providers.<a href="./src/cartesia/resources/agents/phone_numbers/providers.py">update</a>(id, \*\*<a href="src/cartesia/types/agents/phone_numbers/provider_update_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_numbers/provider_update_response.py">ProviderUpdateResponse</a></code>
- <code title="get /agents/phone-numbers/providers">client.agents.phone_numbers.providers.<a href="./src/cartesia/resources/agents/phone_numbers/providers.py">list</a>(\*\*<a href="src/cartesia/types/agents/phone_numbers/provider_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/phone_numbers/provider_list_response.py">ProviderListResponse</a></code>
- <code title="delete /agents/phone-numbers/providers/{id}">client.agents.phone_numbers.providers.<a href="./src/cartesia/resources/agents/phone_numbers/providers.py">delete</a>(id) -> None</code>

## KnowledgeBase

### Folders

Types:

```python
from cartesia.types.agents.knowledge_base import Folder, FolderListResponse
```

Methods:

- <code title="post /agents/folders">client.agents.knowledge_base.folders.<a href="./src/cartesia/resources/agents/knowledge_base/folders.py">create</a>(\*\*<a href="src/cartesia/types/agents/knowledge_base/folder_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/folder.py">Folder</a></code>
- <code title="get /agents/folders/{id}">client.agents.knowledge_base.folders.<a href="./src/cartesia/resources/agents/knowledge_base/folders.py">retrieve</a>(id) -> <a href="./src/cartesia/types/agents/knowledge_base/folder.py">Folder</a></code>
- <code title="patch /agents/folders/{id}">client.agents.knowledge_base.folders.<a href="./src/cartesia/resources/agents/knowledge_base/folders.py">update</a>(id, \*\*<a href="src/cartesia/types/agents/knowledge_base/folder_update_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/folder.py">Folder</a></code>
- <code title="get /agents/folders">client.agents.knowledge_base.folders.<a href="./src/cartesia/resources/agents/knowledge_base/folders.py">list</a>(\*\*<a href="src/cartesia/types/agents/knowledge_base/folder_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/folder_list_response.py">FolderListResponse</a></code>
- <code title="delete /agents/folders/{id}">client.agents.knowledge_base.folders.<a href="./src/cartesia/resources/agents/knowledge_base/folders.py">delete</a>(id, \*\*<a href="src/cartesia/types/agents/knowledge_base/folder_delete_params.py">params</a>) -> None</code>

### Documents

Types:

```python
from cartesia.types.agents.knowledge_base import Document, DocumentCreateBulkResponse
```

Methods:

- <code title="post /agents/documents">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">create</a>(\*\*<a href="src/cartesia/types/agents/knowledge_base/document_create_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/document.py">Document</a></code>
- <code title="get /agents/documents/{document_id}">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">retrieve</a>(document_id) -> <a href="./src/cartesia/types/agents/knowledge_base/document.py">Document</a></code>
- <code title="patch /agents/documents/{document_id}">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">update</a>(document_id, \*\*<a href="src/cartesia/types/agents/knowledge_base/document_update_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/document.py">Document</a></code>
- <code title="get /agents/documents">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">list</a>(\*\*<a href="src/cartesia/types/agents/knowledge_base/document_list_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/document.py">SyncCursorIDPage[Document]</a></code>
- <code title="delete /agents/documents/{document_id}">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">delete</a>(document_id, \*\*<a href="src/cartesia/types/agents/knowledge_base/document_delete_params.py">params</a>) -> None</code>
- <code title="post /agents/documents/bulk">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">create_bulk</a>(\*\*<a href="src/cartesia/types/agents/knowledge_base/document_create_bulk_params.py">params</a>) -> <a href="./src/cartesia/types/agents/knowledge_base/document_create_bulk_response.py">DocumentCreateBulkResponse</a></code>
- <code title="post /agents/documents/{document_id}/retry">client.agents.knowledge_base.documents.<a href="./src/cartesia/resources/agents/knowledge_base/documents.py">retry</a>(document_id) -> <a href="./src/cartesia/types/agents/knowledge_base/document.py">Document</a></code>

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
from cartesia.types import FineTune, FineTuneBaseModel
```

Methods:

- <code title="post /fine-tunes/">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">create</a>(\*\*<a href="src/cartesia/types/fine_tune_create_params.py">params</a>) -> <a href="./src/cartesia/types/fine_tune.py">FineTune</a></code>
- <code title="get /fine-tunes/{id}">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">retrieve</a>(id) -> <a href="./src/cartesia/types/fine_tune.py">FineTune</a></code>
- <code title="get /fine-tunes/">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">list</a>(\*\*<a href="src/cartesia/types/fine_tune_list_params.py">params</a>) -> <a href="./src/cartesia/types/fine_tune.py">SyncCursorIDPage[FineTune]</a></code>
- <code title="delete /fine-tunes/{id}">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">delete</a>(id) -> None</code>
- <code title="get /fine-tunes/{id}/voices">client.fine_tunes.<a href="./src/cartesia/resources/fine_tunes.py">list_voices</a>(id, \*\*<a href="src/cartesia/types/fine_tune_list_voices_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">SyncCursorIDPage[Voice]</a></code>

# Models

Types:

```python
from cartesia.types import ListModelsResponse, ModelCapability, ModelCatalogEntry, STTMode
```

Methods:

- <code title="get /models">client.models.<a href="./src/cartesia/resources/models.py">list</a>(\*\*<a href="src/cartesia/types/model_list_params.py">params</a>) -> <a href="./src/cartesia/types/list_models_response.py">ListModelsResponse</a></code>

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

# STT

Types:

```python
from cartesia.types import STTBatchModel, STTEncoding, STTErrorResponse, STTTranscribeResponse
```

Methods:

- <code title="post /stt">client.stt.<a href="./src/cartesia/resources/stt/stt.py">transcribe</a>(\*\*<a href="src/cartesia/types/stt_transcribe_params.py">params</a>) -> <a href="./src/cartesia/types/stt_transcribe_response.py">STTTranscribeResponse</a></code>

## AutoFinalize

Types:

```python
from cartesia.types.stt import (
    STTAutoFinalizeConnected,
    STTAutoFinalizeModel,
    STTAutoFinalizeTurnEagerEnd,
    STTAutoFinalizeTurnEnd,
    STTAutoFinalizeTurnResume,
    STTAutoFinalizeTurnStart,
    STTAutoFinalizeTurnUpdate,
    STTAutoFinalizeWebsocketRequest,
    STTAutoFinalizeWebsocketResponse,
)
```

## ManualFinalize

Types:

```python
from cartesia.types.stt import (
    STTManualFinalizeDoneResponse,
    STTManualFinalizeFlushDoneResponse,
    STTManualFinalizeModel,
    STTManualFinalizeTranscriptResponse,
    STTManualFinalizeWebsocketRequest,
    STTManualFinalizeWebsocketResponse,
)
```

# TTS

Types:

```python
from cartesia.types import (
    Emotion,
    GenerationConfig,
    GenerationRequest,
    InfillModel,
    ModelSpeed,
    MP3OutputFormat,
    OutputFormatContainer,
    RawEncoding,
    RawOutputFormat,
    TTSModel,
    TTSSSEEvent,
    VoiceSpecifier,
    WAVOutputFormat,
    WebsocketClientEvent,
    WebsocketResponse,
)
```

Methods:

- <code title="post /tts/bytes">client.tts.<a href="./src/cartesia/resources/tts.py">generate</a>(\*\*<a href="src/cartesia/types/tts_generate_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /tts/sse">client.tts.<a href="./src/cartesia/resources/tts.py">generate_sse</a>(\*\*<a href="src/cartesia/types/tts_generate_sse_params.py">params</a>) -> <a href="./src/cartesia/types/tts_sse_event.py">TTSSSEEvent</a></code>
- <code title="post /infill/bytes">client.tts.<a href="./src/cartesia/resources/tts.py">infill</a>(\*\*<a href="src/cartesia/types/tts_infill_params.py">params</a>) -> BinaryAPIResponse</code>

# Watermark

Types:

```python
from cartesia.types import WatermarkDetectResponse
```

Methods:

- <code title="post /v1/watermark/detect">client.watermark.<a href="./src/cartesia/resources/watermark.py">detect</a>(\*\*<a href="src/cartesia/types/watermark_detect_params.py">params</a>) -> <a href="./src/cartesia/types/watermark_detect_response.py">WatermarkDetectResponse</a></code>

# Voices

Types:

```python
from cartesia.types import (
    Accent,
    AddVoiceAccentsRequest,
    AttachVoiceAccent,
    Gender,
    GenderPresentation,
    ListAccentsResponse,
    LocalizeDialect,
    LocalizeTargetLanguage,
    SupportedLanguage,
    Voice,
    VoiceAccent,
    VoiceLocale,
    VoiceMetadata,
)
```

Methods:

- <code title="patch /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">update</a>(id, \*\*<a href="src/cartesia/types/voice_update_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="get /voices">client.voices.<a href="./src/cartesia/resources/voices.py">list</a>(\*\*<a href="src/cartesia/types/voice_list_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">SyncCursorIDPage[Voice]</a></code>
- <code title="delete /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">delete</a>(id) -> None</code>
- <code title="patch /voices/{id}/accents">client.voices.<a href="./src/cartesia/resources/voices.py">add_accents</a>(id, \*\*<a href="src/cartesia/types/voice_add_accents_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="post /voices/clone">client.voices.<a href="./src/cartesia/resources/voices.py">clone</a>(\*\*<a href="src/cartesia/types/voice_clone_params.py">params</a>) -> <a href="./src/cartesia/types/voice_metadata.py">VoiceMetadata</a></code>
- <code title="delete /voices/{id}/accents/{accent_id}">client.voices.<a href="./src/cartesia/resources/voices.py">delete_accent</a>(accent_id, \*, id) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="get /voices/{id}">client.voices.<a href="./src/cartesia/resources/voices.py">get</a>(id, \*\*<a href="src/cartesia/types/voice_get_params.py">params</a>) -> <a href="./src/cartesia/types/voice.py">Voice</a></code>
- <code title="get /accents">client.voices.<a href="./src/cartesia/resources/voices.py">list_accents</a>() -> <a href="./src/cartesia/types/list_accents_response.py">ListAccentsResponse</a></code>
- <code title="post /voices/localize">client.voices.<a href="./src/cartesia/resources/voices.py">localize</a>(\*\*<a href="src/cartesia/types/voice_localize_params.py">params</a>) -> <a href="./src/cartesia/types/voice_metadata.py">VoiceMetadata</a></code>
