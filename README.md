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
from IPython.display import Audio

client = CartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))

voices = client.get_voices()
embedding = voices["Milo"]["embedding"]
transcript = "Hello! Welcome to Cartesia"

# No streaming
output = client.generate(transcript=transcript, voice=embedding)
Audio(output["audio"], rate=output["sampling_rate"])

# Streaming
for output in client.generate(transcript=transcript, voice=embedding, stream=True):
    arr = output["audio"]  # a numpy array
    rate = output["sampling_rate"]
```

We recommend using [`python-dotenv`](https://pypi.org/project/python-dotenv/) to add `CARTESIA_API_KEY="my-api-key"` to your .env file so that your API Key is not stored in the source code.
