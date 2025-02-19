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
    api_key="YOUR_API_KEY",
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

## Datasets
<details><summary><code>client.datasets.<a href="src/cartesia/datasets/client.py">list</a>()</code></summary>
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
    api_key="YOUR_API_KEY",
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key="YOUR_API_KEY",
)
client.datasets.create(
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

**name:** `str` 
    
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key="YOUR_API_KEY",
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

**id:** `str` 
    
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

Only the `sonic-preview` model is supported for infill at this time.

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
    api_key="YOUR_API_KEY",
)
client.infill.bytes(
    model_id="sonic-preview",
    language="en",
    transcript="middle segment",
    voice_id="694f9389-aac1-45b6-b726-9d9369183238",
    output_format_container="wav",
    output_format_sample_rate=44100,
    output_format_encoding="pcm_f32le",
    voice_experimental_controls_speed="slowest",
    voice_experimental_controls_emotion=["surprise:high", "curiosity:high"],
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

**voice_experimental_controls_speed:** `typing.Optional[Speed]` 

Either a number between -1.0 and 1.0 or a natural language description of speed.

If you specify a number, 0.0 is the default speed, -1.0 is the slowest speed, and 1.0 is the fastest speed.

    
</dd>
</dl>

<dl>
<dd>

**voice_experimental_controls_emotion:** `typing.Optional[typing.List[Emotion]]` 

An array of emotion:level tags.

Supported emotions are: anger, positivity, surprise, sadness, and curiosity.

Supported levels are: lowest, low, (omit), high, highest.

    
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
    api_key="YOUR_API_KEY",
)
client.tts.bytes(
    model_id="sonic",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
    language="en",
    output_format={
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
        "container": "raw",
    },
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
    api_key="YOUR_API_KEY",
)
response = client.tts.sse(
    model_id="sonic",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
    language="en",
    output_format={
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
        "container": "raw",
    },
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
    api_key="YOUR_API_KEY",
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
    api_key="YOUR_API_KEY",
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
    api_key="YOUR_API_KEY",
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

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">clone</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Clone a voice from an audio clip. This endpoint has two modes, stability and similarity.

Similarity mode clones are more similar to the source clip, but may reproduce background noise. For these, use an audio clip about 5 seconds long.

Stability mode clones are more stable, but may not sound as similar to the source clip. For these, use an audio clip 10-20 seconds long.
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
    api_key="YOUR_API_KEY",
)
client.voices.clone(
    name="A high-similarity cloned voice",
    description="Copied from Cartesia docs",
    mode="similarity",
    language="en",
    transcript="A transcript of the words spoken in the audio clip.",
    enhance=False,
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

**mode:** `CloneMode` — Tradeoff between similarity and stability. Similarity clones sound more like the source clip, but may reproduce background noise. Stability clones always sound like a studio recording, but may not sound as similar to the source clip.

    
</dd>
</dl>

<dl>
<dd>

**enhance:** `bool` — Whether to enhance the clip to improve its quality before cloning. Useful if the clip has background noise.

    
</dd>
</dl>

<dl>
<dd>

**description:** `typing.Optional[str]` — A description for the voice.

    
</dd>
</dl>

<dl>
<dd>

**transcript:** `typing.Optional[str]` — Optional transcript of the words spoken in the audio clip. Only used for similarity mode.

    
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
    api_key="YOUR_API_KEY",
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key="YOUR_API_KEY",
)
client.voices.update(
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
    api_key="YOUR_API_KEY",
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

#### 🔌 Usage

<dl>
<dd>

<dl>
<dd>

```python
from cartesia import Cartesia

client = Cartesia(
    api_key="YOUR_API_KEY",
)
client.voices.localize(
    embedding=[1.1, 1.1],
    language="en",
    original_speaker_gender="male",
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

client = Cartesia(
    api_key="YOUR_API_KEY",
)
client.voices.mix(
    voices=[{"id": "id", "weight": 1.1}, {"id": "id", "weight": 1.1}],
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

**voices:** `typing.Sequence[MixVoiceSpecifierParams]` 
    
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

<details><summary><code>client.voices.<a href="src/cartesia/voices/client.py">create</a>(...)</code></summary>
<dl>
<dd>

#### 📝 Description

<dl>
<dd>

<dl>
<dd>

Create voice from raw features. If you'd like to clone a voice from an audio file, please use Clone Voice instead.
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
    api_key="YOUR_API_KEY",
)
client.voices.create(
    name="My Custom Voice",
    description="A custom voice created through the API",
    embedding=[],
    language="en",
    base_voice_id="123e4567-e89b-12d3-a456-426614174000",
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

**language:** `typing.Optional[SupportedLanguage]` 
    
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

