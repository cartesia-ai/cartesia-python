# cartesia-python
The official Python library for the Cartesia API.

## Usage
```python
from cartesia.tts import CartesiaTTS
from IPython.display import Audio

client = CartesiaTTS(api_key="your-api-key")
transcript = "Hello! How are you doing?"

voices = client.get_voices()
embedding = voices["Milo"]["embedding"]

# No streaming
output = client.generate(transcript=transcript, voice=embedding)
Audio(output["audio"], rate=output["sampling_rate"])

# Streaming
for output in client.generate(transcript=transcript, voice=embedding, stream=True):
    arr = output["audio"]  # a numpy array
    rate = output["sampling_rate"]
```


## Development
If you are developing, make sure to install the development dependencies.

```python
# active your conda environment

# pip install in editable mode
pip install -e '.[dev]'
```

