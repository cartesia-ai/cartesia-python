# Reference
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
    api_key_header="YOUR_API_KEY_HEADER",
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
from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier

client = Cartesia(
    api_key_header="YOUR_API_KEY_HEADER",
)
client.tts.bytes(
    model_id="sonic-english",
    transcript="Hello, world!",
    voice=TtsRequestIdSpecifier(
        id="694f9389-aac1-45b6-b726-9d9369183238",
    ),
    language="en",
    output_format=OutputFormat_Raw(
        sample_rate=44100,
        encoding="pcm_f32le",
    ),
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

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-sonic/models) for available models.
    
</dd>
</dl>

<dl>
<dd>

**transcript:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `TtsRequestVoiceSpecifier` 
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `OutputFormat` 
    
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
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
from cartesia.tts import Controls, OutputFormat_Raw, TtsRequestIdSpecifier

client = Cartesia(
    api_key_header="YOUR_API_KEY_HEADER",
)
response = client.tts.sse(
    model_id="string",
    transcript="string",
    voice=TtsRequestIdSpecifier(
        id="string",
        experimental_controls=Controls(
            speed=1.1,
            emotion="anger:lowest",
        ),
    ),
    language="en",
    output_format=OutputFormat_Raw(),
    duration=1.1,
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

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-sonic/models) for available models.
    
</dd>
</dl>

<dl>
<dd>

**transcript:** `str` 
    
</dd>
</dl>

<dl>
<dd>

**voice:** `TtsRequestVoiceSpecifier` 
    
</dd>
</dl>

<dl>
<dd>

**output_format:** `OutputFormat` 
    
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
    api_key_header="YOUR_API_KEY_HEADER",
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

**request_options:** `typing.Optional[RequestOptions]` — Request-specific configuration.
    
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
    api_key_header="YOUR_API_KEY_HEADER",
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
<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">list</a>()</code></summary>
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
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.list()

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

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">create</a>(...)</code></summary>
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
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.create(
    name="string",
    description="string",
    embedding=[
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ],
    language="en",
    base_voice_id="string",
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

**embedding:** `Embedding` 
    
</dd>
</dl>

<dl>
<dd>

**language:** `SupportedLanguage` 
    
</dd>
</dl>

<dl>
<dd>

**base_voice_id:** `typing.Optional[BaseVoiceId]` 
    
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
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.delete(
    id="string",
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.update(
    id="string",
    name="string",
    description="string",
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
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.get(
    id="string",
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.localize(
    embedding=[
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
    ],
    language="en",
    original_speaker_gender="male",
    dialect="au",
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

**embedding:** `Embedding` 
    
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

**dialect:** `LocalizeDialect` 
    
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

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">mix</a>(...)</code></summary>
<dl>
<dd>

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia
from cartesia.voices import IdSpecifier

client = Cartesia(
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.mix(
    voices=[
        IdSpecifier(
            id="string",
            weight=1.1,
        )
    ],
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

**voices:** `typing.Sequence[MixVoiceSpecifier]` 
    
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

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">clone_from_clip</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Clone a voice from a clip. The clip should be a 15-20 second recording of a person speaking with little to no background noise.

The endpoint will return an embedding that can either be used directly with text-to-speech endpoints or used to create a new voice.
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
    api_key_header="YOUR_API_KEY_HEADER",
)
client.voices.clone_from_clip()

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

**enhance:** `bool` — Whether to enhance the clip to improve its quality before cloning. Useful if the clip is low quality.

    
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

