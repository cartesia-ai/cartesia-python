# Migrating from Cartesia Python SDK v2.x to v3.x

This guide covers the breaking changes and new patterns when upgrading from the Cartesia Python SDK v2.x to v3.x.

## Installation

```bash
# Install the base SDK
pip install cartesia==3.0.0

# For WebSocket support
pip install "cartesia[websockets]==3.0.0"
```

## TTS Bytes (Batch Generation)

For backwards compatibility, `client.tts.bytes()` is included in the v3 SDK, but
it also includes a new `.generate()` method with better type safety and response
helpers such as `.write_to_file`.

### Basic Usage

```python
# v2.x
output = client.tts.bytes(
    model_id="sonic-3",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
)
with open("output.wav", "wb") as f:
    for chunk in output:
        f.write(chunk)

# v3.x
response = client.tts.generate(
    model_id="sonic-3",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
)
response.write_to_file("output.wav")
```

### Async Usage

```python
# v2.x
async with AsyncCartesia() as client:
    with open("output.wav", "wb") as f:
        async for chunk in client.tts.bytes(...):
            f.write(chunk)

# v3.x
async with AsyncCartesia() as client:
    response = await client.tts.generate(...)
    await response.write_to_file("output.wav")
```

## TTS SSE (Server-Sent Events)

The v3.x SDK automatically decodes the base64-encoded `event.audio`.

```python
# v2.x
import base64

stream = client.tts.sse(
    model_id="sonic-3",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
)

chunks = []
for event in stream:
    if event.type == "chunk":
        audio_bytes = base64.b64decode(event.data)
        chunks.append(audio_bytes)
    elif event.type == "done":
        break

# v3.x
stream = client.tts.generate_sse(
    model_id="sonic-3",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
)

chunks = []
for event in stream:
    if event.type == "chunk":
        chunks.append(event.audio) # v3.x puts decoded bytes in event.audio
    elif event.type == "done":
        break
```

The 3.x SDK also aliases `.sse()` to `.generate_sse()` for backwards compatibility.

## TTS WebSocket

You can now call `client.tts.websocket_connect()` to get a Python context that
automatically closes the websocket.

### Basic Usage

```python
# v2.x
ws = client.tts.websocket()
output = ws.send(
    model_id="sonic-3",
    transcript="Hello, world!",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    stream=True,  # v2.x had stream parameter
)
# Write chunks to file as they arrive.
# You could also send chunks over the network, play them in real-time, etc.
with open("output.pcm", "wb") as f:
    for out in output:
        if out.audio:
            f.write(out.audio)
ws.close()

# v3.x
with client.tts.websocket_connect() as ws:
    ws.send({
        "model_id": "sonic-3",
        "transcript": "Hello, world!",
        "voice": {"mode": "id", "id": "voice-id"},
        "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    })

    # Write chunks to file as they arrive.
    # You could also send chunks over the network, play them in real-time, etc.
    with open("output.pcm", "wb") as f:
        for response in ws:
            if response.type == "chunk":
                f.write(response.audio)
```

### Continuations (Streaming Multiple Transcripts)

```python
# v2.x
ws = client.tts.websocket()
ctx = ws.context()
for transcript in transcripts:
    ctx.send(
        model_id="sonic-3",
        transcript=transcript,
        voice={"mode": "id", "id": "voice-id"},
        output_format=output_format,
        continue_=True,
    )
ctx.no_more_inputs()
with open("output.raw", "wb") as f:
    for out in ctx.receive():
        f.write(out.audio)
ws.close()

# v3.x
with client.tts.websocket_connect() as connection:
    ctx = connection.context()

    for transcript in transcripts:
        ctx.send(
            model_id="sonic-3",
            transcript=transcript,
            voice={"mode": "id", "id": "voice-id"},
            output_format=output_format,
            continue_=True,
        )

    ctx.no_more_inputs()

    # Write chunks to file as they arrive.
    # You could also send chunks over the network, play them in real-time, etc.
    with open("output.raw", "wb") as f:
        for response in ctx.receive():
            if response.type == "chunk" and response.audio:
                f.write(response.audio)
```

## Voices API





### Creating Voices

**Breaking Change:** v3.x no longer supports creating voices from embeddings. Use `clone()` with an audio clip instead.

```python
# v2.x - Create from embedding
voice = client.voices.create(
    name="My Voice",
    description="A custom voice",
    embedding=[1.0] * 192,  # 192-dimensional embedding
    language="en",
)

# v3.x - Clone from audio clip
with open("sample.wav", "rb") as clip:
    voice = client.voices.clone(
        clip=clip,
        name="My Voice",
        description="A custom voice",
        language="en",
    )
```





### Mixing Voices

**Breaking Change:** v3.x no longer supports creating voices by mixing.

```python
# v2.x, deprecated in v3.x
output = client.voices.mix(
    voices=[
        {"id": "voice-1", "weight": 0.5},
        {"id": "voice-2", "weight": 0.5},
    ]
)
```

## Infill API

The infill API remains at `client.tts.infill()` but with `left_audio` and
`right_audio` parameters, which can be audio file paths or audio bytes.

```python
# v2.x
infill_audio, total_audio = client.tts.infill(
    model_id="sonic-3",
    language="en",
    transcript="Infill text",
    left_audio_path="left.wav",
    right_audio_path="right.wav",
    voice={"mode": "id", "id": "voice-id"},
    output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
)

# v3.x
response = client.tts.infill(
    model_id="sonic-3",
    language="en",
    transcript="Infill text",
    left_audio="left.wav",   # left_audio and right_audio can be file paths or
    right_audio="right.wav", # raw audio file bytes.
    voice_id="voice-id",
    output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
)
response.write_to_file("infill_output.wav")
```

## Response Types

### SSE Events

v3.x SSE streams return typed events:

```python
for event in stream:
    match event.type:
        case "chunk":
            # Audio chunk - event.audio contains bytes
            process_audio(event.audio)
        case "timestamps":
            # Word timestamps - event.word_timestamps
            process_timestamps(event.word_timestamps)
        case "done":
            # Stream complete
            break
```

### WebSocket Responses

v3.x WebSocket responses have a similar structure:

```python
for response in connection:
    if response.type == "chunk":
        process_audio(response.audio)
    elif response.type == "timestamps":
        process_timestamps(response.word_timestamps)
    elif response.type == "done" or response.done:
        break
    elif response.type == "error":
        raise Exception(response.error)
```

## Error Handling

```python
from cartesia import (
    CartesiaError,
    APIError,
    APIStatusError,
    BadRequestError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)

try:
    response = client.tts.generate(...)
except BadRequestError as e:
    print(f"Bad request: {e}")
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except NotFoundError as e:
    print(f"Not found: {e}")
except RateLimitError as e:
    print(f"Rate limited: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Summary of Breaking Changes

| Feature | v2.x | v3.x |
|---------|------|------|
| Voice creation | `client.voices.create(embedding=...)` | `client.voices.clone(clip=...)` |
| Infill | `client.tts.infill()` | `client.tts.infill()` (updated params) |
| Stream parameter | `stream=True/False` | Always streaming, iterate responses |
