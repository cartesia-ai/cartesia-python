# Cartesia Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-Built%20with%20Fern-brightgreen)](https://buildwithfern.com?utm_source=github&utm_medium=github&utm_campaign=readme&utm_source=https%3A%2F%2Fgithub.com%2Fcartesia-ai%2Fcartesia-python)
[![pypi](https://img.shields.io/pypi/v/cartesia)](https://pypi.python.org/pypi/cartesia)

The Cartesia Python library provides convenient access to the Cartesia API from Python.

## Documentation

Our complete API documentation can be found [on docs.cartesia.ai](https://docs.cartesia.ai).

## Installation

```sh
pip install cartesia
```

## Usage

Instantiate and use the client with the following:

```python
from cartesia import Cartesia
from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier
import os

client = Cartesia(
    api_key=os.getenv("CARTESIA_API_KEY"),
)
client.tts.bytes(
    model_id="sonic-2",
    transcript="Hello, world!",
    voice={
        "mode": "id",
        "id": "694f9389-aac1-45b6-b726-9d9369183238",
    },
    language="en",
    output_format={
        "container": "raw",
        "sample_rate": 44100,
        "encoding": "pcm_f32le",
    },
)
```

## Async Client

The SDK also exports an `async` client so that you can make non-blocking calls to our API.

```python
import asyncio
import os

from cartesia import AsyncCartesia
from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier

client = AsyncCartesia(
    api_key=os.getenv("CARTESIA_API_KEY"),
)

async def main() -> None:
    async for output in client.tts.bytes(
        model_id="sonic-2",
        transcript="Hello, world!",
        voice={"id": "694f9389-aac1-45b6-b726-9d9369183238"},
        language="en",
        output_format={
            "container": "raw",
            "sample_rate": 44100,
            "encoding": "pcm_f32le",
        },
    ):
        print(f"Received chunk of size: {len(output)}")


asyncio.run(main())
```

## Exception Handling

When the API returns a non-success status code (4xx or 5xx response), a subclass of the following error
will be thrown.

```python
from cartesia.core.api_error import ApiError

try:
    client.tts.bytes(...)
except ApiError as e:
    print(e.status_code)
    print(e.body)
```

## Streaming

The SDK supports streaming responses as well, returning a generator that you can iterate over with a `for ... in ...` loop:

```python
from cartesia import Cartesia
from cartesia.tts import Controls, OutputFormat_RawParams, TtsRequestIdSpecifierParams
import os

def get_tts_chunks():
    client = Cartesia(
        api_key=os.getenv("CARTESIA_API_KEY"),
    )
    response = client.tts.sse(
        model_id="sonic-2",
        transcript="Hello world!",
        voice={
            "id": "f9836c6e-a0bd-460e-9d3c-f7299fa60f94",
            "experimental_controls": {
                "speed": "normal",
                "emotion": [],
            },
        },
        language="en",
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
    )

    audio_chunks = []
    for chunk in response:
        audio_chunks.append(chunk)
    return audio_chunks

chunks = get_tts_chunks()
for chunk in chunks:
    print(f"Received chunk of size: {len(chunk.data)}")
```

## WebSockets

For the lowest latency in advanced usecases (such as streaming in an LLM-generated transcript and streaming out audio), you should use our websockets client:

```python
from cartesia import Cartesia
from cartesia.tts import TtsRequestEmbeddingSpecifierParams, OutputFormat_RawParams
import pyaudio
import os

client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
transcript = "Hello! Welcome to Cartesia"

p = pyaudio.PyAudio()
rate = 22050

stream = None

# Set up the websocket connection
ws = client.tts.websocket()

# Generate and stream audio using the websocket
for output in ws.send(
    model_id="sonic-2", # see: https://docs.cartesia.ai/getting-started/available-models
    transcript=transcript,
    voice={"id": voice_id},
    stream=True,
    output_format={
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": rate
    },
):
    buffer = output.audio

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()

ws.close()  # Close the websocket connection
```

## Speech-to-Text (STT) with Websockets

```python
from cartesia import Cartesia
import os

client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))

# Load your audio file as bytes
with open("path/to/audio.wav", "rb") as f:
    audio_data = f.read()

# Convert to audio chunks (20ms chunks used here for a streaming example)
# This chunk size is calculated for 16kHz, 16-bit audio: 16000 * 0.02 * 2 = 640 bytes
chunk_size = 640
audio_chunks = [audio_data[i:i+chunk_size] for i in range(0, len(audio_data), chunk_size)]

# Create websocket connection with endpointing parameters
ws = client.stt.websocket(
    model="ink-whisper",                 # Model (required)
    language="en",                       # Language of your audio (required)
    encoding="pcm_s16le",                # Audio encoding format (required)
    sample_rate=16000,                   # Audio sample rate (required)
    min_volume=0.1,                      # Volume threshold for voice activity detection
    max_silence_duration_secs=0.4,       # Maximum silence duration before endpointing
)

# Send audio chunks (streaming approach)
for chunk in audio_chunks:
    ws.send(chunk)

# Finalize and close
ws.send("finalize")
ws.send("done")

# Receive transcription results with word-level timestamps
for result in ws.receive():
    if result['type'] == 'transcript':
        print(f"Transcription: {result['text']}")
        
        # Handle word-level timestamps if available
        if 'words' in result and result['words']:
            print("Word-level timestamps:")
            for word_info in result['words']:
                word = word_info['word']
                start = word_info['start']
                end = word_info['end']
                print(f"  '{word}': {start:.2f}s - {end:.2f}s")
        
        if result['is_final']:
            print("Final result received")
    elif result['type'] == 'done':
        break

ws.close()
```

### Async Streaming Speech-to-Text (STT) with Websockets

For real-time streaming applications, here's a more practical async example that demonstrates concurrent audio processing and result handling:

```python
import asyncio
import os
from cartesia import AsyncCartesia

async def streaming_stt_example():
    """
    Advanced async STT example for real-time streaming applications.
    This example simulates streaming audio processing with proper error handling
    and demonstrates the new endpointing and word timestamp features.
    """
    client = AsyncCartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    
    try:
        # Create websocket connection with voice activity detection
        ws = await client.stt.websocket(
            model="ink-whisper",             # Model (required)
            language="en",                   # Language of your audio (required)
            encoding="pcm_s16le",            # Audio encoding format (required)
            sample_rate=16000,               # Audio sample rate (required)
            min_volume=0.15,                 # Volume threshold for voice activity detection
            max_silence_duration_secs=0.3,   # Maximum silence duration before endpointing
        )
        
        # Simulate streaming audio data (replace with your audio source)
        async def audio_stream():
            """Simulate real-time audio streaming - replace with actual audio capture"""
            # Load audio file for simulation
            with open("path/to/audio.wav", "rb") as f:
                audio_data = f.read()
            
            # Stream in 100ms chunks (realistic for real-time processing)
            chunk_size = int(16000 * 0.1 * 2)  # 100ms at 16kHz, 16-bit
            
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                if chunk:
                    yield chunk
                    # Simulate real-time streaming delay
                    await asyncio.sleep(0.1)
        
        # Send audio and receive results concurrently
        async def send_audio():
            """Send audio chunks to the STT websocket"""
            try:
                async for chunk in audio_stream():
                    await ws.send(chunk)
                    print(f"Sent audio chunk of {len(chunk)} bytes")
                    # Small delay to simulate realtime applications
                    await asyncio.sleep(0.02)
                
                # Signal end of audio stream
                await ws.send("finalize")
                await ws.send("done")
                print("Audio streaming completed")
                
            except Exception as e:
                print(f"Error sending audio: {e}")
        
        async def receive_transcripts():
            """Receive and process transcription results with word timestamps"""
            full_transcript = ""
            all_word_timestamps = []
            
            try:
                async for result in ws.receive():
                    if result['type'] == 'transcript':
                        text = result['text']
                        is_final = result['is_final']
                        
                        # Handle word-level timestamps
                        if 'words' in result and result['words']:
                            word_timestamps = result['words']
                            all_word_timestamps.extend(word_timestamps)
                            
                            if is_final:
                                print("Word-level timestamps:")
                                for word_info in word_timestamps:
                                    word = word_info['word']
                                    start = word_info['start']
                                    end = word_info['end']
                                    print(f"  '{word}': {start:.2f}s - {end:.2f}s")
                        
                        if is_final:
                            # Final result - this text won't change
                            full_transcript += text + " "
                            print(f"FINAL: {text}")
                        else:
                            # Partial result - may change as more audio is processed
                            print(f"PARTIAL: {text}")
                            
                    elif result['type'] == 'done':
                        print("Transcription completed")
                        break
                        
            except Exception as e:
                print(f"Error receiving transcripts: {e}")
            
            return full_transcript.strip(), all_word_timestamps
        
        print("Starting streaming STT...")
        
        # Use asyncio.gather to run audio sending and transcript receiving concurrently
        _, (final_transcript, word_timestamps) = await asyncio.gather(
            send_audio(),
            receive_transcripts()
        )
        
        print(f"\nComplete transcript: {final_transcript}")
        print(f"Total words with timestamps: {len(word_timestamps)}")
        
        # Clean up
        await ws.close()
        
    except Exception as e:
        print(f"STT streaming error: {e}")
    finally:
        await client.close()

# Run the example
if __name__ == "__main__":
    asyncio.run(streaming_stt_example())
```

## Batch Speech-to-Text (STT)

For processing pre-recorded audio files, use the batch STT API which supports uploading complete audio files for transcription:

```python
from cartesia import Cartesia
import os

client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))

# Transcribe an audio file with word-level timestamps
with open("path/to/audio.wav", "rb") as audio_file:
    response = client.stt.transcribe(
        file=audio_file,                    # Audio file to transcribe
        model="ink-whisper",                # STT model (required)
        language="en",                      # Language of the audio (optional)
        timestamp_granularities=["word"],   # Include word-level timestamps (optional)
        encoding="pcm_s16le",               # Audio encoding (optional)
        sample_rate=16000,                  # Audio sample rate (optional)
    )

# Access transcription results
print(f"Transcribed text: {response.text}")
print(f"Audio duration: {response.duration:.2f} seconds")

# Process word-level timestamps if requested
if response.words:
    print("\nWord-level timestamps:")
    for word_info in response.words:
        word = word_info.word
        start = word_info.start
        end = word_info.end
        print(f"  '{word}': {start:.2f}s - {end:.2f}s")
```

### Async Batch STT

```python
import asyncio
from cartesia import AsyncCartesia
import os

async def transcribe_file():
    client = AsyncCartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    
    with open("path/to/audio.wav", "rb") as audio_file:
        response = await client.stt.transcribe(
            file=audio_file,
            model="ink-whisper",
            language="en",
            timestamp_granularities=["word"],
        )
    
    print(f"Transcribed text: {response.text}")
    
    # Process word timestamps
    if response.words:
        for word_info in response.words:
            print(f"'{word_info.word}': {word_info.start:.2f}s - {word_info.end:.2f}s")
    
    await client.close()

asyncio.run(transcribe_file())
```

> **Note:** Batch STT also supports OpenAI's audio transcriptions format for easy migration from OpenAI Whisper. See our [migration guide](https://docs.cartesia.ai/api-reference/stt/migrate-from-open-ai) for details.

## Voices

List all available Voices with `client.voices.list`, which returns an iterable that automatically handles pagination:

```python
from cartesia import Cartesia
import os

client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))

# Get all available Voices
voices = client.voices.list()
for voice in voices:
    print(voice)
```

You can also get the complete metadata for a specific Voice, or make a new Voice by cloning from an audio sample:

```python
# Get a specific Voice
voice = client.voices.get(id="a0e99841-438c-4a64-b679-ae501e7d6091")
print("The embedding for", voice.name, "is", voice.embedding)

# Clone a Voice using file data
cloned_voice = client.voices.clone(
    clip=open("path/to/voice.wav", "rb"),
    name="Test cloned voice",
    language="en",
    mode="similarity",  # or "stability"
    enhance=False, # use enhance=True to clean and denoise the cloning audio
    description="Test voice description"
)
```

## Requesting Timestamps

```python
import asyncio
from cartesia import AsyncCartesia
import os

async def main():
    client = AsyncCartesia(api_key=os.getenv("CARTESIA_API_KEY"))

    # Connect to the websocket
    ws = await client.tts.websocket()

    # Generate speech with timestamps
    output_generate = await ws.send(
        model_id="sonic-2",
        transcript="Hello! Welcome to Cartesia's text-to-speech.",
        voice={"id": "f9836c6e-a0bd-460e-9d3c-f7299fa60f94"},
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
        },
        add_timestamps=True,            # Enable word-level timestamps
        add_phoneme_timestamps=True,    # Enable phonemized timestamps
        stream=True
    )

    # Process the streaming response with timestamps
    all_words = []
    all_starts = []
    all_ends = []
    audio_chunks = []

    async for out in output_generate:
        # Collect audio data
        if out.audio is not None:
            audio_chunks.append(out.audio)

        # Process timestamp data
        if out.word_timestamps is not None:
            all_words.extend(out.word_timestamps.words)    # List of words
            all_starts.extend(out.word_timestamps.start)   # Start time for each word (seconds)
            all_ends.extend(out.word_timestamps.end)       # End time for each word (seconds)

    await ws.close()
    await client.close()

asyncio.run(main())
```

## Advanced

### Retries

The SDK is instrumented with automatic retries with exponential backoff. A request will be retried as long
as the request is deemed retriable and the number of retry attempts has not grown larger than the configured
retry limit (default: 2).

A request is deemed retriable when any of the following HTTP status codes is returned:

- [408](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/408) (Timeout)
- [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429) (Too Many Requests)
- [5XX](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500) (Internal Server Errors)

Use the `max_retries` request option to configure this behavior.

```python
client.tts.bytes(..., request_options={
    "max_retries": 1
})
```

### Timeouts

The SDK defaults to a 60 second timeout. You can configure this with a timeout option at the client or request level.

```python

from cartesia import Cartesia

client = Cartesia(
    ...,
    timeout=20.0,
)


# Override timeout for a specific method
client.tts.bytes(..., request_options={
    "timeout_in_seconds": 1
})
```

### Mixing voices and creating from embeddings

```python
# Mix voices together
mixed_voice = client.voices.mix(
    voices=[
        {"id": "voice_id_1", "weight": 0.25},
        {"id": "voice_id_2", "weight": 0.75}
    ]
)

# Create a new voice from embedding
new_voice = client.voices.create(
    name="Test Voice",
    description="Test voice description",
    embedding=[...],  # List[float] with 192 dimensions
    language="en"
)
```
### Custom Client

You can override the `httpx` client to customize it for your use-case. Some common use-cases include support for proxies
and transports.
```python
import httpx
from cartesia import Cartesia

client = Cartesia(
    ...,
    httpx_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Reference

A full reference for this library is available [here](./reference.md).

## Contributing

Note that most of this library is generated programmatically from
<https://github.com/cartesia-ai/docs> — before making edits to a file, verify it's not autogenerated
by checking for this comment at the top of the file:

```
# This file was auto-generated by Fern from our API Definition.
```

### Running tests

```sh
uv pip install -r requirements.txt
uv run pytest -rP -vv tests/custom/test_client.py::test_get_voices
```
### Manually generating SDK code from docs

Assuming all your repos are cloned into your home directory:

```sh
$ cd ~/docs
$ fern generate --group python-sdk --log-level debug --api version-2024-11-13 --preview
$ cd ~/cartesia-python
$ git pull ~/docs/fern/apis/version-2024-11-13/.preview/fern-python-sdk
$ git commit --amend -m "manually regenerate from docs" # optional
```

### Automatically generating new SDK releases

From https://github.com/cartesia-ai/docs click `Actions` then `Release Python SDK`. (Requires permissions.)



