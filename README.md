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

## Reference

A full reference for this library is available [here](./reference.md).

## Voices

```python
from cartesia import Cartesia
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

# Get all available voices
voices = client.voices.list()
print(voices)

# Get a specific voice
voice = client.voices.get(id="a0e99841-438c-4a64-b679-ae501e7d6091")
print("The embedding for", voice["name"], "is", voice["embedding"])

# Clone a voice using filepath
cloned_voice_embedding = client.voices.clone(filepath="path/to/voice")

# Mix voices together
mixed_voice_embedding = client.voices.mix(
    [{ "id": "voice_id_1", "weight": 0.5 }, { "id": "voice_id_2", "weight": 0.25 }, { "id": "voice_id_3", "weight": 0.25 }]
)

# Create a new voice
new_voice = client.voices.create(
    name="New Voice",
    description="A clone of my own voice",
    embedding=cloned_voice_embedding,
)
```

## Usage

Instantiate and use the client with the following:

```python
from cartesia import Cartesia
from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier

client = Cartesia(
    api_key="YOUR_API_KEY",
)
client.tts.bytes(
    model_id="sonic-english",
    transcript="Hello, world!",
    voice={"id": "694f9389-aac1-45b6-b726-9d9369183238"},
    ),
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

from cartesia import AsyncCartesia
from cartesia.tts import OutputFormat_Raw, TtsRequestIdSpecifier

client = AsyncCartesia(
    api_key="YOUR_API_KEY",
)


async def main() -> None:
    await client.tts.bytes(
        model_id="sonic-english",
        transcript="Hello, world!",
        voice={"id": "694f9389-aac1-45b6-b726-9d9369183238"},
        language="en",
        output_format={
            "container": "raw",
            "sample_rate": 44100,
            "encoding": "pcm_f32le",
        },
    )


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

The SDK supports streaming responses, as well, the response will be a generator that you can loop over.

```python
from cartesia import Cartesia
from cartesia.tts import Controls, OutputFormat_RawParams, TtsRequestIdSpecifierParams

client = Cartesia(
    api_key="YOUR_API_KEY",
)
response = client.tts.sse(
    model_id="string",
    transcript="string",
    voice={
        "id": "string",
        "experimental_controls": {
            speed=1.1,
            emotion="anger:lowest",
        },
    },
    language="en",
    output_format={},
    duration=1.1,
)
for chunk in response:
    yield chunk
```

## WebSocket

```python
from cartesia import Cartesia
from cartesia.tts import TtsRequestEmbeddingSpecifierParams, OutputFormat_RawParams
import pyaudio

client = Cartesia(
    api_key="YOUR_API_KEY",
)
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
voice = client.voices.get(id=voice_id)
transcript = "Hello! Welcome to Cartesia"

# You can check out our models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-english"

p = pyaudio.PyAudio()
rate = 22050

stream = None

# Set up the websocket connection
ws = client.tts.websocket()

# Generate and stream audio using the websocket
for output in ws.send(
    model_id=model_id,
    transcript=transcript,
    voice={"embedding": voice.embedding},
    stream=True,
    output_format={
        "container": "raw",
        "encoding": "pcm_f32le", 
        "sample_rate": 22050
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

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically.
Additions made directly to this library would have to be moved over to our generation code,
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
a proof of concept, but know that we will not be able to merge it as-is. We suggest opening
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
