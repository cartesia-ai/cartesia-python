"""Test against the production Cartesia TTS API.

This test suite tries to be as general as possible because different keys
will lead to different results. Therefore, we cannot test for complete correctness
but rather for general correctness.
"""

import os
from typing import Dict, Generator

import numpy as np
import pytest

from cartesia.tts import CartesiaTTS, VoiceMetadata

SAMPLE_VOICE = "Milo"


class _Resources:
    def __init__(self, *, client: CartesiaTTS, voices: Dict[str, VoiceMetadata]):
        self.client = client
        self.voices = voices


@pytest.fixture(scope="session")
def client():
    return CartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))


@pytest.fixture(scope="session")
def resources(client: CartesiaTTS):
    voices = client.get_voices()
    voice_id = voices[SAMPLE_VOICE]["id"]
    voices[SAMPLE_VOICE]["embedding"] = client.get_voice_embedding(voice_id=voice_id)

    return _Resources(
        client=client,
        voices=voices,
    )


def test_get_voices(client: CartesiaTTS):
    voices = client.get_voices()

    assert isinstance(voices, dict)
    assert all(isinstance(key, str) for key in voices.keys())
    ids = [voice["id"] for voice in voices.values()]
    assert len(ids) == len(set(ids)), "All ids must be unique"
    assert all(
        key == voice["name"] for key, voice in voices.items()
    ), "The key must be the same as the name"


def test_get_voice_embedding_from_id(client: CartesiaTTS):
    voices = client.get_voices()
    voice_id = voices[SAMPLE_VOICE]["id"]

    client.get_voice_embedding(voice_id=voice_id)


def test_get_voice_embedding_from_url(client: CartesiaTTS):
    url = "https://youtu.be/g2Z7Ddd573M?si=P8BM_hBqt5P8Ft6I&t=69"
    _ = client.get_voice_embedding(link=url)


@pytest.mark.parametrize("websocket", [True, False])
def test_generate(resources: _Resources, websocket: bool):
    client = resources.client
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    output = client.generate(transcript=transcript, voice=embedding, websocket=websocket)
    assert output.keys() == {"audio", "sampling_rate"}
    assert isinstance(output["audio"], np.ndarray)
    assert output["audio"].dtype == np.float32
    assert isinstance(output["sampling_rate"], int)


@pytest.mark.parametrize("websocket", [True, False])
def test_generate_stream(resources: _Resources, websocket: bool):
    client = resources.client
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    generator = client.generate(
        transcript=transcript, voice=embedding, websocket=websocket, stream=True
    )
    assert isinstance(generator, Generator)

    for output in generator:
        assert output.keys() == {"audio", "sampling_rate"}
        assert isinstance(output["audio"], np.ndarray)
        assert output["audio"].dtype == np.float32
        assert isinstance(output["sampling_rate"], int)
