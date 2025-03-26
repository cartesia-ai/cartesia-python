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
