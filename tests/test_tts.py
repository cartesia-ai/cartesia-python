import pytest
from unittest.mock import AsyncMock, MagicMock
from cartesia.tts import CartesiaTTS
import json
import numpy as np
import base64

@pytest.fixture
def tts_client():
    client = CartesiaTTS(api_key="test_api_key")
    client._http_url = AsyncMock(return_value="http://testserver")
    return client

@pytest.fixture
def mock_httpx_client(mocker):
    mock = mocker.patch('httpx.AsyncClient')
    mock.return_value.__aenter__.return_value.get = AsyncMock(return_value=MagicMock(status_code=200, text=json.dumps(["voice1", "voice2"])))

    mock_post_response = MagicMock(status_code=200)
    mock_post_response.json.return_value = {
        "audio": base64.b64encode(np.random.rand(16000).astype(np.float32)).decode('utf-8'),
        "sampling_rate": 16000
    }

    async def aiter_bytes():
        yield json.dumps({
            "data": mock_post_response.json.return_value["audio"],
            "sampling_rate": mock_post_response.json.return_value["sampling_rate"]
        }).encode('utf-8')

    mock_post_response.aiter_bytes = aiter_bytes
    mock.return_value.__aenter__.return_value.post = AsyncMock(return_value=mock_post_response)
    return mock

@pytest.mark.asyncio
async def test_voices(tts_client, mock_httpx_client):
    voices = await tts_client.voices()
    assert isinstance(voices, list), "The voices method should return a list."
    assert "voice1" in voices, "The list should contain 'voice1'."
    assert "voice2" in voices, "The list should contain 'voice2'."

@pytest.mark.asyncio
async def test_generate_required_params(tts_client, mock_httpx_client):
    audio_output = await tts_client.generate(transcript="test")
    assert isinstance(audio_output, dict), "The generate method should return a dictionary."
    assert "audio" in audio_output, "The dictionary should have an 'audio' key."
    assert "sampling_rate" in audio_output, "The dictionary should have a 'sampling_rate' key."
    assert isinstance(audio_output["audio"], np.ndarray), "The 'audio' key should contain audio data as a numpy array."
    assert audio_output["sampling_rate"] == 16000, "The 'sampling_rate' key should contain 16000."

@pytest.mark.asyncio
async def test_generate_stream(tts_client, mock_httpx_client):
    audio_generator = await tts_client.generate(transcript="test", stream=True)
    audio_data = await audio_generator.__anext__()
    assert isinstance(audio_data, dict), "The generate method should return a generator that yields audio data."
    assert isinstance(audio_data["audio"], np.ndarray), "The generator should yield audio data as a numpy array."
    assert audio_data["sampling_rate"] == 16000, "The generator should yield '16000' as the sampling rate."
