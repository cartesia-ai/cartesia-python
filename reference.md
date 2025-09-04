# Reference
## Agents
<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">list</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists all agents associated with your account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Returns the details of a specific agent. To create an agent, use the CLI or the Playground for the best experience and integration with Github.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.get(
    agent_id="agent_123",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.update(
    agent_id="agent_123",
    tts_voice="bf0a246a-8642-498a-9950-80c35e9276b5",
    tts_language="en",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — The name of the agent.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — The description of the agent.
    
</dd>
</dl>

<dl>
<dd>

**tts_voice:** `typing.Optional[VoiceId]` — The voice to use for text-to-speech.
    
</dd>
</dl>

<dl>
<dd>

**tts_language:** `typing.Optional[str]` — The language to use for text-to-speech.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.delete(
    agent_id="agent_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">templates</a>()</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List of public, Cartesia-provided agent templates to help you get started.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.templates()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">list_calls</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Lists calls sorted by start time in descending order for a specific agent. `agent_id` is required and if you want to include `transcript` in the response, add `expand=transcript` to the request. This endpoint is paginated.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
response = client.agents.list_calls(
    agent_id="agent_id",
)
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**expand:** `typing.Optional[str]` — The fields to expand in the response. Currently, the only supported value is `transcript`.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — (Pagination option)The ID of the call to start after.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` — (Pagination option) The ID of the call to end before.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — (Pagination option) The number of calls to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">get_call</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.get_call(
    call_id="ac_abc123",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**call_id:** `str` — The ID of the call.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">phone_numbers</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List the phone numbers associated with an agent. Currently, you can only have one phone number per agent and these are provisioned by Cartesia.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.phone_numbers(
    agent_id="agent_demo",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">list_metrics</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List of all LLM-as-a-Judge metrics owned by your account.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.list_metrics()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — (Pagination option) The ID of the last Metric in the current response as a cursor for the next page of results.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — (Pagination option) The number of metrics to return per page, ranging between 1 and 100. The default page limit is 10.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">get_metric</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a metric by its ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.get_metric(
    metric_id="am_abc123",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**metric_id:** `str` — The ID of the metric.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">create_metric</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new metric.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.create_metric(
    name="evaluate-user-satisfaction",
    display_name="Evaluate User Satisfaction",
    prompt="Task:\nEvaluate how engaged and satisfied the user is with the conversation. Engagement may be shown through active interest in the agent’s products/services, expressing that the agent was helpful, or indicating they would want to interact again.\n\nDecision Logic:\n- If the user shows strong engagement (asks detailed follow-up questions, expresses high interest, compliments the agent, or states they would use the service/agent again) → classify as HIGH_SATISFACTION\n- If the user shows some engagement (asks a few relevant questions, shows mild interest, or gives neutral feedback) → classify as MEDIUM_SATISFACTION\n- If the user shows little or no engagement (short answers, off-topic responses, disinterest, no signs of satisfaction) → classify as LOW_SATISFACTION\n\nNotes:\n- Engagement can be verbal (explicit statements of interest) or behavioral (asking more about features, prices, benefits, or next steps).\n- Expressions of satisfaction, gratitude, or willingness to call again count as positive engagement.\n- Ignore scripted greetings or polite closings unless they contain genuine feedback.\n\nReturn:\nOnly output the exact category name as a string: HIGH_SATISFACTION, MEDIUM_SATISFACTION, or LOW_SATISFACTION.\n",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — The name of the metric. This must be a unique name that only allows lower case letters, numbers, and the characters _, -, and .
    
</dd>
</dl>

<dl>
<dd>

**prompt:** `str` — The prompt associated with the metric, detailing the task and evaluation criteria.
    
</dd>
</dl>

<dl>
<dd>

**display_name:** `typing.Optional[str]` — The display name of the metric.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">list_metric_results</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated list of metric results. Filter results using the query parameters,
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
response = client.agents.list_metric_results()
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**deployment_id:** `typing.Optional[str]` — The ID of the deployment.
    
</dd>
</dl>

<dl>
<dd>

**metric_id:** `typing.Optional[str]` — The ID of the metric.
    
</dd>
</dl>

<dl>
<dd>

**call_id:** `typing.Optional[str]` — The ID of the call.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — A cursor to use in pagination. `starting_after` is a metric result ID that defines your place in the list. For example, if you make a /metrics/results request and receive 100 objects, ending with `metric_result_abc123`, your subsequent call can include `starting_after=metric_result_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` — A cursor to use in pagination. `ending_before` is a metric result ID that defines your place in the list. For example, if you make a /metrics/results request and receive 100 objects, starting with `metric_result_abc123`, your subsequent call can include `ending_before=metric_result_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of metric results to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">export_metric_results</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Export metric results to a CSV file. This endpoint is paginated with a default of 10 results per page and maximum of 100 results per page. Information on pagination can be found in the headers `x-has-more`, `x-limit`, and `x-next-page`.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.export_metric_results()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `typing.Optional[str]` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**deployment_id:** `typing.Optional[str]` — The ID of the deployment.
    
</dd>
</dl>

<dl>
<dd>

**metric_id:** `typing.Optional[str]` — The ID of the metric.
    
</dd>
</dl>

<dl>
<dd>

**call_id:** `typing.Optional[str]` — The ID of the call.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` — A cursor to use in pagination. `starting_after` is a metric result ID that defines your place in the list. For example, if you make a /metrics/results request and receive 100 objects, ending with `metric_result_abc123`, your subsequent call can include `starting_after=metric_result_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` — A cursor to use in pagination. `ending_before` is a metric result ID that defines your place in the list. For example, if you make a /metrics/results request and receive 100 objects, starting with `metric_result_abc123`, your subsequent call can include `ending_before=metric_result_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of metric results to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">add_metric_to_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Add a metric to an agent. Once the metric is added, it will be run on all calls made to the agent automatically from that point onwards.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.add_metric_to_agent(
    agent_id="agent_id",
    metric_id="metric_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**metric_id:** `str` — The ID of the metric.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">remove_metric_from_agent</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove a metric from an agent. Once the metric is removed, it will no longer be run on all calls made to the agent automatically from that point onwards. Existing metric results will remain.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.remove_metric_from_agent(
    agent_id="agent_id",
    metric_id="metric_id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**metric_id:** `str` — The ID of the metric.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">list_deployments</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List of all deployments associated with an agent.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.list_deployments(
    agent_id="agent_demo",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**agent_id:** `str` — The ID of the agent.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.agents.<a href="src/cartesia/agents/client.py">get_deployment</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Get a deployment by its ID.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.agents.get_deployment(
    deployment_id="ad_abc123",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**deployment_id:** `str` — The ID of the deployment.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## ApiStatus
<details><summary><code>client.api_status.<a href="src/cartesia/api_status/client.py">get</a>()</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.api_status.get()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Auth
<details><summary><code>client.auth.<a href="src/cartesia/auth/client.py">access_token</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generates a new Access Token for the client. These tokens are short-lived and should be used to make requests to the API from authenticated clients.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.auth.access_token(
    grants={"stt": True},
    expires_in=60,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**grants:** `typing.Optional[TokenGrantParams]` — The permissions to be granted via the token. Both TTS and STT grants are optional - specify only the capabilities you need.
    
</dd>
</dl>

<dl>
<dd>

**expires_in:** `typing.Optional[int]` — The number of seconds the token will be valid for since the time of generation. The maximum is 1 hour (3600 seconds).
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Datasets
<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated list of datasets
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of Datasets to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a Dataset ID that defines your
place in the list. For example, if you make a /datasets request and receive 20
objects, ending with `dataset_abc123`, your subsequent call can include
`starting_after=dataset_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a Dataset ID that defines your
place in the list. For example, if you make a /datasets request and receive 20
objects, starting with `dataset_abc123`, your subsequent call can include
`ending_before=dataset_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new dataset
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.create(
    name="name",
    description="description",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name for the new dataset
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — Optional description for the dataset
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific dataset by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.get(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the dataset to retrieve
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update an existing dataset
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.update(
    id="id",
    name="name",
    description="description",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the dataset to update
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — New name for the dataset
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — New description for the dataset
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a dataset
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.delete(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the dataset to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">list_files</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated list of files in a dataset
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.list_files(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the dataset to list files from
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of files to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a file ID that defines your
place in the list. For example, if you make a dataset files request and receive 20
objects, ending with `file_abc123`, your subsequent call can include
`starting_after=file_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a file ID that defines your
place in the list. For example, if you make a dataset files request and receive 20
objects, starting with `file_abc123`, your subsequent call can include
`ending_before=file_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">delete_file</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Remove a file from a dataset
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.datasets.delete_file(
    id="id",
    file_id="fileID",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the dataset containing the file
    
</dd>
</dl>

<dl>
<dd>

**file_id:** `str` — ID of the file to remove
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## FineTunes
<details><summary><code>client.fine_tunes.<a href="src/cartesia/fine_tunes/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Paginated list of all fine-tunes for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.fine_tunes.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of fine-tunes to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a fine-tune ID that defines your
place in the list. For example, if you make a /fine-tunes request and receive 20
objects, ending with `fine_tune_abc123`, your subsequent call can include
`starting_after=fine_tune_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a fine-tune ID that defines your
place in the list. For example, if you make a /fine-tunes request and receive 20
objects, starting with `fine_tune_abc123`, your subsequent call can include
`ending_before=fine_tune_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.fine_tunes.<a href="src/cartesia/fine_tunes/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new fine-tune
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.fine_tunes.create(
    name="name",
    description="description",
    language="language",
    model_id="model_id",
    dataset="dataset",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name for the new fine-tune
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — Description for the fine-tune
    
</dd>
</dl>

<dl>
<dd>

**language:** `str` — Language code for the fine-tune
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `str` — Base model ID to fine-tune from
    
</dd>
</dl>

<dl>
<dd>

**dataset:** `str` — Dataset ID containing training files
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.fine_tunes.<a href="src/cartesia/fine_tunes/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific fine-tune by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.fine_tunes.get(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the fine-tune to retrieve
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.fine_tunes.<a href="src/cartesia/fine_tunes/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a fine-tune
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.fine_tunes.delete(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the fine-tune to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.fine_tunes.<a href="src/cartesia/fine_tunes/client.py">list_voices</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all voices created from a fine-tune
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.fine_tunes.list_voices(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the fine-tune to list voices from
    
</dd>
</dl>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of voices to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a voice ID that defines your
place in the list. For example, if you make a fine-tune voices request and receive 20
objects, ending with `voice_abc123`, your subsequent call can include
`starting_after=voice_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a voice ID that defines your
place in the list. For example, if you make a fine-tune voices request and receive 20
objects, starting with `voice_abc123`, your subsequent call can include
`ending_before=voice_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Infill
<details><summary><code>client.infill.<a href="src/cartesia/infill/client.py">bytes</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Generate audio that smoothly connects two existing audio segments. This is useful for inserting new speech between existing speech segments while maintaining natural transitions.

**The cost is 1 credit per character of the infill text plus a fixed cost of 300 credits.**

Infilling is only available on `sonic-2` at this time.

At least one of `left_audio` or `right_audio` must be provided.

As with all generative models, there's some inherent variability, but here's some tips we recommend to get the best results from infill:
- Use longer infill transcripts
  - This gives the model more flexibility to adapt to the rest of the audio
- Target natural pauses in the audio when deciding where to clip
  - This means you don't need word-level timestamps to be as precise
- Clip right up to the start and end of the audio segment you want infilled, keeping as much silence in the left/right audio segments as possible
  - This helps the model generate more natural transitions
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.infill.bytes(
    model_id="sonic-2",
    language="en",
    transcript="middle segment",
    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
    output_format_container="wav",
    output_format_sample_rate=44100,
    output_format_encoding="pcm_f32le",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**left_audio:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**right_audio:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**model_id:** `str` — The ID of the model to use for generating audio
    
</dd>
</dl>

<dl>
<dd>

**language:** `str` — The language of the transcript
    
</dd>
</dl>

<dl>
<dd>

**transcript:** `str` — The infill text to generate
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` — The ID of the voice to use for generating audio
    
</dd>
</dl>

<dl>
<dd>

**output_format_container:** `OutputFormatContainer` — The format of the output audio
    
</dd>
</dl>

<dl>
<dd>

**output_format_sample_rate:** `int` — The sample rate of the output audio
    
</dd>
</dl>

<dl>
<dd>

**output_format_encoding:** `typing.Optional[RawEncoding]` — Required for `raw` and `wav` containers.
    
</dd>
</dl>

<dl>
<dd>

**output_format_bit_rate:** `typing.Optional[int]` — Required for `mp3` containers.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## PronunciationDicts
<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

List all pronunciation dictionaries for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.list()

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of dictionaries to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a dictionary ID that defines your
place in the list. For example, if you make a request and receive 20 objects, ending
with `dict_abc123`, your subsequent call can include `starting_after=dict_abc123`
to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a dictionary ID that defines your
place in the list. For example, if you make a request and receive 20 objects, starting
with `dict_abc123`, your subsequent call can include `ending_before=dict_abc123`
to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.create(
    name="name",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**name:** `str` — Name for the new pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.Optional[typing.Sequence[PronunciationDictItemParams]]` — Optional initial list of pronunciation mappings
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Retrieve a specific pronunciation dictionary by ID
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.get(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to retrieve
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update a pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.update(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to update
    
</dd>
</dl>

<dl>
<dd>

**name:** `typing.Optional[str]` — New name for the pronunciation dictionary
    
</dd>
</dl>

<dl>
<dd>

**items:** `typing.Optional[typing.Sequence[PronunciationDictItemParams]]` — Updated list of pronunciation mappings
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Delete a pronunciation dictionary
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.delete(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to delete
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">pin</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Pin a pronunciation dictionary for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.pin(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to pin
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.pronunciation_dicts.<a href="src/cartesia/pronunciation_dicts/client.py">unpin</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Unpin a pronunciation dictionary for the authenticated user
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.pronunciation_dicts.unpin(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `str` — ID of the pronunciation dictionary to unpin
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Stt
<details><summary><code>client.stt.<a href="src/cartesia/stt/client.py">transcribe</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Transcribes audio files into text using Cartesia's Speech-to-Text API.

Upload an audio file and receive a complete transcription response. Supports arbitrarily long audio files with automatic intelligent chunking for longer audio.

**Supported audio formats:** flac, m4a, mp3, mp4, mpeg, mpga, oga, ogg, wav, webm

**Response format:** Returns JSON with transcribed text, duration, and language. Include `timestamp_granularities: ["word"]` to get word-level timestamps.
 
**Pricing:** Batch transcription is priced at **1 credit per 2 seconds** of audio processed.

<Note>
For migrating from the OpenAI SDK, see our [OpenAI Whisper to Cartesia Ink Migration Guide](/api-reference/stt/migrate-from-open-ai).
</Note>
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.stt.transcribe(
    model="ink-whisper",
    language="en",
    timestamp_granularities=["word"],
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**file:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**model:** `str` — ID of the model to use for transcription. Use `ink-whisper` for the latest Cartesia Whisper model.
    
</dd>
</dl>

<dl>
<dd>

**encoding:** `typing.Optional[SttEncoding]` 

The encoding format to process the audio as. If not specified, the audio file will be decoded automatically.

**Supported formats:**
- `pcm_s16le` - 16-bit signed integer PCM, little-endian (recommended for best performance)
- `pcm_s32le` - 32-bit signed integer PCM, little-endian
- `pcm_f16le` - 16-bit floating point PCM, little-endian
- `pcm_f32le` - 32-bit floating point PCM, little-endian
- `pcm_mulaw` - 8-bit μ-law encoded PCM
- `pcm_alaw` - 8-bit A-law encoded PCM
    
</dd>
</dl>

<dl>
<dd>

**sample_rate:** `typing.Optional[int]` — The sample rate of the audio in Hz. 
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[str]` 

The language of the input audio in ISO-639-1 format. Defaults to `en`.

<Accordion title="Supported languages">
  - `en` (English)
  - `zh` (Chinese)
  - `de` (German)
  - `es` (Spanish)
  - `ru` (Russian)
  - `ko` (Korean)
  - `fr` (French)
  - `ja` (Japanese)
  - `pt` (Portuguese)
  - `tr` (Turkish)
  - `pl` (Polish)
  - `ca` (Catalan)
  - `nl` (Dutch)
  - `ar` (Arabic)
  - `sv` (Swedish)
  - `it` (Italian)
  - `id` (Indonesian)
  - `hi` (Hindi)
  - `fi` (Finnish)
  - `vi` (Vietnamese)
  - `he` (Hebrew)
  - `uk` (Ukrainian)
  - `el` (Greek)
  - `ms` (Malay)
  - `cs` (Czech)
  - `ro` (Romanian)
  - `da` (Danish)
  - `hu` (Hungarian)
  - `ta` (Tamil)
  - `no` (Norwegian)
  - `th` (Thai)
  - `ur` (Urdu)
  - `hr` (Croatian)
  - `bg` (Bulgarian)
  - `lt` (Lithuanian)
  - `la` (Latin)
  - `mi` (Maori)
  - `ml` (Malayalam)
  - `cy` (Welsh)
  - `sk` (Slovak)
  - `te` (Telugu)
  - `fa` (Persian)
  - `lv` (Latvian)
  - `bn` (Bengali)
  - `sr` (Serbian)
  - `az` (Azerbaijani)
  - `sl` (Slovenian)
  - `kn` (Kannada)
  - `et` (Estonian)
  - `mk` (Macedonian)
  - `br` (Breton)
  - `eu` (Basque)
  - `is` (Icelandic)
  - `hy` (Armenian)
  - `ne` (Nepali)
  - `mn` (Mongolian)
  - `bs` (Bosnian)
  - `kk` (Kazakh)
  - `sq` (Albanian)
  - `sw` (Swahili)
  - `gl` (Galician)
  - `mr` (Marathi)
  - `pa` (Punjabi)
  - `si` (Sinhala)
  - `km` (Khmer)
  - `sn` (Shona)
  - `yo` (Yoruba)
  - `so` (Somali)
  - `af` (Afrikaans)
  - `oc` (Occitan)
  - `ka` (Georgian)
  - `be` (Belarusian)
  - `tg` (Tajik)
  - `sd` (Sindhi)
  - `gu` (Gujarati)
  - `am` (Amharic)
  - `yi` (Yiddish)
  - `lo` (Lao)
  - `uz` (Uzbek)
  - `fo` (Faroese)
  - `ht` (Haitian Creole)
  - `ps` (Pashto)
  - `tk` (Turkmen)
  - `nn` (Nynorsk)
  - `mt` (Maltese)
  - `sa` (Sanskrit)
  - `lb` (Luxembourgish)
  - `my` (Myanmar)
  - `bo` (Tibetan)
  - `tl` (Tagalog)
  - `mg` (Malagasy)
  - `as` (Assamese)
  - `tt` (Tatar)
  - `haw` (Hawaiian)
  - `ln` (Lingala)
  - `ha` (Hausa)
  - `ba` (Bashkir)
  - `jw` (Javanese)
  - `su` (Sundanese)
  - `yue` (Cantonese)
</Accordion>
    
</dd>
</dl>

<dl>
<dd>

**timestamp_granularities:** `typing.Optional[typing.List[TimestampGranularity]]` — The timestamp granularities to populate for this transcription. Currently only `word` level timestamps are supported.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Tts
<details><summary><code>client.tts.<a href="src/cartesia/tts/client.py">bytes</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.tts.bytes(
    model_id="sonic-2",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
    language="en",
    output_format={
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
        "container": "wav",
    },
    save=True,
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-cartesia/tts-models) for available models.
    
</dd>
</dl>

<dl>
<dd>

**transcript:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `TtsRequestVoiceSpecifierParams` 
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `OutputFormatParams` 
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[SupportedLanguage]` 
    
</dd>
</dl>

<dl>
<dd>

**duration:** `typing.Optional[float]` 

The maximum duration of the audio in seconds. You do not usually need to specify this.
If the duration is not appropriate for the length of the transcript, the output audio may be truncated.
    
</dd>
</dl>

<dl>
<dd>

**speed:** `typing.Optional[ModelSpeed]` 
    
</dd>
</dl>

<dl>
<dd>

**save:** `typing.Optional[bool]` — Whether to save the generated audio file. When true, the response will include a `Cartesia-File-ID` header.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dict_ids:** `typing.Optional[typing.Sequence[str]]` — A list of pronunciation dict IDs to use for the generation. This will be applied in addition to the pinned pronunciation dict, which will be treated as the first element of the list. If there are conflicts with dict items, the latest dict will take precedence.
    
</dd>
</dl>

<dl>
<dd>

**generation_config:** `typing.Optional[GenerationConfigParams]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.tts.<a href="src/cartesia/tts/client.py">sse</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
response = client.tts.sse(
    model_id="sonic-2",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
    language="en",
    output_format={
        "container": "raw",
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
    },
    context_id="my-context-123",
)
for chunk in response:
    yield chunk

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-cartesia/tts-models) for available models.
    
</dd>
</dl>

<dl>
<dd>

**transcript:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `TtsRequestVoiceSpecifierParams` 
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `SseOutputFormatParams` 
    
</dd>
</dl>

<dl>
<dd>

**language:** `typing.Optional[SupportedLanguage]` 
    
</dd>
</dl>

<dl>
<dd>

**duration:** `typing.Optional[float]` 

The maximum duration of the audio in seconds. You do not usually need to specify this.
If the duration is not appropriate for the length of the transcript, the output audio may be truncated.
    
</dd>
</dl>

<dl>
<dd>

**speed:** `typing.Optional[ModelSpeed]` 
    
</dd>
</dl>

<dl>
<dd>

**add_timestamps:** `typing.Optional[bool]` — Whether to return word-level timestamps. If `false` (default), no word timestamps will be produced at all. If `true`, the server will return timestamp events containing word-level timing information.
    
</dd>
</dl>

<dl>
<dd>

**add_phoneme_timestamps:** `typing.Optional[bool]` — Whether to return phoneme-level timestamps. If `false` (default), no phoneme timestamps will be produced. If `true`, the server will return timestamp events containing phoneme-level timing information.
    
</dd>
</dl>

<dl>
<dd>

**use_normalized_timestamps:** `typing.Optional[bool]` — Whether to use normalized timestamps (True) or original timestamps (False).
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dict_ids:** `typing.Optional[typing.Sequence[str]]` — A list of pronunciation dict IDs to use for the generation. This will be applied in addition to the pinned pronunciation dict, which will be treated as the first element of the list. If there are conflicts with dict items, the latest dict will take precedence.
    
</dd>
</dl>

<dl>
<dd>

**context_id:** `typing.Optional[ContextId]` — Optional context ID for this request.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## VoiceChanger
<details><summary><code>client.voice_changer.<a href="src/cartesia/voice_changer/client.py">bytes</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Takes an audio file of speech, and returns an audio file of speech spoken with the same intonation, but with a different voice.

This endpoint is priced at 15 characters per second of input audio.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voice_changer.bytes(
    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
    output_format_container="raw",
    output_format_sample_rate=44100,
    output_format_encoding="pcm_f32le",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**clip:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_container:** `OutputFormatContainer` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_sample_rate:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_encoding:** `typing.Optional[RawEncoding]` — Required for `raw` and `wav` containers.
    
</dd>
</dl>

<dl>
<dd>

**output_format_bit_rate:** `typing.Optional[int]` — Required for `mp3` containers.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration. You can pass in configuration such as `chunk_size`, and more to customize the request and response.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voice_changer.<a href="src/cartesia/voice_changer/client.py">sse</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
response = client.voice_changer.sse(
    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
    output_format_container="raw",
    output_format_sample_rate=44100,
    output_format_encoding="pcm_f32le",
)
for chunk in response:
    yield chunk

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**clip:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**voice_id:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_container:** `OutputFormatContainer` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_sample_rate:** `int` 
    
</dd>
</dl>

<dl>
<dd>

**output_format_encoding:** `typing.Optional[RawEncoding]` — Required for `raw` and `wav` containers.
    
</dd>
</dl>

<dl>
<dd>

**output_format_bit_rate:** `typing.Optional[int]` — Required for `mp3` containers.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

## Voices
<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">list</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
response = client.voices.list()
for item in response:
    yield item
# alternatively, you can paginate page-by-page
for page in response.iter_pages():
    yield page

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**limit:** `typing.Optional[int]` — The number of Voices to return per page, ranging between 1 and 100.
    
</dd>
</dl>

<dl>
<dd>

**starting_after:** `typing.Optional[str]` 

A cursor to use in pagination. `starting_after` is a Voice ID that defines your
place in the list. For example, if you make a /voices request and receive 100
objects, ending with `voice_abc123`, your subsequent call can include
`starting_after=voice_abc123` to fetch the next page of the list.
    
</dd>
</dl>

<dl>
<dd>

**ending_before:** `typing.Optional[str]` 

A cursor to use in pagination. `ending_before` is a Voice ID that defines your
place in the list. For example, if you make a /voices request and receive 100
objects, starting with `voice_abc123`, your subsequent call can include
`ending_before=voice_abc123` to fetch the previous page of the list.
    
</dd>
</dl>

<dl>
<dd>

**is_owner:** `typing.Optional[bool]` — Whether to only return voices owned by the current user.
    
</dd>
</dl>

<dl>
<dd>

**is_starred:** `typing.Optional[bool]` — Whether to only return starred voices.
    
</dd>
</dl>

<dl>
<dd>

**gender:** `typing.Optional[GenderPresentation]` — The gender presentation of the voices to return.
    
</dd>
</dl>

<dl>
<dd>

**expand:** `typing.Optional[typing.Sequence[VoiceExpandOptions]]` — Additional fields to include in the response.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">clone</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Clone a high similarity voice from an audio clip. Clones are more similar to the source clip, but may reproduce background noise. For these, use an audio clip about 5 seconds long.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voices.clone(
    name="A high-similarity cloned voice",
    description="Copied from Cartesia docs",
    language="en",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**clip:** `from __future__ import annotations

core.File` — See core.File for more documentation
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the voice.
    
</dd>
</dl>

<dl>
<dd>

**language:** `SupportedLanguage` — The language of the voice.
    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — A description for the voice.
    
</dd>
</dl>

<dl>
<dd>

**enhance:** `typing.Optional[bool]` — Whether to apply AI enhancements to the clip to reduce background noise. This is not recommended unless the source clip is extremely low quality.
    
</dd>
</dl>

<dl>
<dd>

**base_voice_id:** `typing.Optional[VoiceId]` — Optional base voice ID that the cloned voice is derived from.
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">delete</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voices.delete(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `VoiceId` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">update</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Update the name, description, and gender of a voice. To set the gender back to the default, set the gender to `null`. If gender is not specified, the gender will not be updated.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voices.update(
    id="8f7d3c2e-1a2b-3c4d-5e6f-7g8h9i0j1k2l",
    name="Sarah Peninsular Spanish",
    description="Sarah Voice in Peninsular Spanish",
    gender="feminine",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `VoiceId` 
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the voice.
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — The description of the voice.
    
</dd>
</dl>

<dl>
<dd>

**gender:** `typing.Optional[GenderPresentation]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">get</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voices.get(
    id="id",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**id:** `VoiceId` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">localize</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create a new voice from an existing voice localized to a new language and dialect.
</dd>
</dl>
</dd>
</dl>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    token="YOUR_TOKEN",
)
client.voices.localize(
    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
    name="Sarah Peninsular Spanish",
    description="Sarah Voice in Peninsular Spanish",
    language="es",
    original_speaker_gender="female",
    dialect="pe",
)

```
</dd>
</dl>
</dd>
</dl>

#### ⚙️ Parameters

<dl>
<dd>

<dl>
<dd>

**voice_id:** `str` — The ID of the voice to localize.
    
</dd>
</dl>

<dl>
<dd>

**name:** `str` — The name of the new localized voice.
    
</dd>
</dl>

<dl>
<dd>

**description:** `str` — The description of the new localized voice.
    
</dd>
</dl>

<dl>
<dd>

**language:** `LocalizeTargetLanguage` 
    
</dd>
</dl>

<dl>
<dd>

**original_speaker_gender:** `Gender` 
    
</dd>
</dl>

<dl>
<dd>

**dialect:** `typing.Optional[LocalizeDialectParams]` 
    
</dd>
</dl>

<dl>
<dd>

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
</dd>
</dl>
</dd>
</dl>


</dd>
</dl>
</details>

