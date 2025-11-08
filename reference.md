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
    api_key="YOUR_API_KEY",
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
    api_key="YOUR_API_KEY",
)
client.infill.bytes(
    model_id="sonic-2",
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

**output_format_sample_rate:** `int` — The sample rate of the output audio in Hz. Supported sample rates are 8000, 16000, 22050, 24000, 44100, 48000.
    
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
    api_key="YOUR_API_KEY",
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
    api_key="YOUR_API_KEY",
)
client.tts.bytes(
    model_id="sonic-2",
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

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.
    
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

**generation_config:** `typing.Optional[GenerationConfigParams]` 
    
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

**pronunciation_dict_id:** `typing.Optional[str]` — A pronunciation dict ID to use for the generation. This will be applied to this TTS generation only.
    
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
    model_id="sonic-2",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "694f9389-aac1-45b6-b726-9d9369183238"},
    language="en",
    output_format={
        "container": "raw",
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
    },
    add_timestamps=True,
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

**model_id:** `str` — The ID of the model to use for the generation. See [Models](/build-with-cartesia/models) for available models.
    
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

**generation_config:** `typing.Optional[GenerationConfigParams]` 
    
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

**add_phoneme_timestamps:** `typing.Optional[bool]` — Whether to return phoneme-level timestamps. If `false` (default), no phoneme timestamps will be produced - if `add_timestamps` is `true`, the produced timestamps will be word timestamps instead. If `true`, the server will return timestamp events containing phoneme-level timing information.
    
</dd>
</dl>

<dl>
<dd>

**use_normalized_timestamps:** `typing.Optional[bool]` — Whether to use normalized timestamps (True) or original timestamps (False).
    
</dd>
</dl>

<dl>
<dd>

**context_id:** `typing.Optional[ContextId]` — Optional context ID for this request.
    
</dd>
</dl>

<dl>
<dd>

**pronunciation_dict_id:** `typing.Optional[str]` — A pronunciation dict ID to use for the generation. This will be applied to this TTS generation only.
    
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

**output_format_sample_rate:** `int` — The sample rate of the output audio in Hz. Supported sample rates are 8000, 16000, 22050, 24000, 44100, 48000.
    
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
    api_key="YOUR_API_KEY",
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

**description:** `typing.Optional[str]` — A description for the voice.
    
</dd>
</dl>

<dl>
<dd>

**enhance:** `typing.Optional[bool]` — Whether to apply AI enhancements to the clip to reduce background noise. This leads to cleaner generated speech at the cost of reduced similarity to the source clip.
    
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
    api_key="YOUR_API_KEY",
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
    name="name",
    description="description",
    embedding=[1.1, 1.1],
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

