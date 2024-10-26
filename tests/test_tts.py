"""Test against the production Cartesia TTS API.

This test suite tries to be as general as possible because different keys will lead to
different results. Therefore, we cannot test for complete correctness but rather for
general correctness.
"""

import asyncio
import logging
import os
import sys
import uuid
from typing import AsyncGenerator, Generator, List

import numpy as np
import pytest

from cartesia import AsyncCartesia, Cartesia
from cartesia._types import VoiceControls, VoiceMetadata

THISDIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(THISDIR))
RESOURCES_DIR = os.path.join(THISDIR, "resources")

DEFAULT_MODEL_ID = "sonic-english"  # latest default model
MULTILINGUAL_MODEL_ID = "sonic-multilingual"  # latest multilingual model
SAMPLE_VOICE = "Newsman"
SAMPLE_VOICE_ID = "d46abd1d-2d02-43e8-819f-51fb652c1c61"
EXPERIMENTAL_VOICE_CONTROLS = {
    "emotion": ["anger:high", "positivity:low"],
    "speed": "fastest",
}
EXPERIMENTAL_VOICE_CONTROLS_2 = {"speed": 0.4}
SAMPLE_TRANSCRIPT = "Hello, world! I'm generating audio on Cartesia."

logger = logging.getLogger(__name__)


class _Resources:
    def __init__(
        self, *, client: Cartesia, voices: List[VoiceMetadata], voice: VoiceMetadata
    ):
        self.client = client
        self.voices = voices
        self.voice = voice


def create_client():
    return Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))


def create_async_client():
    return AsyncCartesia(api_key=os.environ.get("CARTESIA_API_KEY"))


@pytest.fixture(scope="session")
def client():
    logger.info("Creating client")
    return create_client()


@pytest.fixture(scope="session")
def resources(client: Cartesia):
    logger.info("Creating resources")
    voice = client.voices.get(SAMPLE_VOICE_ID)
    voices = client.voices.list()

    return _Resources(client=client, voices=voices, voice=voice)


def test_get_voices(client: Cartesia):
    logger.info("Testing voices.list")
    voices = client.voices.list()
    assert isinstance(voices, list)
    # Check that voices is a list of VoiceMetadata objects
    assert all(isinstance(voice, dict) for voice in voices)
    ids = [voice["id"] for voice in voices]
    assert len(ids) == len(set(ids)), "All ids must be unique"


@pytest.mark.skip(reason="Enable after api_status flag is stable and deployed")
def test_get_voice_from_id(client: Cartesia):
    logger.info("Testing voices.get")
    voice = client.voices.get(SAMPLE_VOICE_ID)
    assert voice["id"] == SAMPLE_VOICE_ID
    assert voice["name"] == SAMPLE_VOICE
    assert voice["is_public"] is True
    voices = client.voices.list()
    assert voice in voices


def test_clone_voice_with_file(client: Cartesia):
    logger.info("Testing voices.clone with file")
    output = client.voices.clone(
        filepath=os.path.join(RESOURCES_DIR, "sample-speech-4s.wav")
    )
    assert isinstance(output, list)


@pytest.mark.parametrize("enhance", [True, False])
def test_clone_voice_with_file_enhance(client: Cartesia, enhance: bool):
    logger.info("Testing voices.clone with file")
    output = client.voices.clone(
        filepath=os.path.join(RESOURCES_DIR, "sample-speech-4s.wav"), enhance=enhance
    )
    assert isinstance(output, list)


def test_create_voice(client: Cartesia):
    logger.info("Testing voices.create")
    embedding = np.ones(192).tolist()
    voice = client.voices.create(
        name="Test Voice", description="Test voice description", embedding=embedding
    )
    assert voice["name"] == "Test Voice"
    assert voice["description"] == "Test voice description"
    assert voice["is_public"] is False
    voices = client.voices.list()
    assert voice in voices

    client.voices.delete(voice["id"])


@pytest.mark.skip(reason="Enable after https://github.com/cartesia-ai/bifrost/pull/847 is deployed")
def test_create_voice_with_parent(client: Cartesia):
    logger.info("Testing voices.create with parent")
    voice = client.voices.create(
        name="Test Base voice",
        description="Test base voice description",
        embedding=np.ones(192).tolist(),
        base_voice_id=SAMPLE_VOICE_ID,
    )
    assert isinstance(voice, dict)
    assert voice["base_voice_id"] == SAMPLE_VOICE_ID

    get_voice = client.voices.get(voice["id"])
    assert get_voice["base_voice_id"] == SAMPLE_VOICE_ID

    client.voices.delete(voice["id"])


def test_mix_voice(client: Cartesia):
    logger.info("Testing voices.mix")
    output = client.voices.mix(
        voices=[
            {"id": SAMPLE_VOICE_ID, "weight": 0.1},
            {"id": SAMPLE_VOICE_ID, "weight": 0.9},
        ]
    )
    assert isinstance(output, list)


@pytest.mark.parametrize("stream", [True, False])
@pytest.mark.parametrize(
    "_experimental_voice_controls",
    [None, EXPERIMENTAL_VOICE_CONTROLS, EXPERIMENTAL_VOICE_CONTROLS_2],
)
def test_sse_send(
    resources: _Resources, stream: bool, _experimental_voice_controls: VoiceControls
):
    logger.info("Testing SSE send")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output_generate = client.tts.sse(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=DEFAULT_MODEL_ID,
        _experimental_voice_controls=_experimental_voice_controls,
    )

    if not stream:
        output_generate = [output_generate]

    for out in output_generate:
        assert isinstance(out["audio"], bytes)


@pytest.mark.parametrize("stream", [True, False])
def test_sse_send_with_model_id(resources: _Resources, stream: bool):
    logger.info("Testing SSE send with model_id")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output_generate = client.tts.sse(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=DEFAULT_MODEL_ID,
    )

    if not stream:
        output_generate = [output_generate]

    for out in output_generate:
        assert isinstance(out["audio"], bytes)


@pytest.mark.asyncio
async def test_sse_send_concurrent():
    async def send_sse_request(client, transcript, voice_id, output_format, model_id, num):
        logger.info(f"Concurrent SSE request {num} sent")
        await asyncio.sleep(0.1)
        output_generate = await client.tts.sse(
            transcript=transcript,
            voice_id=voice_id,
            output_format=output_format,
            stream=True,
            model_id=model_id
        )
        async for out in output_generate:
            assert isinstance(out["audio"], bytes)

    logger.info("Testing concurrent SSE send")
    client = create_async_client()

    transcripts = [
        "Hello, world! I'm generating audio on Cartesia. Hello, world! I'm generating audio on Cartesia.",
        "Hello, world! I'm generating audio on Cartesia. Hello, world! I'm generating audio on Cartesia.",
        "Hello, world! I'm generating audio on Cartesia. Hello, world! I'm generating audio on Cartesia.",
    ]

    output_format = {
        "container": "raw",
        "encoding": "pcm_f32le",
        "sample_rate": 44100
    }

    tasks = [
        send_sse_request(
            client,
            transcript,
            SAMPLE_VOICE_ID,
            output_format,
            DEFAULT_MODEL_ID,
            num
        ) for num, transcript in enumerate(transcripts)
    ]

    await asyncio.gather(*tasks)


def test_sse_send_with_voice_id_and_embedding(resources: _Resources):
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT
    voice = client.voices.get(SAMPLE_VOICE_ID)
    embedding = voice["embedding"]

    output_generate = client.tts.sse(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        voice_embedding=embedding,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=True,
        model_id=DEFAULT_MODEL_ID,
    )

    for out in output_generate:
        assert isinstance(out["audio"], bytes)


@pytest.mark.parametrize("stream", [True, False])
@pytest.mark.parametrize(
    "_experimental_voice_controls",
    [None, EXPERIMENTAL_VOICE_CONTROLS, EXPERIMENTAL_VOICE_CONTROLS_2],
)
def test_websocket_send(
    resources: _Resources, stream: bool, _experimental_voice_controls: VoiceControls
):
    logger.info("Testing WebSocket send")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    ws = client.tts.websocket()
    context_id = str(uuid.uuid4())
    output_generate = ws.send(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=DEFAULT_MODEL_ID,
        context_id=context_id,
        _experimental_voice_controls=_experimental_voice_controls,
    )

    if not stream:
        output_generate = [output_generate]

    for out in output_generate:
        assert isinstance(out["audio"], bytes)

    ws.close()


@pytest.mark.parametrize("stream", [True, False])
def test_websocket_send_timestamps(resources: _Resources, stream: bool):
    logger.info("Testing WebSocket send")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    ws = client.tts.websocket()
    context_id = str(uuid.uuid4())
    output_generate = ws.send(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=DEFAULT_MODEL_ID,
        context_id=context_id,
        add_timestamps=True,
    )

    if not stream:
        output_generate = [output_generate]

    has_wordtimestamps = False
    for out in output_generate:
        has_wordtimestamps |= "word_timestamps" in out
        _validate_schema(out)

    assert has_wordtimestamps, "No word timestamps found"

    ws.close()


@pytest.mark.parametrize(
    "_experimental_voice_controls",
    [None, EXPERIMENTAL_VOICE_CONTROLS, EXPERIMENTAL_VOICE_CONTROLS_2],
)
def test_sse_send_context_manager(
    resources: _Resources, _experimental_voice_controls: VoiceControls
):
    logger.info("Testing SSE send context manager")
    transcript = SAMPLE_TRANSCRIPT

    with create_client() as client:
        output_generate = client.tts.sse(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
            _experimental_voice_controls=_experimental_voice_controls,
        )
        assert isinstance(output_generate, Generator)

        for out in output_generate:
            assert out.keys() == {"audio"}
            assert isinstance(out["audio"], bytes)


def test_sse_send_context_manager_with_err():
    logger.info("Testing SSE send context manager with error")
    transcript = SAMPLE_TRANSCRIPT

    try:
        with create_client() as client:
            client.tts.sse(
                transcript=transcript,
                voice_id="",
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                stream=True,
                model_id=DEFAULT_MODEL_ID,
            )  # should throw err because voice_id is ""
        raise RuntimeError("Expected error to be thrown")
    except Exception:
        pass


def test_websocket_send_context_manager(resources: _Resources):
    logger.info("Testing WebSocket send context manager")
    transcript = SAMPLE_TRANSCRIPT

    with create_client() as client:
        ws = client.tts.websocket()
        output_generate = ws.send(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
        )
        assert isinstance(output_generate, Generator)

        for out in output_generate:
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)


def test_websocket_send_context_manage_err(resources: _Resources):
    logger.info("Testing WebSocket send context manager")
    transcript = SAMPLE_TRANSCRIPT

    try:
        with create_client() as client:
            ws = client.tts.websocket()
            ws.send(
                transcript=transcript,
                voice_id="",
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                stream=True,
                model_id=DEFAULT_MODEL_ID,
            )  # should throw err because voice_id is ""
        raise RuntimeError("Expected error to be thrown")
    except Exception:
        pass


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "_experimental_voice_controls",
    [None, EXPERIMENTAL_VOICE_CONTROLS, EXPERIMENTAL_VOICE_CONTROLS_2],
)
async def test_async_sse_send(
    resources: _Resources, _experimental_voice_controls: VoiceControls
):
    logger.info("Testing async SSE send")
    transcript = SAMPLE_TRANSCRIPT

    async_client = create_async_client()
    try:
        output = await async_client.tts.sse(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        async for out in output:
            assert out.keys() == {"audio"}
            assert isinstance(out["audio"], bytes)
    finally:
        # Close the websocket
        await async_client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "_experimental_voice_controls",
    [None, EXPERIMENTAL_VOICE_CONTROLS, EXPERIMENTAL_VOICE_CONTROLS_2],
)
async def test_async_websocket_send(
    resources: _Resources, _experimental_voice_controls: VoiceControls
):
    logger.info("Testing async WebSocket send")
    transcript = SAMPLE_TRANSCRIPT

    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        output = await ws.send(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
            context_id=context_id,
            _experimental_voice_controls=_experimental_voice_controls,
        )

        async for out in output:
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)
    finally:
        # Close the websocket
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_async_websocket_send_timestamps(resources: _Resources):
    logger.info("Testing async WebSocket send with timestamps")
    transcript = SAMPLE_TRANSCRIPT

    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        output = await ws.send(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
            context_id=context_id,
            add_timestamps=True,
        )

        has_wordtimestamps = False
        async for out in output:
            assert "context_id" in out
            has_wordtimestamps |= "word_timestamps" in out
            _validate_schema(out)

        assert has_wordtimestamps, "No word timestamps found"

    finally:
        # Close the websocket
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_async_sse_send_context_manager(resources: _Resources):
    logger.info("Testing async SSE send context manager")
    transcript = SAMPLE_TRANSCRIPT

    async with create_async_client() as async_client:
        output_generate = await async_client.tts.sse(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
        )
        assert isinstance(output_generate, AsyncGenerator)

        async for out in output_generate:
            assert out.keys() == {"audio"}
            assert isinstance(out["audio"], bytes)


@pytest.mark.asyncio
async def test_async_sse_send_context_manager_with_err():
    logger.info("Testing async SSE send context manager with error")
    transcript = SAMPLE_TRANSCRIPT

    try:
        async with create_async_client() as async_client:
            await async_client.tts.sse(
                transcript=transcript,
                voice_id="",
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                stream=True,
                model_id=DEFAULT_MODEL_ID,
            )  # should throw err because voice_id is ""
        raise RuntimeError("Expected error to be thrown")
    except Exception:
        pass


@pytest.mark.asyncio
async def test_async_websocket_send_context_manager():
    logger.info("Testing async WebSocket send context manager")
    transcript = SAMPLE_TRANSCRIPT

    async with create_async_client() as async_client:
        ws = await async_client.tts.websocket()
        output_generate = await ws.send(
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            stream=True,
            model_id=DEFAULT_MODEL_ID,
        )
        assert isinstance(output_generate, AsyncGenerator)

        async for out in output_generate:
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)

        await ws.close()


@pytest.mark.parametrize("stream", [True, False])
@pytest.mark.parametrize("language", ["en", "es", "fr", "de", "ja", "pt", "zh"])
def test_sse_send_multilingual(resources: _Resources, stream: bool, language: str):
    logger.info("Testing SSE send")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output_generate = client.tts.sse(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=MULTILINGUAL_MODEL_ID,
        language=language,
    )

    if not stream:
        output_generate = [output_generate]

    for out in output_generate:
        assert isinstance(out["audio"], bytes)


@pytest.mark.parametrize("stream", [True, False])
@pytest.mark.parametrize("language", ["en", "es", "fr", "de", "ja", "pt", "zh"])
def test_websocket_send_multilingual(
    resources: _Resources, stream: bool, language: str
):
    logger.info("Testing WebSocket send")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    ws = client.tts.websocket()
    output_generate = ws.send(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=stream,
        model_id=MULTILINGUAL_MODEL_ID,
        language=language,
    )

    if not stream:
        output_generate = [output_generate]

    for out in output_generate:
        assert isinstance(out["audio"], bytes)

    ws.close()


def chunk_generator(transcripts):
    for transcript in transcripts:
        if transcript.endswith(" "):
            yield transcript
        else:
            yield transcript + " "


def test_sync_continuation_websocket_context_send():
    logger.info("Testing sync continuation WebSocket context send")
    client = create_client()
    ws = client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        output_generate = ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=chunk_generator(transcripts),
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        )
        for out in output_generate:
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)
    finally:
        ws.close()


def test_sync_context_send_timestamps(resources: _Resources):
    logger.info("Testing WebSocket send")
    client = resources.client
    transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]

    ws = client.tts.websocket()
    ctx = ws.context()
    output_generate = ctx.send(
        transcript=chunk_generator(transcripts),
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        model_id=DEFAULT_MODEL_ID,
        add_timestamps=True,
    )

    has_wordtimestamps = False
    for out in output_generate:
        has_wordtimestamps |= "word_timestamps" in out
        _validate_schema(out)

    assert has_wordtimestamps, "No word timestamps found"

    ws.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send():
    logger.info("Testing async continuation WebSocket context send")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        for _, transcript in enumerate(transcripts):
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice_id=SAMPLE_VOICE_ID,
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                continue_=True,
            )

        await ctx.no_more_inputs()

        async for out in ctx.receive():
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send_incorrect_transcript():
    logger.info(
        "Testing async continuation WebSocket context send with incorrect transcript"
    )
    transcript = SAMPLE_TRANSCRIPT
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        with pytest.raises(ValueError):
            ctx = ws.context(context_id)
            transcripts = [
                "Hello, world!",
                "",
                "I'''m generating audio on Cartesia.",
            ]  # second transcript is empty
            for _, transcript in enumerate(transcripts):
                await ctx.send(
                    model_id=DEFAULT_MODEL_ID,
                    transcript=transcript,
                    voice_id=SAMPLE_VOICE_ID,
                    output_format={
                        "container": "raw",
                        "encoding": "pcm_f32le",
                        "sample_rate": 44100,
                    },
                    continue_=True,
                )

            await ctx.no_more_inputs()

            async for _ in ctx.receive():
                pass
    except Exception as e:
        logger.info("Caught unexpected exception", e)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send_incorrect_voice_id():
    logger.info(
        "Testing async continuation WebSocket context send with incorrect voice_id"
    )
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        with pytest.raises(RuntimeError):
            ctx = ws.context(context_id)
            transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
            for _, transcript in enumerate(transcripts):
                await ctx.send(
                    model_id=DEFAULT_MODEL_ID,
                    transcript=transcript,
                    voice_id="",  # voice_id is empty
                    output_format={
                        "container": "raw",
                        "encoding": "pcm_f32le",
                        "sample_rate": 44100,
                    },
                    continue_=True,
                )

            await ctx.no_more_inputs()

            async for _ in ctx.receive():
                pass
    except Exception as e:
        logger.info("Caught unexpected exception", e)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send_incorrect_output_format():
    logger.info(
        "Testing async continuation WebSocket context send with incorrect output_format"
    )
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        with pytest.raises(RuntimeError):
            ctx = ws.context(context_id)
            transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
            for _, transcript in enumerate(transcripts):
                await ctx.send(
                    model_id=DEFAULT_MODEL_ID,
                    transcript=transcript,
                    voice_id=SAMPLE_VOICE_ID,
                    output_format={
                        "container": "raw",
                        "encoding": "pcm_f32le",
                        "sample_rate": 40,
                    },  # output_format is empty
                    continue_=True,
                )

            await ctx.no_more_inputs()

            async for _ in ctx.receive():
                pass
    except Exception as e:
        logger.info("Caught unexpected exception", e)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send_incorrect_model_id():
    logger.info(
        "Testing async continuation WebSocket context send with incorrect model_id"
    )
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    try:
        with pytest.raises(RuntimeError):
            ctx = ws.context()
            transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
            for _, transcript in enumerate(transcripts):
                await ctx.send(
                    model_id="",  # model_id is empty
                    transcript=transcript,
                    voice_id=SAMPLE_VOICE_ID,
                    output_format={
                        "container": "raw",
                        "encoding": "pcm_f32le",
                        "sample_rate": 44100,
                    },
                    continue_=True,
                )
            async for _ in ctx.receive():
                pass
    except Exception as e:
        logger.info("Caught unexpected exception", e)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_send_incorrect_context_id():
    logger.info(
        "Testing async continuation WebSocket context send with incorrect context_id"
    )
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    try:
        with pytest.raises(ValueError):
            ctx = ws.context(str(uuid.uuid4()))  # create context with context_id
            transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
            for _, transcript in enumerate(transcripts):
                await ctx.send(
                    model_id=DEFAULT_MODEL_ID,
                    transcript=transcript,
                    voice_id=SAMPLE_VOICE_ID,
                    context_id="sad-monkeys-fly",  # context_id is different
                    output_format={
                        "container": "raw",
                        "encoding": "pcm_f32le",
                        "sample_rate": 44100,
                    },
                    continue_=True,
                )

            await ctx.no_more_inputs()

            async for _ in ctx.receive():
                pass
    except Exception as e:
        logger.info("Caught unexpected exception", e)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_websocket_context_twice_on_same_context():
    logger.info("Testing async continuation WebSocket context twice on same context")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        # Send once on the context
        for _, transcript in enumerate(transcripts):
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice_id=SAMPLE_VOICE_ID,
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                continue_=True,
            )

        # Send again on the same context
        for _, transcript in enumerate(transcripts):
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice_id=SAMPLE_VOICE_ID,
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                continue_=True,
            )

        await ctx.no_more_inputs()

        async for out in ctx.receive():
            assert out.keys() == {"audio", "context_id"}
            assert isinstance(out["audio"], bytes)
    finally:
        await ws.close()
        await async_client.close()


async def context_runner(ws, transcripts):
    ctx = ws.context()

    out = []

    for _, transcript in enumerate(transcripts):
        await ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=transcript,
            voice_id=SAMPLE_VOICE_ID,
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
            continue_=True,
        )

    await ctx.no_more_inputs()

    async_gen = ctx.receive()

    async for out in async_gen:
        assert out.keys() == {"audio", "context_id"}
        assert out["context_id"] == ctx.context_id
        assert isinstance(out["audio"], bytes)


@pytest.mark.asyncio
async def test_continuation_websocket_context_three_contexts_parallel():
    logger.info("Testing async continuation WebSocket context three contexts parallel")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    try:
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        tasks = [context_runner(ws, transcripts) for _ in range(3)]
        await asyncio.gather(*tasks)
    finally:
        await ws.close()
        await async_client.close()


output_format_names = [
    "raw_pcm_f32le_44100",
    "raw_pcm_s16le_44100",
    "raw_pcm_f32le_24000",
    "raw_pcm_s16le_24000",
    "raw_pcm_f32le_22050",
    "raw_pcm_s16le_22050",
    "raw_pcm_f32le_16000",
    "raw_pcm_s16le_16000",
    "raw_pcm_f32le_8000",
    "raw_pcm_s16le_8000",
    "raw_pcm_mulaw_8000",
    "raw_pcm_alaw_8000",
]

deprecated_output_format_names = [
    "fp32",
    "pcm",
    "fp32_8000",
    "fp32_16000",
    "fp32_22050",
    "fp32_24000",
    "fp32_44100",
    "pcm_8000",
    "pcm_16000",
    "pcm_22050",
    "pcm_24000",
    "pcm_44100",
    "mulaw_8000",
    "alaw_8000",
]


@pytest.mark.parametrize("output_format_name", output_format_names)
def test_output_formats(resources: _Resources, output_format_name: str):
    logger.info(f"Testing output format: {output_format_name}")
    output_format = resources.client.tts.get_output_format(output_format_name)
    assert isinstance(output_format, dict), "Output is not of type dict"
    assert output_format["container"] is not None, "Output format container is None"
    assert output_format["encoding"] is not None, "Output format encoding is None"
    assert output_format["sample_rate"] is not None, "Output format sample rate is None"


@pytest.mark.parametrize("output_format_name", deprecated_output_format_names)
def test_deprecated_output_formats(resources: _Resources, output_format_name: str):
    logger.info(f"Testing deprecated output format: {output_format_name}")
    output_format = resources.client.tts.get_output_format(output_format_name)
    assert isinstance(output_format, dict), "Output is not of type dict"
    assert output_format["container"] is not None, "Output format container is None"
    assert output_format["encoding"] is not None, "Output format encoding is None"
    assert output_format["sample_rate"] is not None, "Output format sample rate is None"


def test_invalid_output_format(resources: _Resources):
    logger.info("Testing invalid output format")
    with pytest.raises(ValueError):
        resources.client.tts.get_output_format("invalid_format")

def test_websocket_send_with_custom_url():
    logger.info("Testing WebSocket send with custom URL")
    transcript = SAMPLE_TRANSCRIPT

    client = Cartesia(
        api_key=os.environ.get("CARTESIA_API_KEY"), base_url="wss://api.cartesia.ai"
    )

    ws = client.tts.websocket()
    output_generate = ws.send(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=True,
        model_id=DEFAULT_MODEL_ID,
    )

    for out in output_generate:
        assert isinstance(out["audio"], bytes)

    ws.close()


def test_sse_send_with_custom_url():
    logger.info("Testing SSE send with custom URL")
    transcript = SAMPLE_TRANSCRIPT

    client = Cartesia(
        api_key=os.environ.get("CARTESIA_API_KEY"), base_url="https://api.cartesia.ai"
    )
    output_generate = client.tts.sse(
        transcript=transcript,
        voice_id=SAMPLE_VOICE_ID,
        output_format={
            "container": "raw",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
        stream=True,
        model_id=DEFAULT_MODEL_ID,
    )

    for out in output_generate:
        assert isinstance(out["audio"], bytes)


def test_sse_send_with_incorrect_url():
    logger.info("Testing SSE send with custom URL")
    transcript = SAMPLE_TRANSCRIPT

    client = Cartesia(
        api_key=os.environ.get("CARTESIA_API_KEY"),
        base_url="https://api.notcartesia.ai",
    )
    try:
        with pytest.raises(RuntimeError):
            client.tts.sse(
                transcript=transcript,
                voice_id=SAMPLE_VOICE_ID,
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                stream=False,
                model_id=DEFAULT_MODEL_ID,
            )
    except Exception as e:
        logger.info("Unexpected error occured: ", e)


def test_websocket_send_with_incorrect_url():
    logger.info("Testing WebSocket send with custom URL")
    transcript = SAMPLE_TRANSCRIPT

    client = Cartesia(
        api_key=os.environ.get("CARTESIA_API_KEY"), base_url="wss://api.notcartesia.ai"
    )

    try:
        with pytest.raises(RuntimeError):
            ws = client.tts.websocket()
            ws.send(
                transcript=transcript,
                voice_id=SAMPLE_VOICE_ID,
                output_format={
                    "container": "raw",
                    "encoding": "pcm_f32le",
                    "sample_rate": 44100,
                },
                stream=True,
                model_id=DEFAULT_MODEL_ID,
            )
            ws.close()
    except Exception as e:
        logger.info("Unexpected error occured: ", e)


@pytest.mark.asyncio
async def test_tts_bytes():
    async with create_async_client() as async_client:
        data = await async_client.tts.bytes(
            model_id=DEFAULT_MODEL_ID,
            voice_id=SAMPLE_VOICE_ID,
            transcript=SAMPLE_TRANSCRIPT,
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        )
        _validate_wav_response(data)


def test_sync_tts_bytes():
    client = create_client()
    data = client.tts.bytes(
        model_id=DEFAULT_MODEL_ID,
        voice_id=SAMPLE_VOICE_ID,
        transcript=SAMPLE_TRANSCRIPT,
        output_format={
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100,
        },
    )
    _validate_wav_response(data)


def _validate_schema(out):
    if "audio" in out:
        assert isinstance(out["audio"], bytes)
    if "word_timestamps" in out:
        assert isinstance(out["word_timestamps"], dict)
        word_timestamps = out["word_timestamps"]

        assert word_timestamps.keys() == {"words", "start", "end"}
        assert isinstance(word_timestamps["words"], list) and all(
            isinstance(word, str) for word in word_timestamps["words"]
        )
        assert isinstance(word_timestamps["start"], list) and all(
            isinstance(start, (int, float)) for start in word_timestamps["start"]
        )
        assert isinstance(word_timestamps["end"], list) and all(
            isinstance(end, (int, float)) for end in word_timestamps["end"]
        )

def _validate_wav_response(data: bytes):
    assert data.startswith(b'RIFF')
    assert data[8:12] == b'WAVE'
    assert len(data) > 44  # Ensure there's audio data beyond the header
