# cartesia-python
The official Python library for the Cartesia API.

## Usage
```python
from cartesia.tts import CartesiaTTS
from IPython.display import Audio

client = CartesiaTTS()
transcript = "Hello! How are you doing?"

# No streaming
output = client.generate(transcript=transcript)
Audio(output["audio"], rate=output["sampling_rate"])
```


## Development
If you are developing, make sure to install the development dependencies.

```python
# active your conda environment

# pip install in editable mode
pip install -e '.[dev]'
```

