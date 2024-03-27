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
    buffer = output["audio"]
    rate = output["sampling_rate"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=rate,
                        output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()
```

If you are using Jupyter Notebook or JupyterLab, you can use IPython.display.Audio to play the generated audio directly in the notebook. Here's an example:

```python
from cartesia.tts import CartesiaTTS
from IPython.display import Audio
import io
import os

client = CartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))
voices = client.get_voices()
voice = client.get_voice_embedding(voice_id=voices["Graham"]["id"])
transcript = "Hello! Welcome to Cartesia"

# Create a BytesIO object to store the audio data
audio_data = io.BytesIO()

# Generate and stream audio
for output in client.generate(transcript=transcript, voice=voice, stream=True):
    buffer = output["audio"]
    audio_data.write(buffer)

# Set the cursor position to the beginning of the BytesIO object
audio_data.seek(0)

# Create an Audio object from the BytesIO data
audio = Audio(np.frombuffer(audio_data.read(), dtype=np.float32), rate=output["sampling_rate"])

# Display the Audio object
display(audio)
```

You can also use the async client if you want to make asynchronous API calls. The usage is very similar:
```python
from cartesia.tts import AsyncCartesiaTTS
from IPython.display import Audio
import io
import os

client = AsyncCartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))
voices = client.get_voices()
voice = client.get_voice_embedding(voice_id=voices["Graham"]["id"])
transcript = "Hello! Welcome to Cartesia"

# Create a BytesIO object to store the audio data
audio_data = io.BytesIO()

# Generate and stream audio
async for output in client.generate(transcript=transcript, voice=voice, stream=True):
    buffer = output["audio"]
    audio_data.write(buffer)

# Set the cursor position to the beginning of the BytesIO object
audio_data.seek(0)

# Create an Audio object from the BytesIO data
audio = Audio(np.frombuffer(audio_data.read(), dtype=np.float32), rate=output["sampling_rate"])

# Display the Audio object
display(audio)
```

To avoid storing your API key in the source code, we recommend doing one of the following:
1. Use [`python-dotenv`](https://pypi.org/project/python-dotenv/) to add `CARTESIA_API_KEY="my-api-key"` to your .env file. 
1. Set the `CARTESIA_API_KEY` environment variable, preferably to a secure shell init file (e.g. `~/.zshrc`, `~/.bashrc`)
