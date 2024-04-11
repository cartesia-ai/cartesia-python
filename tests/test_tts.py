"""Test against the production Cartesia TTS API.

This test suite tries to be as general as possible because different keys
will lead to different results. Therefore, we cannot test for complete correctness
but rather for general correctness.
"""

import os
import sys
import uuid
from typing import AsyncGenerator, Dict, Generator, List

import pytest

THISDIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(THISDIR))
from cartesia.tts import DEFAULT_MODEL_ID, AsyncCartesiaTTS, CartesiaTTS, VoiceMetadata

SAMPLE_VOICE = "Milo"


class _Resources:
    def __init__(self, *, client: CartesiaTTS, voices: Dict[str, VoiceMetadata]):
        self.client = client
        self.voices = voices


def create_client():
    return CartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))


def create_async_client():
    return AsyncCartesiaTTS(api_key=os.environ.get("CARTESIA_API_KEY"))


@pytest.fixture(scope="session")
def client():
    return create_client()


@pytest.fixture(scope="session")
def client_with_ws_interrupt():
    return CartesiaTTS(
        api_key=os.environ.get("CARTESIA_API_KEY"), experimental_ws_handle_interrupts=True
    )


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
    client.get_voice_embedding(link=url)


@pytest.mark.parametrize("websocket", [True, False])
def test_generate(resources: _Resources, websocket: bool):
    client = resources.client
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    output = client.generate(transcript=transcript, voice=embedding, websocket=websocket)
    assert output.keys() == {"audio", "sampling_rate"}
    assert isinstance(output["audio"], bytes)
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
        assert isinstance(output["audio"], bytes)
        assert isinstance(output["sampling_rate"], int)


@pytest.mark.parametrize("websocket", [True, False])
def test_generate_stream_context_manager(resources: _Resources, websocket: bool):
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    with create_client() as client:
        generator = client.generate(
            transcript=transcript, voice=embedding, websocket=websocket, stream=True
        )
        assert isinstance(generator, Generator)

        for output in generator:
            assert output.keys() == {"audio", "sampling_rate"}
            assert isinstance(output["audio"], bytes)
            assert isinstance(output["sampling_rate"], int)


def test_generate_context_manager_with_err():
    websocket = None
    websocket_was_opened = False
    try:
        with create_client() as client:
            client.refresh_websocket()
            websocket = client.websocket
            websocket_was_opened = websocket.socket.fileno() != -1
            client.generate(
                transcript=None, voice=None, websocket=True
            )  # should throw because transcript None
        raise RuntimeError("Expected AttributeError to be thrown")
    except AttributeError:
        pass

    assert websocket_was_opened
    assert websocket.socket.fileno() == -1  # check socket is now closed


@pytest.mark.parametrize("websocket", [True, False])
@pytest.mark.asyncio
async def test_async_generate(resources: _Resources, websocket: bool):
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    async_client = create_async_client()
    output = await async_client.generate(
        transcript=transcript, voice=embedding, websocket=websocket
    )

    assert output.keys() == {"audio", "sampling_rate"}
    assert isinstance(output["audio"], bytes)
    assert isinstance(output["sampling_rate"], int)


@pytest.mark.parametrize("websocket", [True, False])
@pytest.mark.asyncio
async def test_async_generate_stream(resources: _Resources, websocket: bool):
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    async_client = create_async_client()

    generator = await async_client.generate(transcript=transcript, voice=embedding, stream=True)
    assert isinstance(generator, AsyncGenerator)

    async for output in generator:
        assert output.keys() == {"audio", "sampling_rate"}
        assert isinstance(output["audio"], bytes)
        assert isinstance(output["sampling_rate"], int)


@pytest.mark.parametrize("websocket", [True, False])
@pytest.mark.asyncio
async def test_async_generate_stream_context_manager(resources: _Resources, websocket: bool):
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    async with create_async_client() as async_client:
        generator = await async_client.generate(transcript=transcript, voice=embedding, stream=True)
        assert isinstance(generator, AsyncGenerator)

        async for output in generator:
            assert output.keys() == {"audio", "sampling_rate"}
            assert isinstance(output["audio"], bytes)
            assert isinstance(output["sampling_rate"], int)


@pytest.mark.asyncio
async def test_generate_async_context_manager_with_err():
    websocket = None
    websocket_was_opened = False
    try:
        async with create_async_client() as async_client:
            await async_client.refresh_websocket()
            websocket = async_client.websocket
            websocket_was_opened = not websocket.closed
            # below should throw because transcript None
            await async_client.generate(transcript=None, voice=None, websocket=True)
        raise RuntimeError("Expected AttributeError to be thrown")
    except AttributeError:
        pass

    assert websocket_was_opened
    assert websocket.closed  # check websocket is now closed


@pytest.mark.parametrize(
    "actions",
    [
        ["cancel-5", None],
        ["cancel-5", "cancel-1", None],
        [None, "cancel-3", None],
        [None, "cancel-1", "cancel-2"],
    ],
)
def test_generate_stream_interrupt(
    client_with_ws_interrupt: CartesiaTTS, resources: _Resources, actions: List[str]
):
    client = client_with_ws_interrupt
    voices = resources.voices
    embedding = voices[SAMPLE_VOICE]["embedding"]
    transcript = "Hello, world!"

    context_ids = [f"test-{uuid.uuid4().hex[:6]}" for _ in range(len(actions))]

    for context_id, action in zip(context_ids, actions):
        body = dict(transcript=transcript, model_id=DEFAULT_MODEL_ID, voice=embedding)

        # Parse actions to see what we should expect.
        if action is None:
            num_turns = None
        elif "cancel" in action:
            num_turns = int(action.split("-")[1])

        generator = client._generate_ws(body, context_id=context_id)
        for idx, response in enumerate(generator):
            assert response.keys() == {"audio", "sampling_rate", "context_id"}
            assert response["context_id"] == context_id, (
                f"Context ID from response ({response['context_id']}) does not match "
                f"the expected context ID ({context_id})"
            )
            if idx + 1 == num_turns:
                break


def test_transcribe(resources: _Resources):
    client = resources.client
    text = client.transcribe(os.path.join(THISDIR, "mock_data/sample_speech.wav"))
    assert text == "It is a great day to be alive when all of the trees are green."


@pytest.mark.asyncio
async def test_async_transcribe():
    async_client = create_async_client()
    text = await async_client.transcribe(os.path.join(THISDIR, "mock_data/sample_speech.wav"))
    assert text == "It is a great day to be alive when all of the trees are green."


@pytest.mark.parametrize("chunk_time", [0.05, 0.6])
def test_check_inputs_invalid_chunk_time(client: CartesiaTTS, chunk_time):
    with pytest.raises(ValueError, match="`chunk_time` must be between 0.1 and 0.5"):
        client._check_inputs("Test", None, chunk_time)


@pytest.mark.parametrize("chunk_time", [0.1, 0.3, 0.5])
def test_check_inputs_valid_chunk_time(client, chunk_time):
    try:
        client._check_inputs("Test", None, chunk_time)
    except ValueError:
        pytest.fail("Unexpected ValueError raised")


def test_check_inputs_duration_less_than_chunk_time(client: CartesiaTTS):
    with pytest.raises(ValueError, match="`duration` must be greater than chunk_time"):
        client._check_inputs("Test", 0.2, 0.3)


@pytest.mark.parametrize("duration,chunk_time", [(0.5, 0.2), (1.0, 0.5), (2.0, 0.1)])
def test_check_inputs_valid_duration_and_chunk_time(client: CartesiaTTS, duration, chunk_time):
    try:
        client._check_inputs("Test", duration, chunk_time)
    except ValueError:
        pytest.fail("Unexpected ValueError raised")


def test_check_inputs_empty_transcript(client: CartesiaTTS):
    with pytest.raises(ValueError, match="`transcript` must be non empty"):
        client._check_inputs("", None, None)


@pytest.mark.parametrize("transcript", ["Hello", "Test transcript", "Lorem ipsum dolor sit amet"])
def test_check_inputs_valid_transcript(client: CartesiaTTS, transcript):
    try:
        client._check_inputs(transcript, None, None)
    except ValueError:
        pytest.fail("Unexpected ValueError raised")
