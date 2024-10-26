# Cartesia Python API Library

![PyPI - Version](https://img.shields.io/pypi/v/cartesia)
[![Discord](https://badgen.net/badge/black/Cartesia/icon?icon=discord&label)](https://discord.gg/cartesia)

The official Cartesia Python library which provides convenient access to the Cartesia REST and Websocket API from any Python 3.8+ application.

> [!IMPORTANT]
> The client library introduces breaking changes in v1.0.0, which was released on June 24th 2024. See the [release notes](https://github.com/cartesia-ai/cartesia-python/releases/tag/v1.0.0) and [migration guide](https://github.com/cartesia-ai/cartesia-python/discussions/44). Reach out to us on [Discord](https://discord.gg/cartesia) for any support requests!

- [Cartesia Python API Library](#cartesia-python-api-library)
  - [Documentation](#documentation)
  - [Installation](#installation)
  - [Voices](#voices)
  - [Text-to-Speech](#text-to-speech)
    - [Bytes](#bytes)
    - [Server-Sent Events (SSE)](#server-sent-events-sse)
    - [WebSocket](#websocket)
      - [Conditioning speech on previous generations using WebSocket](#conditioning-speech-on-previous-generations-using-websocket)
    - [Generating timestamps using WebSocket](#generating-timestamps-using-websocket)
    - [Multilingual Text-to-Speech \[Alpha\]](#multilingual-text-to-speech-alpha)
    - [Speed and Emotion Control \[Experimental\]](#speed-and-emotion-control-experimental)
    - [Jupyter Notebook Usage](#jupyter-notebook-usage)
    - [Utility methods](#utility-methods)
      - [Output Formats](#output-formats)


## Documentation

Our complete API documentation can be found [on docs.cartesia.ai](https://docs.cartesia.ai).

## Installation

```bash
pip install cartesia

# pip install in editable mode w/ dev dependencies
pip install -e '.[dev]'
```

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

## Text-to-Speech

### Bytes

```python
from cartesia import Cartesia
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

data = client.tts.bytes(
    model_id="sonic-english",
    transcript="Hello, world! I'm generating audio on Cartesia.",
    voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",  # Barbershop Man
    # You can find the supported `output_format`s at https://docs.cartesia.ai/api-reference/tts/bytes
    output_format={
        "container": "wav",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    },
)

with open("output.wav", "wb") as f:
    f.write(data)
```

### Server-Sent Events (SSE)

```python
from cartesia import Cartesia
import pyaudio
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
voice = client.voices.get(id=voice_id)

transcript = "Hello! Welcome to Cartesia"

# You can check out our models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-english"

# You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

p = pyaudio.PyAudio()
rate = 44100

stream = None

# Generate and stream audio
for output in client.tts.sse(
    model_id=model_id,
    transcript=transcript,
    voice_embedding=voice["embedding"],
    stream=True,
    output_format=output_format,
):
    buffer = output["audio"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()
```

You can also use the async client if you want to make asynchronous API calls. Simply import `AsyncCartesia` instead of `Cartesia` and use await with each API call:

```python
from cartesia import AsyncCartesia
import asyncio
import pyaudio
import os


async def write_stream():
    client = AsyncCartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    voice = client.voices.get(id=voice_id)
    transcript = "Hello! Welcome to Cartesia"
    # You can check out our models at https://docs.cartesia.ai/getting-started/available-models
    model_id = "sonic-english"

    # You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    }

    p = pyaudio.PyAudio()
    rate = 44100

    stream = None

    # Generate and stream audio
    async for output in await client.tts.sse(
        model_id=model_id,
        transcript=transcript,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format=output_format,
    ):
        buffer = output["audio"]

        if not stream:
            stream = p.open(
                format=pyaudio.paFloat32, channels=1, rate=rate, output=True
            )

        # Write the audio data to the stream
        stream.write(buffer)

    stream.stop_stream()
    stream.close()
    p.terminate()
    await client.close()


asyncio.run(write_stream())
```

### WebSocket

```python
from cartesia import Cartesia
import pyaudio
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
voice = client.voices.get(id=voice_id)
transcript = "Hello! Welcome to Cartesia"

# You can check out our models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-english"

# You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 22050,
}

p = pyaudio.PyAudio()
rate = 22050

stream = None

# Set up the websocket connection
ws = client.tts.websocket()

# Generate and stream audio using the websocket
for output in ws.send(
    model_id=model_id,
    transcript=transcript,
    voice_embedding=voice["embedding"],
    stream=True,
    output_format=output_format,
):
    buffer = output["audio"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()

ws.close()  # Close the websocket connection
```

#### Conditioning speech on previous generations using WebSocket

In some cases, input text may need to be streamed in. In these cases, it would be slow to wait for all the text to buffer before sending it to Cartesia's TTS service.

To mitigate this, Cartesia offers audio continuations. In this setting, users can send input text, as it becomes available, over a websocket connection.

To do this, we will create a `context` and send multiple requests without awaiting the response. Then you can listen to the responses in the order they were sent.

Each `context` will be closed automatically after 5 seconds of inactivity or when the `no_more_inputs` method is called. `no_more_inputs` sends a request with the `continue_=False`, which indicates no more inputs will be sent over this context

```python
import asyncio
import os
import pyaudio
from cartesia import AsyncCartesia

async def send_transcripts(ctx):
    # Check out voice IDs by calling `client.voices.list()` or on https://play.cartesia.ai/
    voice_id = "87748186-23bb-4158-a1eb-332911b0b708"

    # You can check out our models at https://docs.cartesia.ai/getting-started/available-models
    model_id = "sonic-english"

    # You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100,
    }

    transcripts = [
        "Sonic and Yoshi team up in a dimension-hopping adventure! ",
        "Racing through twisting zones, they dodge Eggman's badniks and solve ancient puzzles. ",
        "In the Echoing Caverns, they find the Harmonic Crystal, unlocking new powers. ",
        "Sonic's speed creates sound waves, while Yoshi's eggs become sonic bolts. ",
        "As they near Eggman's lair, our heroes charge their abilities for an epic boss battle. ",
        "Get ready to spin, jump, and sound-blast your way to victory in this high-octane crossover!"
    ]

    for transcript in transcripts:
        # Send text inputs as they become available
        await ctx.send(
            model_id=model_id,
            transcript=transcript,
            voice_id=voice_id,
            continue_=True,
            output_format=output_format,
        )

    # Indicate that no more inputs will be sent. Otherwise, the context will close after 5 seconds of inactivity.
    await ctx.no_more_inputs()

async def receive_and_play_audio(ctx):
    p = pyaudio.PyAudio()
    stream = None
    rate = 44100

    async for output in ctx.receive():
        buffer = output["audio"]

        if not stream:
            stream = p.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=rate,
                output=True
            )

        stream.write(buffer)

    stream.stop_stream()
    stream.close()
    p.terminate()

async def stream_and_listen():
    client = AsyncCartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

    # Set up the websocket connection
    ws = await client.tts.websocket()

    # Create a context to send and receive audio
    ctx = ws.context() # Generates a random context ID if not provided

    send_task = asyncio.create_task(send_transcripts(ctx))
    listen_task = asyncio.create_task(receive_and_play_audio(ctx))

    # Call the two coroutine tasks concurrently
    await asyncio.gather(send_task, listen_task)

    await ws.close()
    await client.close()

asyncio.run(stream_and_listen())
```

You can also use continuations on the synchronous Cartesia client to stream in text as it becomes available. To do this, pass in a text generator that produces text chunks at intervals of less than 1 second, as shown below. This ensures smooth audio playback.

Note: the sync client has a different API for continuations compared to the async client.

```python
from cartesia import Cartesia
import pyaudio
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))

transcripts = [
    "The crew engaged in a range of activities designed to mirror those "
    "they might perform on a real Mars mission. ",
    "Aside from growing vegetables and maintaining their habitat, they faced "
    "additional stressors like communication delays with Earth, ",
    "up to twenty-two minutes each way, to simulate the distance from Mars to our planet. ",
    "These exercises were critical for understanding how astronauts can "
    "maintain not just physical health but also mental well-being under such challenging conditions. ",
]

# Ending each transcript with a space makes the audio smoother
def chunk_generator(transcripts):
    for transcript in transcripts:
        if transcript.endswith(" "):
            yield transcript
        else:
            yield transcript + " "


# You can check out voice IDs by calling `client.voices.list()` or on https://play.cartesia.ai/
voice_id = "87748186-23bb-4158-a1eb-332911b0b708"

# You can check out our models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-english"

# You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

p = pyaudio.PyAudio()
rate = 44100

stream = None

# Set up the websocket connection
ws = client.tts.websocket()

# Create a context to send and receive audio
ctx = ws.context()  # Generates a random context ID if not provided

# Pass in a text generator to generate & stream the audio
output_stream = ctx.send(
    model_id=model_id,
    transcript=chunk_generator(transcripts),
    voice_id=voice_id,
    output_format=output_format,
)

for output in output_stream:
    buffer = output["audio"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()

ws.close()  # Close the websocket connection
```

### Generating timestamps using WebSocket

The WebSocket endpoint supports timestamps, allowing you to get detailed timing information for each word in the transcript. To enable this feature, pass an `add_timestamps` boolean flag to the `send` method. The results are returned in the `word_timestamps` object, which contains three keys:
- words (list): The individual words in the transcript.
- start (list): The starting timestamp for each word (in seconds).
- end (list): The ending timestamp for each word (in seconds).

```python
response = ws.send(
    model_id=model_id,
    transcript=transcript,
    voice_id=voice_id,
    output_format=output_format,
    stream=False,
    add_timestamps=True
)

# Accessing the word_timestamps object
word_timestamps = response['word_timestamps']

words = word_timestamps['words']
start_times = word_timestamps['start']
end_times = word_timestamps['end']

for word, start, end in zip(words, start_times, end_times):
    print(f"Word: {word}, Start: {start}, End: {end}")
```

### Multilingual Text-to-Speech [Alpha]

You can use our `sonic-multilingual` model to generate audio in multiple languages. The languages supported are available at [docs.cartesia.ai](https://docs.cartesia.ai/getting-started/available-models).

```python
from cartesia import Cartesia
import pyaudio
import os

client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))
voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
voice = client.voices.get(id=voice_id)

transcript = "Hola! Bienvenido a Cartesia"
language = "es"  # Language code corresponding to the language of the transcript

# Make sure you use the multilingual model! You can check out all models at https://docs.cartesia.ai/getting-started/available-models
model_id = "sonic-multilingual"

# You can find the supported `output_format`s at https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

p = pyaudio.PyAudio()
rate = 44100

stream = None

# Pass in the corresponding language code to the `language` parameter to generate and stream audio.
for output in client.tts.sse(
    model_id=model_id,
    transcript=transcript,
    voice_embedding=voice["embedding"],
    stream=True,
    output_format=output_format,
    language=language,
):
    buffer = output["audio"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()
```

### Speed and Emotion Control [Experimental]

You can enhance the voice output by adjusting the `speed` and `emotion` parameters. To do this, pass a `_experimental_voice_controls` dictionary with the desired `speed` and `emotion` values to any `send` method.

Speed Options:
- `slowest`, `slow`, `normal`, `fast`, `fastest`
- Float values between -1.0 and 1.0, where -1.0 is the slowest speed and 1.0 is the fastest speed.

Emotion Options:
Use a list of tags in the format `emotion_name:level` where:
- Emotion Names: `anger`, `positivity`, `surprise`, `sadness`, `curiosity`
- Levels: `lowest`, `low`, (omit for medium level), `high`, `highest`
The emotion tag levels add the specified emotion to the voice at the indicated intensity, with the omission of a level tag resulting in a medium intensity.

```python
ws.send(
    model_id=model_id,
    transcript=transcript,
    voice_id=voice_id,
    output_format=output_format,
    _experimental_voice_controls={"speed": "fast", "emotion": ["positivity:high"]},
)
```

### Jupyter Notebook Usage

If you are using Jupyter Notebook or JupyterLab, you can use IPython.display.Audio to play the generated audio directly in the notebook.
Additionally, in these notebook examples we show how to use the client as a context manager (though this is not required).

```python
from IPython.display import Audio
import io
import os
import numpy as np

from cartesia import Cartesia

with Cartesia(api_key=os.environ.get("CARTESIA_API_KEY")) as client:
    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 8000,
    }
    rate = 8000
    voice_id = "a0e99841-438c-4a64-b679-ae501e7d6091"
    voice = client.voices.get(id=voice_id)
    transcript = "Hey there! Welcome to Cartesia"

    # Create a BytesIO object to store the audio data
    audio_data = io.BytesIO()

    # Generate and stream audio
    for output in client.tts.sse(
        model_id="sonic-english",
        transcript=transcript,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format=output_format,
    ):
        buffer = output["audio"]
        audio_data.write(buffer)

# Set the cursor position to the beginning of the BytesIO object
audio_data.seek(0)

# Create an Audio object from the BytesIO data
audio = Audio(np.frombuffer(audio_data.read(), dtype=np.float32), rate=rate)

# Display the Audio object
display(audio)
```

Below is the same example using the async client:

```python
from IPython.display import Audio
import io
import os
import numpy as np

from cartesia import AsyncCartesia

async with AsyncCartesia(api_key=os.environ.get("CARTESIA_API_KEY")) as client:
    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 8000,
    }
    rate = 8000
    voice_id = "248be419-c632-4f23-adf1-5324ed7dbf1d"
    transcript = "Hey there! Welcome to Cartesia"

    # Create a BytesIO object to store the audio data
    audio_data = io.BytesIO()

    # Generate and stream audio
    async for output in client.tts.sse(
        model_id="sonic-english",
        transcript=transcript,
        voice_id=voice_id,
        stream=True,
        output_format=output_format,
    ):
        buffer = output["audio"]
        audio_data.write(buffer)

# Set the cursor position to the beginning of the BytesIO object
audio_data.seek(0)

# Create an Audio object from the BytesIO data
audio = Audio(np.frombuffer(audio_data.read(), dtype=np.float32), rate=rate)

# Display the Audio object
display(audio)
```

### Utility methods

#### Output Formats

You can use the `client.tts.get_output_format` method to convert string-based output format names into the `output_format` dictionary which is expected by the `output_format` parameter. You can see the `OutputFormatMapping` class in `cartesia._types` for the currently supported output format names. You can also view the currently supported `output_format`s in our [API Reference](https://docs.cartesia.ai/reference/api-reference/rest/stream-speech-server-sent-events).

The previously used `output_format` strings are now deprecated and will be removed in v1.2.0. These are listed in the `DeprecatedOutputFormatMapping` class in `cartesia._types`.

```python
# Get the output format dictionary from string name
output_format = client.tts.get_output_format("raw_pcm_f32le_44100")

# Pass in the output format dictionary to generate and stream audio
generator = client.tts.sse(
    model_id=model,
    transcript=transcript,
    voice_id=SAMPLE_VOICE_ID,
    stream=True,
    output_format=output_format,
)
```

To avoid storing your API key in the source code, we recommend doing one of the following:

1. Use [`python-dotenv`](https://pypi.org/project/python-dotenv/) to add `CARTESIA_API_KEY="my-api-key"` to your .env file.
1. Set the `CARTESIA_API_KEY` environment variable, preferably to a secure shell init file (e.g. `~/.zshrc`, `~/.bashrc`)
