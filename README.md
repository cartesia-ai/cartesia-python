# Cartesia Python API Library
The official Cartesia Python library which provides convenient access to the Cartesia REST and Websocket API from any Python 3.8+ application.

**Note:** This API is still in alpha. Please expect breaking changes and report any issues you encounter.

## Installation
```bash
pip install cartesia

# pip install in editable mode w/ dev dependencies
pip install -e '.[dev]'
```

## Usage
```python
from cartesia.tts import CartesiaTTS
import pyaudio
import os

client = CartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))
voices = client.get_voices()
voice = client.get_voice_embedding(voice_id=voices["Graham"]["id"])
transcript = "Hello! Welcome to Cartesia"

p = pyaudio.PyAudio()

stream = None

# Generate and stream audio
for output in client.generate(transcript=transcript, voice=voice, stream=True):
    arr = output["audio"]  # a numpy array
    rate = output["sampling_rate"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=rate,
                        output=True)

    # Write the audio data to the stream
    stream.write(arr.tobytes())

stream.stop_stream()
stream.close()
p.terminate()
```

We recommend using [`python-dotenv`](https://pypi.org/project/python-dotenv/) to add `CARTESIA_API_KEY="my-api-key"` to your .env file so that your API Key is not stored in the source code.
