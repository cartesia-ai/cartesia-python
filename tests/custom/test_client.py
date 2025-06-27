"""Test against the production Cartesia TTS API.

This test suite tries to be as general as possible because different keys will lead to
different results. Therefore, we cannot test for complete correctness but rather for
general correctness.
"""

import asyncio
import base64
import logging
import os
import sys
import uuid
from typing import Generator, List, Optional, TypedDict, Union

import pytest
from pydantic import ValidationError

from cartesia import AsyncCartesia, Cartesia
from cartesia.core.pagination import SyncPager
from cartesia.tts.requests import (
    ControlsParams,
    TtsRequestIdSpecifierParams,
    TtsRequestVoiceSpecifierParams,
)
from cartesia.tts.requests.output_format import (
    OutputFormat_Mp3Params,
    OutputFormat_RawParams,
    OutputFormat_WavParams,
    OutputFormatParams,
)
from cartesia.tts.types import (
    WebSocketResponse_Chunk,
    WebSocketTtsOutput,
    WordTimestamps,
)
from cartesia.tts.utils.tts import get_output_format
from cartesia.voices.types import Voice, VoiceMetadata


class VoiceControls(TypedDict, total=False):
    speed: Union[float, str]
    emotion: List[str]


THISDIR = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(THISDIR))
RESOURCES_DIR = os.path.join(THISDIR, "resources")

DEFAULT_MODEL_ID = "sonic-2"
DEFAULT_PREVIEW_MODEL_ID = "sonic-2"
DEFAULT_OUTPUT_FORMAT_PARAMS = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}
DEFAULT_OUTPUT_FORMAT = OutputFormat_RawParams(container="raw", encoding="pcm_f32le", sample_rate=44100)
EXPERIMENTAL_VOICE_CONTROLS = {
    "speed": "fastest",
    "emotion": ["anger:high", "positivity:low"],
}
EXPERIMENTAL_VOICE_CONTROLS_2 = {"speed": 0.4, "emotion": []}

SAMPLE_VOICE_NAME = "Southern Woman"
SAMPLE_VOICE_ID = "f9836c6e-a0bd-460e-9d3c-f7299fa60f94"
SAMPLE_VOICE_SPEC = TtsRequestIdSpecifierParams(mode="id", id=SAMPLE_VOICE_ID)
SAMPLE_TRANSCRIPT = "Hello, world! I'm generating audio on Cartesia."
SAMPLE_LANGUAGE = "en"


def _output_format_to_str(fmt: OutputFormatParams) -> str:
    """Convert an output format to a string key.

    Examples:
        wav_pcm_f32le_44100
        wav_pcm_s16le_24000
        mp3_44100
    """
    if fmt["container"] == "wav":
        return f"wav_{fmt['encoding']}_{fmt['sample_rate']}"
    else:  # mp3
        return f"mp3_{fmt['sample_rate']}"


TEST_RAW_OUTPUT_FORMATS = [
    OutputFormat_RawParams(container="raw", encoding="pcm_f32le", sample_rate=44100),
    OutputFormat_RawParams(container="raw", encoding="pcm_s16le", sample_rate=44100),
    OutputFormat_RawParams(container="raw", encoding="pcm_f32le", sample_rate=16000),
    OutputFormat_RawParams(container="raw", encoding="pcm_s16le", sample_rate=16000),
]

TEST_OUTPUT_FORMATS = [
    # WAV format with different encodings and sample rates
    OutputFormat_WavParams(container="wav", encoding="pcm_f32le", sample_rate=44100),
    OutputFormat_WavParams(container="wav", encoding="pcm_s16le", sample_rate=44100),
    OutputFormat_WavParams(container="wav", encoding="pcm_f32le", sample_rate=16000),
    OutputFormat_WavParams(container="wav", encoding="pcm_s16le", sample_rate=16000),
    # MP3 format
    OutputFormat_Mp3Params(container="mp3", sample_rate=44100, bit_rate=128000),
]

# Input audio files keyed by output format string
TEST_INPUT_AUDIO_PATHS = {
    # WAV 44.1kHz
    "wav_pcm_f32le_44100": os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_f32le-44100.wav"),
    "wav_pcm_s16le_44100": os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_s16le-44100.wav"),
    # WAV 16kHz
    "wav_pcm_f32le_16000": os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_f32le-16000.wav"),
    "wav_pcm_s16le_16000": os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_s16le-16000.wav"),
    # MP3
    "mp3_44100": os.path.join(RESOURCES_DIR, "sample-speech-4s-44100.mp3"),
}

logger = logging.getLogger(__name__)


class _Resources:
    def __init__(self, *, client: Cartesia, voices: List[VoiceMetadata], voice: VoiceMetadata):
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

    return _Resources(client=client, voices=voices, voice=voice)  # type: ignore


def _validate_schema(out: WebSocketTtsOutput):
    if out.audio is not None:
        assert isinstance(out.audio, bytes)
    if out.word_timestamps is not None:
        assert isinstance(out.word_timestamps, WordTimestamps)
        word_timestamps = out.word_timestamps

        assert word_timestamps.words is not None
        assert word_timestamps.start is not None
        assert word_timestamps.end is not None
        assert isinstance(word_timestamps.words, list) and all(isinstance(word, str) for word in word_timestamps.words)
        assert isinstance(word_timestamps.start, list) and all(
            isinstance(start, (int, float)) for start in word_timestamps.start
        )
        assert isinstance(word_timestamps.end, list) and all(
            isinstance(end, (int, float)) for end in word_timestamps.end
        )


def _validate_wav_response(data: bytes):
    """Validate WAV format audio data."""
    assert data.startswith(b"RIFF")
    assert data[8:12] == b"WAVE"
    assert len(data) > 44  # Ensure there's audio data beyond the header


def _validate_mp3_response(data: bytes):
    """Validate MP3 format audio data.

    We do basic validation:
    1. Check minimum length
    2. Look for MP3 frame sync word anywhere in first 1KB
    3. Don't enforce specific MPEG version/layer as encoder may vary
    """
    assert len(data) > 128, "MP3 data too short"

    # Search for sync word in first 1KB
    # Valid sync word: 11 bits set (0xFFE0) followed by valid version/layer bits
    found_sync = False
    search_window = min(len(data), 1024)
    for i in range(search_window - 1):
        if data[i] == 0xFF and (data[i + 1] & 0xE0) == 0xE0:
            found_sync = True
            break
    assert found_sync, "No valid MP3 frame sync found"


def _validate_raw_response(data: bytes, sample_rate: int, min_duration_s: float = 1.0):
    """Validate raw audio data."""
    assert len(data) >= sample_rate * min_duration_s, "Raw audio data is too short"


def _validate_audio_response(data: bytes, output_format: OutputFormatParams):
    """Validate audio data based on format."""
    assert len(data) > 0  # All formats should have non-empty data

    if output_format["container"] == "wav":
        _validate_wav_response(data)
    elif output_format["container"] == "mp3":
        _validate_mp3_response(data)
    elif output_format["container"] == "raw":
        _validate_raw_response(data, output_format["sample_rate"])
    else:
        raise ValueError(f"Unsupported output format container: {output_format['container']}")


def test_get_voices(client: Cartesia):
    logger.info("Testing voices.list")
    voices = client.voices.list()
    assert isinstance(voices, SyncPager)
    # Check that voices is a list of Voice objects
    assert all(isinstance(voice, Voice) for voice in voices)
    ids = [voice.id for voice in voices]
    assert len(ids) == len(set(ids)), "All ids must be unique"


def test_get_voice_from_id(client: Cartesia):
    logger.info("Testing voices.get")
    voice = client.voices.get(SAMPLE_VOICE_ID)
    assert voice.id == SAMPLE_VOICE_ID
    assert voice.name == SAMPLE_VOICE_NAME
    assert voice.is_owner is False

    # The API does not yet support expand[]=tags for voices.list, but voices.get does return tags.
    # thus this will not work:
    # voices = client.voices.list(expand=["embedding", "tags"])
    # assert voice in voices
    # Instead:
    voices = client.voices.list()
    
    # Convert to list but limit iteration to avoid full pagination of all voices
    voice_ids = []
    count = 0
    for v in voices:
        voice_ids.append(v.id)
        count += 1
        if count >= 50:
            break
    
    assert voice.id in voice_ids


@pytest.mark.parametrize("mode", ["similarity", "stability"])
@pytest.mark.parametrize("enhance", [True, False])
@pytest.mark.parametrize("language", ["en", "es"])
def test_clone_voice(client: Cartesia, mode: str, enhance: bool, language: str):
    logger.info(
        f"Testing voices.clone with file with path {RESOURCES_DIR}/sample-speech-4s.wav, mode {mode}, enhance {enhance}"
    )
    output = client.voices.clone(
        clip=open(os.path.join(RESOURCES_DIR, "sample-speech-4s.wav"), "rb"),
        name="Test cloned voice",
        language=language,
        mode=mode,
        enhance=enhance,
        description="Test voice description",
    )
    try:
        VoiceMetadata(**output.dict())
    except ValidationError as e:
        pytest.fail(f"Validation error: {e}")
    assert output.name == "Test cloned voice"
    assert output.language == language
    assert output.description == "Test voice description"

    # TTS with the cloned voice
    for model_id in [DEFAULT_MODEL_ID, DEFAULT_PREVIEW_MODEL_ID]:
        audio_chunks = client.tts.bytes(
            transcript=SAMPLE_TRANSCRIPT,
            voice={"mode": "id", "id": output.id},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            model_id=model_id,
            language=language,
        )

        # Combine chunks and validate audio
        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT_PARAMS)

    client.voices.delete(output.id)


def test_create_voice(client: Cartesia):
    logger.info("Testing voices.create")
    embedding = [1.0] * 192
    voice = client.voices.create(
        name="Test Voice",
        description="Test voice description",
        embedding=embedding,
        language="en",
    )
    assert voice.name == "Test Voice"
    assert voice.description == "Test voice description"
    assert voice.is_owner is True
    voices = client.voices.list()
    assert voice.id in [v.id for v in voices]

    client.voices.delete(voice.id)


def test_mix_voice(client: Cartesia):
    logger.info("Testing voices.mix")
    output = client.voices.mix(
        voices=[
            {"id": SAMPLE_VOICE_ID, "weight": 0.1},
            {"id": SAMPLE_VOICE_ID, "weight": 0.9},
        ]
    )
    assert isinstance(output.embedding, list)
    assert all(isinstance(x, float) for x in output.embedding)


@pytest.mark.parametrize("output_format", TEST_OUTPUT_FORMATS)
def test_bytes_sync(resources: _Resources, output_format: OutputFormatParams):
    logger.info("Testing bytes sync")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output = client.tts.bytes(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=output_format,
        model_id=DEFAULT_MODEL_ID,
    )

    data = b"".join(output)
    _validate_audio_response(data, output_format)


@pytest.mark.asyncio
async def test_bytes_async():
    """Test asynchronous bytes generation."""
    async with create_async_client() as async_client:
        chunks = []
        async for chunk in async_client.tts.bytes(
            model_id=DEFAULT_MODEL_ID,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            transcript=SAMPLE_TRANSCRIPT,
            output_format={
                "container": "wav",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
        ):
            chunks.append(chunk)

        data = b"".join(chunks)
        _validate_wav_response(data)


@pytest.mark.parametrize("output_format", TEST_RAW_OUTPUT_FORMATS)
def test_sse_sync(resources: _Resources, output_format: OutputFormatParams):
    logger.info("Testing SSE sync")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output_generate = client.tts.sse(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=output_format,
        model_id=DEFAULT_MODEL_ID,
    )

    chunks = []
    for response in output_generate:
        assert isinstance(response, WebSocketResponse_Chunk)
        audio_bytes = base64.b64decode(response.data)
        chunks.append(audio_bytes)

    data = b"".join(chunks)
    _validate_audio_response(data, output_format)


@pytest.mark.asyncio
@pytest.mark.parametrize("num_requests", [1, 4])
async def test_sse_async(num_requests: int):
    """Test asynchronous SSE generation with concurrent requests."""

    async def send_sse_request(client, transcript, num):
        logger.info(f"Concurrent SSE request {num} sent")
        await asyncio.sleep(0.1)
        output_generate = client.tts.sse(
            transcript=transcript,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            model_id=DEFAULT_MODEL_ID,
        )

        chunks = []
        async for response in output_generate:
            assert isinstance(response, WebSocketResponse_Chunk)
            audio_bytes = base64.b64decode(response.data)
            chunks.append(audio_bytes)

        data = b"".join(chunks)
        _validate_audio_response(data, DEFAULT_OUTPUT_FORMAT_PARAMS)

    async with create_async_client() as async_client:
        transcripts = [SAMPLE_TRANSCRIPT] * num_requests

        tasks = [send_sse_request(async_client, transcript, num) for num, transcript in enumerate(transcripts)]

        await asyncio.gather(*tasks)


def test_sse_err():
    logger.info("Testing SSE with error")
    transcript = SAMPLE_TRANSCRIPT

    try:
        with create_client() as client:
            client.tts.sse(
                transcript=transcript,
                voice={"mode": "id", "id": ""},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                model_id=DEFAULT_MODEL_ID,
            )  # should throw err because voice_id is ""
        raise RuntimeError("Expected error to be thrown")
    except Exception:
        pass


@pytest.mark.parametrize("output_format", TEST_RAW_OUTPUT_FORMATS)
@pytest.mark.parametrize("stream", [True, False])
def test_ws_sync(resources: _Resources, output_format: OutputFormatParams, stream: bool):
    logger.info("Testing WebSocket send context manager")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    with create_client() as client:
        ws = client.tts.websocket()
        output_generate = ws.send(
            transcript=transcript,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},  # type: ignore
            output_format=output_format,
            model_id=DEFAULT_MODEL_ID,
            stream=stream,
        )
        if stream:
            assert isinstance(output_generate, Generator)
            audio = b"".join(out.audio for out in output_generate)
        else:
            assert isinstance(output_generate, WebSocketTtsOutput)
            audio = output_generate.audio

        _validate_audio_response(audio, output_format)


def test_ws_err():
    logger.info("Testing WebSocket with error")
    transcript = SAMPLE_TRANSCRIPT

    try:
        with create_client() as client:
            ws = client.tts.websocket()
            ws.send(
                transcript=transcript,
                voice={"mode": "id", "id": ""},  # type: ignore
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
                model_id=DEFAULT_MODEL_ID,
            )  # should throw err because voice_id is ""
        raise RuntimeError("Expected error to be thrown")
    except Exception:
        pass


@pytest.mark.asyncio
@pytest.mark.parametrize("num_requests", [1, 4])
@pytest.mark.parametrize("stream", [True, False])
async def test_ws_async(num_requests: int, stream: bool):
    """Test asynchronous WebSocket generation with concurrent requests."""

    async def send_websocket_request(client, transcript, num):
        logger.info(f"Concurrent WebSocket request {num} sent")
        await asyncio.sleep(0.1)
        ws = await client.tts.websocket()
        try:
            output_generate = await ws.send(
                transcript=transcript,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                model_id=DEFAULT_MODEL_ID,
                stream=stream,
            )

            if stream:
                chunks = []
                async for out in output_generate:
                    chunks.append(out.audio)

                audio = b"".join(chunks)
            else:
                audio = output_generate.audio

            _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)
        finally:
            await ws.close()

    async with create_async_client() as async_client:
        transcripts = [SAMPLE_TRANSCRIPT] * num_requests

        tasks = [send_websocket_request(async_client, transcript, num) for num, transcript in enumerate(transcripts)]

        await asyncio.gather(*tasks)


def _validate_timestamps(all_words: List[str], all_starts: List[float], all_ends: List[float], transcript: str):
    """Helper method to validate word timestamps against a transcript.

    Args:
        all_words: List of words from timestamps
        all_starts: List of start times
        all_ends: List of end times
        transcript: Original transcript text
    """
    # Verify timestamps
    expected_words = transcript.split()
    assert len(all_words) == len(
        expected_words
    ), f"Expected {len(expected_words)} words in timestamps, got {len(all_words)}"
    assert len(all_starts) == len(all_words), "Number of start times doesn't match number of words"
    assert len(all_ends) == len(all_words), "Number of end times doesn't match number of words"

    # Verify timing order
    for i in range(len(all_starts) - 1):
        assert all_starts[i] <= all_starts[i + 1], "Start times are not monotonically increasing"
        assert all_ends[i] <= all_starts[i + 1], "Word end time is after next word's start time"
        assert all_starts[i] <= all_ends[i], "Word start time is after its end time"

@pytest.mark.parametrize("use_original_timestamps", [True, False])
@pytest.mark.asyncio
async def test_ws_timestamps(use_original_timestamps: bool):
    logger.info("Testing WebSocket with timestamps")
    transcript = SAMPLE_TRANSCRIPT

    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    output_generate = await ws.send(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},  # type: ignore
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
        model_id=DEFAULT_MODEL_ID,
        add_timestamps=True,
        use_original_timestamps=use_original_timestamps,
        stream=True,
    )
    has_wordtimestamps = False
    chunks = []
    all_words = []
    all_starts = []
    all_ends = []
    async for out in output_generate:
        assert out.context_id is not None
        has_wordtimestamps |= out.word_timestamps is not None
        _validate_schema(out)
        if out.word_timestamps is not None:
            all_words.extend(out.word_timestamps.words)
            all_starts.extend(out.word_timestamps.start)
            all_ends.extend(out.word_timestamps.end)
        has_audio = out.audio is not None
        if has_audio:
            chunks.append(out.audio)

    assert has_wordtimestamps, "No word timestamps found"
    _validate_timestamps(all_words, all_starts, all_ends, transcript)

    # Verify audio
    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    # Close the websocket
    await ws.close()
    await async_client.close()


def chunk_generator(transcripts):
    for transcript in transcripts:
        if transcript.endswith(" "):
            yield transcript
        else:
            yield transcript + " "


@pytest.mark.parametrize("stream", [True, False])
@pytest.mark.parametrize("max_buffer_delay_ms", [None, 1000])
def test_continuation_sync(stream: bool, max_buffer_delay_ms: int):
    logger.info("Testing sync continuations")
    client = create_client()
    ws = client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        output_generate = ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=chunk_generator(transcripts),
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            stream=stream,
            max_buffer_delay_ms=max_buffer_delay_ms,
        )
        audio = b"".join(out.audio for out in output_generate)
        _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)
    finally:
        ws.close()


@pytest.mark.parametrize("use_original_timestamps", [True, False])
def test_continuation_timestamps(use_original_timestamps: bool):
    logger.info("Testing continuations with timestamps")
    client = create_client()
    transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
    full_transcript = " ".join(transcripts)

    ws = client.tts.websocket()
    ctx = ws.context()
    output_generate = ctx.send(
        model_id=DEFAULT_MODEL_ID,
        transcript=chunk_generator(transcripts),
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},  # type: ignore
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
        add_timestamps=True,
        use_original_timestamps=use_original_timestamps,
    )

    has_wordtimestamps = False
    chunks = []
    all_words = []
    all_starts = []
    all_ends = []
    for out in output_generate:
        has_wordtimestamps |= out.word_timestamps is not None
        _validate_schema(out)
        if out.word_timestamps is not None:
            all_words.extend(out.word_timestamps.words)
            all_starts.extend(out.word_timestamps.start)
            all_ends.extend(out.word_timestamps.end)
        if out.audio is not None:
            chunks.append(out.audio)

    assert has_wordtimestamps, "No word timestamps found"
    _validate_timestamps(all_words, all_starts, all_ends, full_transcript)

    # Verify audio
    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    ws.close()

@pytest.mark.asyncio
@pytest.mark.parametrize("max_buffer_delay_ms", [None, 1000])
async def test_continuation_async(max_buffer_delay_ms: int):
    logger.info("Testing async continuations")
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
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                continue_=True,
                max_buffer_delay_ms=max_buffer_delay_ms,
            )

        await ctx.no_more_inputs()

        chunks = []
        async for out in ctx.receive():
            chunks.append(out.audio)

        audio = b"".join(chunks)
        _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_incorrect_transcript():
    logger.info("Testing continuations with incorrect transcript")
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
                    voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                    output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
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
@pytest.mark.parametrize("max_buffer_delay_ms", [-100, 2000])
async def test_continuation_incorrect_buffer_delay(max_buffer_delay_ms: int):
    logger.info("Testing continuations with incorrect buffer delay")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        with pytest.raises(RuntimeError):
            ctx = ws.context(context_id)
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript="Hello, world!",
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                max_buffer_delay_ms=max_buffer_delay_ms,
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
async def test_continuation_incorrect_voice_id():
    logger.info("Testing continuations with incorrect voice_id")
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
                    voice={"mode": "id", "id": ""},
                    output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
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
async def test_continuation_incorrect_output_format():
    logger.info("Testing continuations with incorrect output_format")
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
                    voice={"mode": "id", "id": SAMPLE_VOICE_ID},
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
async def test_continuation_incorrect_model_id():
    logger.info("Testing continuations with incorrect model_id")
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
                    voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                    output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
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
async def test_continuation_incorrect_context_id():
    logger.info("Testing continuations with incorrect context_id")
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
                    voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                    context_id="sad-monkeys-fly",  # context_id is different
                    output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
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

@pytest.mark.parametrize("use_original_timestamps", [True, False])
@pytest.mark.asyncio
async def test_continuation_same_context(use_original_timestamps: bool):
    logger.info("Testing continuations with same context")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        full_transcript = " ".join(transcripts)
        # Send once on the context
        for _, transcript in enumerate(transcripts):
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                continue_=True,
                add_timestamps=True,
                use_original_timestamps=use_original_timestamps,
            )

        # Send again on the same context
        for _, transcript in enumerate(transcripts):
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                continue_=True,
                add_timestamps=True,
                use_original_timestamps=use_original_timestamps,
            )

        await ctx.no_more_inputs()

        chunks = []
        all_words = []
        all_starts = []
        all_ends = []
        async for out in ctx.receive():
            if out.word_timestamps is not None:
                all_words.extend(out.word_timestamps.words)
                all_starts.extend(out.word_timestamps.start)
                all_ends.extend(out.word_timestamps.end)
            if out.audio is not None:
                chunks.append(out.audio)

        _validate_timestamps(all_words, all_starts, all_ends, full_transcript + " " + full_transcript)
        audio = b"".join(chunks)
        _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_continuation_flush():
    logger.info("Testing continuations with flush")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    context_id = str(uuid.uuid4())
    try:
        ctx = ws.context(context_id)
        transcripts = [
            "Hello, world!",
            "My name is Cartesia.",
            "I am a text-to-speech API.",
        ]
        receivers = []
        for transcript in transcripts:
            await ctx.send(
                model_id=DEFAULT_MODEL_ID,
                transcript=transcript,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
                continue_=True,
            )
            new_receiver = await ctx.flush()
            receivers.append(new_receiver)
        await ctx.no_more_inputs()

        for receiver in receivers:
            chunks = []
            async for out in receiver():
                if out.audio is not None:
                    chunks.append(out.audio)
                elif out.flush_done:
                    assert out.flush_done is True
                    assert out.flush_id is not None
                else:
                    assert False, f"Received unexpected message: {out}"

            # Validate complete audio
            complete_audio = b"".join(chunks)
            _validate_audio_response(complete_audio, DEFAULT_OUTPUT_FORMAT_PARAMS)
    finally:
        await ws.close()
        await async_client.close()


@pytest.mark.asyncio
async def test_context_cancel():
    """Test cancelling a context during generation."""
    logger.info("Testing context cancellation")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    try:
        # Create a context with a long transcript to ensure there's time to cancel
        ctx = ws.context()
        long_transcript = "This is a very long transcript that will take some time to generate. " * 10

        # Send the request
        await ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=long_transcript,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            continue_=False,
        )

        # Start receiving but cancel after getting a few chunks
        chunks_received = 0
        async for out in ctx.receive():
            chunks_received += 1
            if chunks_received >= 2:  # Cancel after receiving 2 chunks
                await ctx.cancel()
                break

        # Verify the context was closed after cancellation
        assert ctx.is_closed(), "Context should be closed after cancellation"
        logger.info(f"Chunks received: {chunks_received}")

    finally:
        await ws.close()
        await async_client.close()


async def context_runner(ws, transcripts):
    ctx = ws.context()

    full_transcript = " ".join(transcripts)
    chunks = []
    all_words = []
    all_starts = []
    all_ends = []
    has_wordtimestamps = False

    for _, transcript in enumerate(transcripts):
        await ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=transcript,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            continue_=True,
            add_timestamps=True,
        )

    await ctx.no_more_inputs()

    async_gen = ctx.receive()

    async for out in async_gen:
        assert out.context_id == ctx.context_id
        _validate_schema(out)
        if out.audio is not None:
            chunks.append(out.audio)
        if out.word_timestamps is not None:
            has_wordtimestamps = True
            all_words.extend(out.word_timestamps.words)
            all_starts.extend(out.word_timestamps.start)
            all_ends.extend(out.word_timestamps.end)

    # Validate timestamps
    assert has_wordtimestamps, "No word timestamps found"
    _validate_timestamps(all_words, all_starts, all_ends, full_transcript)

    # Validate complete audio
    complete_audio = b"".join(chunks)
    _validate_audio_response(complete_audio, DEFAULT_OUTPUT_FORMAT_PARAMS)


@pytest.mark.asyncio
@pytest.mark.parametrize("num_contexts", [3])
async def test_continuation_parallel(num_contexts: int):
    logger.info(f"Testing async continuation parallel with {num_contexts} contexts")
    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    try:
        transcripts = ["Hello, world!", "I'''m generating audio on Cartesia."]
        tasks = [context_runner(ws, transcripts) for _ in range(num_contexts)]
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
def test_output_formats(output_format_name: str):
    logger.info(f"Testing output format: {output_format_name}")
    output_format = get_output_format(output_format_name)
    assert isinstance(output_format, dict), "Output is not of type dict"
    assert output_format["container"] is not None, "Output format container is None"
    assert output_format["encoding"] is not None, "Output format encoding is None"
    assert output_format["sample_rate"] is not None, "Output format sample rate is None"


def test_invalid_output_format():
    logger.info("Testing invalid output format")
    with pytest.raises(ValueError):
        get_output_format("invalid_format")


def test_ws_with_custom_url():
    logger.info("Testing WebSocket send with custom URL")

    client = Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"), base_url="wss://api.cartesia.ai")

    ws = client.tts.websocket()
    output_generate = ws.send(
        transcript=SAMPLE_TRANSCRIPT,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
        model_id=DEFAULT_MODEL_ID,
        stream=True,
        add_timestamps=True,
    )

    chunks = []
    all_words = []
    all_starts = []
    all_ends = []
    for out in output_generate:
        if out.word_timestamps is not None:
            all_words.extend(out.word_timestamps.words)
            all_starts.extend(out.word_timestamps.start)
            all_ends.extend(out.word_timestamps.end)
        if out.audio is not None:
            chunks.append(out.audio)

    _validate_timestamps(all_words, all_starts, all_ends, SAMPLE_TRANSCRIPT)

    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    ws.close()


@pytest.mark.parametrize("output_format", TEST_OUTPUT_FORMATS)
def test_infill_sync(client: Cartesia, output_format: OutputFormatParams):
    """Test synchronous infill with different output formats."""
    # Get test input audio file matching the output format
    input_audio_path = TEST_INPUT_AUDIO_PATHS[_output_format_to_str(output_format)]

    # Test infill with both left and right audio
    infill_audio, total_audio = client.tts.infill(  # type: ignore
        model_id=DEFAULT_PREVIEW_MODEL_ID,
        language=SAMPLE_LANGUAGE,
        transcript=SAMPLE_TRANSCRIPT,
        left_audio_path=input_audio_path,
        right_audio_path=input_audio_path,
        voice=SAMPLE_VOICE_SPEC,
        output_format=output_format,
    )
    _validate_audio_response(infill_audio, output_format)
    _validate_audio_response(total_audio, output_format)

    # Test infill with only left audio
    infill_audio, total_audio = client.tts.infill(  # type: ignore
        model_id=DEFAULT_PREVIEW_MODEL_ID,
        language=SAMPLE_LANGUAGE,
        transcript=SAMPLE_TRANSCRIPT,
        left_audio_path=input_audio_path,
        right_audio_path=None,
        voice=SAMPLE_VOICE_SPEC,
        output_format=output_format,
    )
    _validate_audio_response(infill_audio, output_format)
    _validate_audio_response(total_audio, output_format)

    # Test infill with only right audio
    infill_audio, total_audio = client.tts.infill(  # type: ignore
        model_id=DEFAULT_PREVIEW_MODEL_ID,
        language=SAMPLE_LANGUAGE,
        transcript=SAMPLE_TRANSCRIPT,
        left_audio_path=None,
        right_audio_path=input_audio_path,
        voice=SAMPLE_VOICE_SPEC,
        output_format=output_format,
    )
    _validate_audio_response(infill_audio, output_format)
    _validate_audio_response(total_audio, output_format)


async def test_infill_async():
    """Test asynchronous infill"""
    output_format = TEST_OUTPUT_FORMATS[0]
    input_audio_path = TEST_INPUT_AUDIO_PATHS[_output_format_to_str(output_format)]

    # Create async client for this test
    async_client = create_async_client()
    try:
        # Test infill with both left and right audio
        infill_audio, total_audio = await async_client.tts.infill(
            model_id=DEFAULT_PREVIEW_MODEL_ID,
            language=SAMPLE_LANGUAGE,
            transcript=SAMPLE_TRANSCRIPT,
            left_audio_path=input_audio_path,
            right_audio_path=input_audio_path,
            voice=SAMPLE_VOICE_SPEC,
            output_format=output_format,
        )
        _validate_audio_response(infill_audio, output_format)
        _validate_audio_response(total_audio, output_format)

        # Test infill with only left audio
        infill_audio, total_audio = await async_client.tts.infill(
            model_id=DEFAULT_PREVIEW_MODEL_ID,
            language=SAMPLE_LANGUAGE,
            transcript=SAMPLE_TRANSCRIPT,
            left_audio_path=input_audio_path,
            right_audio_path=None,
            voice=SAMPLE_VOICE_SPEC,
            output_format=output_format,
        )
        _validate_audio_response(infill_audio, output_format)
        _validate_audio_response(total_audio, output_format)

        # Test infill with only right audio
        infill_audio, total_audio = await async_client.tts.infill(
            model_id=DEFAULT_PREVIEW_MODEL_ID,
            language=SAMPLE_LANGUAGE,
            transcript=SAMPLE_TRANSCRIPT,
            left_audio_path=None,
            right_audio_path=input_audio_path,
            voice=SAMPLE_VOICE_SPEC,
            output_format=output_format,
        )
        _validate_audio_response(infill_audio, output_format)
        _validate_audio_response(total_audio, output_format)
    finally:
        await async_client.close()


@pytest.mark.parametrize(
    "voice_controls",
    [
        None,
        {"speed": 1.0, "emotion": ["positivity:high"]},
        {
            "speed": "normal",
            "emotion": ["curiosity:high", "surprise:high"],
        },
    ],
)
def test_voice_controls(resources: _Resources, voice_controls: Optional[ControlsParams]):
    logger.info("Testing voice controls")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    voice: TtsRequestVoiceSpecifierParams = {"mode": "id", "id": SAMPLE_VOICE_ID}
    if voice_controls:
        voice["experimental_controls"] = voice_controls

    output_generate = client.tts.sse(
        transcript=transcript,
        voice=voice,
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
        model_id=DEFAULT_MODEL_ID,
    )

    chunks = []
    for response in output_generate:
        assert isinstance(response, WebSocketResponse_Chunk)
        audio_bytes = base64.b64decode(response.data)
        chunks.append(audio_bytes)

    complete_audio = b"".join(chunks)
    _validate_audio_response(complete_audio, DEFAULT_OUTPUT_FORMAT_PARAMS)


def test_voice_embedding(resources: _Resources):
    transcript = SAMPLE_TRANSCRIPT
    voice = resources.client.voices.get(SAMPLE_VOICE_ID)
    embedding = voice.embedding

    output_generate = resources.client.tts.sse(
        transcript=transcript,
        voice={"mode": "embedding", "embedding": embedding},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
        model_id=DEFAULT_MODEL_ID,
    )

    chunks = []
    for response in output_generate:
        assert isinstance(response, WebSocketResponse_Chunk)
        audio_bytes = base64.b64decode(response.data)
        chunks.append(audio_bytes)

    complete_audio = b"".join(chunks)
    _validate_audio_response(complete_audio, DEFAULT_OUTPUT_FORMAT_PARAMS)


@pytest.mark.parametrize("language", ["en", "es", "fr", "de", "ja", "pt", "zh"])
def test_multilingual(resources: _Resources, language: str):
    logger.info("Testing multilingual")
    client = resources.client
    transcript = SAMPLE_TRANSCRIPT

    output_generate = client.tts.sse(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,  # type: ignore
        language=language,
        model_id=DEFAULT_MODEL_ID,
    )

    chunks = []
    for out in output_generate:
        assert isinstance(out, WebSocketResponse_Chunk)
        audio_bytes = base64.b64decode(out.data)
        chunks.append(audio_bytes)

    complete_audio = b"".join(chunks)
    _validate_audio_response(complete_audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

# TODO: Add validation against phonemized transcript
def _validate_phoneme_timestamps(phonemes: List[str], starts: List[float], ends: List[float]):
    """Helper method to validate phoneme timestamps against a transcript.

    Args:
        phonemes: List of phonemes from timestamps
        starts: List of start times
        ends: List of end times
    """
    # Verify timestamps
    assert len(phonemes) > 0, "Expected phonemes in timestamps, got none"
    assert len(starts) == len(phonemes), "Number of start times doesn't match number of phonemes"
    assert len(ends) == len(phonemes), "Number of end times doesn't match number of phonemes"

    # Verify timing order
    for i in range(len(starts) - 1):
        assert starts[i] <= starts[i + 1], "Start times are not monotonically increasing"
        assert ends[i] <= starts[i + 1], "Phoneme end time is after next phoneme's start time"
        assert starts[i] <= ends[i], "Phoneme start time is after its end time"


def test_ws_phoneme_timestamps():
    logger.info("Testing WebSocket with phoneme timestamps")
    transcript = SAMPLE_TRANSCRIPT

    client = create_client()
    ws = client.tts.websocket()
    output_generate = ws.send(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
        model_id=DEFAULT_MODEL_ID,
        add_phoneme_timestamps=True,
        stream=True,
    )
    has_phoneme_timestamps = False
    chunks = []
    all_phonemes = []
    all_starts = []
    all_ends = []
    for out in output_generate:
        assert out.context_id is not None
        has_phoneme_timestamps |= out.phoneme_timestamps is not None
        _validate_schema(out)
        if out.phoneme_timestamps is not None:
            all_phonemes.extend(out.phoneme_timestamps.phonemes)
            all_starts.extend(out.phoneme_timestamps.start)
            all_ends.extend(out.phoneme_timestamps.end)
        has_audio = out.audio is not None
        if has_audio:
            chunks.append(out.audio)

    assert has_phoneme_timestamps, "No phoneme timestamps found"
    _validate_phoneme_timestamps(all_phonemes, all_starts, all_ends)

    # Verify audio
    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    # Close the websocket
    ws.close()

def test_continuation_phoneme_timestamps():
    logger.info("Testing continuations with phoneme timestamps")
    client = create_client()
    ws = client.tts.websocket()
    context_id = str(uuid.uuid4())
    ctx = ws.context(context_id)
    transcripts = ["Hello, world!", "I'm generating audio on Cartesia."]

    output_generate = ctx.send(
        model_id=DEFAULT_MODEL_ID,
        transcript=chunk_generator(transcripts),
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
        add_phoneme_timestamps=True,
    )

    has_phoneme_timestamps = False
    chunks = []
    all_phonemes = []
    all_starts = []
    all_ends = []
    for out in output_generate:
        has_phoneme_timestamps |= out.phoneme_timestamps is not None
        _validate_schema(out)
        if out.phoneme_timestamps is not None:
            all_phonemes.extend(out.phoneme_timestamps.phonemes)
            all_starts.extend(out.phoneme_timestamps.start)
            all_ends.extend(out.phoneme_timestamps.end)
        if out.audio is not None:
            chunks.append(out.audio)
    
    assert has_phoneme_timestamps, "No phoneme timestamps found"
    _validate_phoneme_timestamps(all_phonemes, all_starts, all_ends)

    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    ws.close()

@pytest.mark.asyncio
async def test_ws_phoneme_timestamps_async():
    logger.info("Testing WebSocket with phoneme timestamps (async)")
    transcript = SAMPLE_TRANSCRIPT

    async_client = create_async_client()
    ws = await async_client.tts.websocket()
    output_generate = await ws.send(
        transcript=transcript,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
        model_id=DEFAULT_MODEL_ID,
        add_phoneme_timestamps=True,
        stream=True,
    )
    has_phoneme_timestamps = False
    chunks = []
    all_phonemes = []
    all_starts = []
    all_ends = []
    async for out in output_generate:
        assert out.context_id is not None
        has_phoneme_timestamps |= out.phoneme_timestamps is not None
        _validate_schema(out)
        if out.phoneme_timestamps is not None:
            all_phonemes.extend(out.phoneme_timestamps.phonemes)
            all_starts.extend(out.phoneme_timestamps.start)
            all_ends.extend(out.phoneme_timestamps.end)
        has_audio = out.audio is not None
        if has_audio:
            chunks.append(out.audio)

    assert has_phoneme_timestamps, "No phoneme timestamps found"
    _validate_phoneme_timestamps(all_phonemes, all_starts, all_ends)

    # Verify audio
    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    # Close the websocket
    await ws.close()
    await async_client.close()

@pytest.mark.asyncio
async def test_continuation_phoneme_timestamps_async():
    logger.info("Testing continuations with phoneme timestamps (async)")
    client = create_async_client()
    ws = await client.tts.websocket()
    context_id = str(uuid.uuid4())
    ctx = ws.context(context_id)
    transcripts = ["Hello, world!", "I'm generating audio on Cartesia."]

    for transcript in transcripts:
        await ctx.send(
            model_id=DEFAULT_MODEL_ID,
            transcript=transcript,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT_PARAMS,
            add_phoneme_timestamps=True,
            continue_=True,
        )
        
    await ctx.no_more_inputs()

    has_phoneme_timestamps = False
    chunks = []
    all_phonemes = []
    all_starts = []
    all_ends = []
    async for out in ctx.receive():
        has_phoneme_timestamps |= out.phoneme_timestamps is not None
        _validate_schema(out)
        if out.phoneme_timestamps is not None:
            all_phonemes.extend(out.phoneme_timestamps.phonemes)
            all_starts.extend(out.phoneme_timestamps.start)
            all_ends.extend(out.phoneme_timestamps.end)
        if out.audio is not None:
            chunks.append(out.audio)

    assert has_phoneme_timestamps, "No phoneme timestamps found"
    _validate_phoneme_timestamps(all_phonemes, all_starts, all_ends)

    audio = b"".join(chunks)
    _validate_audio_response(audio, DEFAULT_OUTPUT_FORMAT_PARAMS)

    await ws.close()

def _load_test_audio_chunks() -> List[bytes]:
    """Load test audio file and convert to chunks for STT testing."""
    audio_path = os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_s16le-16000.wav")
    
    import wave
    with wave.open(audio_path, 'rb') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        
        chunk_size_frames = int(0.1 * sample_rate)
        chunk_size_bytes = chunk_size_frames * channels * sample_width
        
        chunks = []
        for i in range(0, len(frames), chunk_size_bytes):
            chunk = frames[i:i + chunk_size_bytes]
            if chunk:
                chunks.append(chunk)
        
        return chunks


def _validate_transcript_accuracy(actual_text: str, expected_text: str, min_accuracy: float = 0.7) -> bool:
    """Validate transcript accuracy by comparing word overlap.
    
    Args:
        actual_text: The transcribed text from STT
        expected_text: The expected transcript content
        min_accuracy: Minimum accuracy threshold (0.0 to 1.0)
    
    Returns:
        True if accuracy meets threshold, False otherwise
    """
    if not actual_text or not expected_text:
        return False
    
    # Normalize text: lowercase and split into words
    actual_words = set(actual_text.lower().split())
    expected_words = set(expected_text.lower().split())
    
    if not expected_words:
        return False
    
    # Calculate word overlap accuracy
    matching_words = actual_words.intersection(expected_words)
    accuracy = len(matching_words) / len(expected_words)
    
    logger.info(f"Transcript accuracy: {accuracy:.2%} (expected: {min_accuracy:.0%})")
    logger.info(f"Expected: {expected_text}")
    logger.info(f"Actual: {actual_text}")
    logger.info(f"Matching words: {matching_words}")
    
    return accuracy >= min_accuracy


def test_stt_websocket_sync():
    """Test synchronous STT websocket functionality."""
    logger.info("Testing STT WebSocket sync")
    
    expected_transcript = "magnetic resonance imaging, mri, is clinically relevant"
    
    with create_client() as client:
        audio_chunks = _load_test_audio_chunks()
        
        # Create websocket connection
        ws = client.stt.websocket(
            model="ink-whisper",
            language="en",
            encoding="pcm_s16le", 
            sample_rate=16000,
            min_volume=0.1,
            max_silence_duration_secs=2.0,
        )
        
        # Send audio chunks (streaming input)
        for chunk in audio_chunks:
            ws.send(chunk)
        
        # Finalize and close
        ws.send("finalize")
        ws.send("done")
        
        # Receive transcription results
        results = []
        final_transcript_chunks = []
        word_timestamps_found = False
        for result in ws.receive():
            results.append(result)
            if result['type'] == 'transcript':
                assert isinstance(result['text'], str)
                assert isinstance(result['is_final'], bool)
                logger.info(f"Received transcript: {result['text']}")
                
                # Check for word-level timestamps
                if 'words' in result and result['words']:
                    word_timestamps_found = True
                    words = result['words']
                    assert isinstance(words, list), "Words should be a list"
                    for word_info in words:
                        assert 'word' in word_info, "Each word entry should have 'word' field"
                        assert 'start' in word_info, "Each word entry should have 'start' field"
                        assert 'end' in word_info, "Each word entry should have 'end' field"
                        assert isinstance(word_info['start'], (int, float)), "Start time should be numeric"
                        assert isinstance(word_info['end'], (int, float)), "End time should be numeric"
                        assert word_info['start'] <= word_info['end'], "Start time should be <= end time"
                    logger.info(f"Word timestamps found: {len(words)} words")
                
                # Capture final transcript chunks for accuracy validation
                if result.get('is_final') and result.get('text'):
                    final_transcript_chunks.append(result['text'])
            elif result['type'] == 'done':
                break
        
        ws.close()
        
        assert len(results) > 0, "No STT results received"
        transcript_found = any(r['type'] == 'transcript' for r in results)
        assert transcript_found, "No transcript messages received"
        assert word_timestamps_found, "No word-level timestamps found in responses"
        
        # Validate transcript accuracy
        if final_transcript_chunks:
            final_transcript = ' '.join(final_transcript_chunks).strip()
            accuracy_valid = _validate_transcript_accuracy(final_transcript, expected_transcript, min_accuracy=0.7)
            assert accuracy_valid, f"Transcript accuracy below 70%: '{final_transcript.lower()}' vs expected '{expected_transcript}'"


@pytest.mark.asyncio
async def test_stt_websocket_async():
    """Test asynchronous STT websocket functionality."""
    logger.info("Testing STT WebSocket async")
    
    expected_transcript = "magnetic resonance imaging, mri, is clinically relevant"
    
    async with create_async_client() as async_client:
        audio_chunks = _load_test_audio_chunks()
        
        # Create websocket connection
        ws = await async_client.stt.websocket(
            model="ink-whisper",
            language="en",
            encoding="pcm_s16le",
            sample_rate=16000,
            min_volume=0.15, 
            max_silence_duration_secs=1.5,
        )
        
        # Send audio chunks (streaming input)
        for chunk in audio_chunks:
            await ws.send(chunk)
        
        # Finalize and close
        await ws.send("finalize")
        await ws.send("done")
        
        # Receive transcription results
        results = []
        final_transcript_chunks = []
        word_timestamps_found = False
        async for result in ws.receive():
            results.append(result)
            if result['type'] == 'transcript':
                assert isinstance(result['text'], str)
                assert isinstance(result['is_final'], bool)
                logger.info(f"Received transcript: {result['text']}")
                
                # Check for word-level timestamps
                if 'words' in result and result['words']:
                    word_timestamps_found = True
                    words = result['words']
                    assert isinstance(words, list), "Words should be a list"
                    for word_info in words:
                        assert 'word' in word_info, "Each word entry should have 'word' field"
                        assert 'start' in word_info, "Each word entry should have 'start' field"
                        assert 'end' in word_info, "Each word entry should have 'end' field"
                        assert isinstance(word_info['start'], (int, float)), "Start time should be numeric"
                        assert isinstance(word_info['end'], (int, float)), "End time should be numeric"
                        assert word_info['start'] <= word_info['end'], "Start time should be <= end time"
                    logger.info(f"Word timestamps found: {len(words)} words")
                
                # Capture final transcript chunks for accuracy validation
                if result.get('is_final') and result.get('text'):
                    final_transcript_chunks.append(result['text'])
            elif result['type'] == 'done':
                break
        
        await ws.close()
        
        assert len(results) > 0, "No STT results received"
        transcript_found = any(r['type'] == 'transcript' for r in results)
        assert transcript_found, "No transcript messages received"
        assert word_timestamps_found, "No word-level timestamps found in responses"
        
        # Validate transcript accuracy
        if final_transcript_chunks:
            final_transcript = ' '.join(final_transcript_chunks).strip()
            accuracy_valid = _validate_transcript_accuracy(final_transcript, expected_transcript, min_accuracy=0.7)
            assert accuracy_valid, f"Transcript accuracy below 70%: '{final_transcript.lower()}' vs expected '{expected_transcript}'"


def test_stt_batch_transcription():
    """Test batch STT transcription with word timestamps."""
    logger.info("Testing STT batch transcription")
    
    expected_transcript = "magnetic resonance imaging, mri, is clinically relevant"
    audio_path = os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_s16le-16000.wav")
    
    with create_client() as client:
        # Test batch transcription with word timestamps
        with open(audio_path, 'rb') as audio_file:
            response = client.stt.transcribe(
                file=audio_file,
                model="ink-whisper",
                language="en",
                timestamp_granularities=["word"],
                encoding="pcm_s16le",
                sample_rate=16000
            )
        
        # Validate response structure
        assert hasattr(response, 'text'), "Response should have 'text' field"
        assert hasattr(response, 'language'), "Response should have 'language' field"
        assert hasattr(response, 'duration'), "Response should have 'duration' field"
        assert hasattr(response, 'words'), "Response should have 'words' field for timestamps"
        
        # Validate text content
        assert isinstance(response.text, str), "Text should be a string"
        assert len(response.text.strip()) > 0, "Text should not be empty"
        logger.info(f"Transcribed text: {response.text}")
        
        # Validate language
        if response.language:
            assert response.language == "en", f"Expected language 'en', got '{response.language}'"
        
        # Validate duration
        if response.duration:
            assert isinstance(response.duration, (int, float)), "Duration should be numeric"
            assert response.duration > 0, "Duration should be positive"
            assert response.duration < 10, "Duration should be reasonable for test file"
            logger.info(f"Audio duration: {response.duration:.2f}s")
        
        # Validate word timestamps
        if response.words:
            assert isinstance(response.words, list), "Words should be a list"
            assert len(response.words) > 0, "Should have word timestamps"
            
            for word_info in response.words:
                assert hasattr(word_info, 'word'), "Each word entry should have 'word' field"
                assert hasattr(word_info, 'start'), "Each word entry should have 'start' field"
                assert hasattr(word_info, 'end'), "Each word entry should have 'end' field"
                assert isinstance(word_info.word, str), "Word should be a string"
                assert isinstance(word_info.start, (int, float)), "Start time should be numeric"
                assert isinstance(word_info.end, (int, float)), "End time should be numeric"
                assert word_info.start <= word_info.end, "Start time should be <= end time"
                assert word_info.start >= 0, "Start time should be non-negative"
            
            # Validate timestamp ordering
            for i in range(len(response.words) - 1):
                current_word = response.words[i]
                next_word = response.words[i + 1]
                assert current_word.start <= next_word.start, "Word start times should be in order"
            
            logger.info(f"Word timestamps found: {len(response.words)} words")
            
            # Log sample timestamps for verification
            sample_words = response.words[:3] if len(response.words) >= 3 else response.words
            for word_info in sample_words:
                logger.info(f"  '{word_info.word}': {word_info.start:.2f}s - {word_info.end:.2f}s")
        else:
            logger.warning("No word timestamps returned (this may indicate an API issue)")
        
        # Validate transcript accuracy
        accuracy_valid = _validate_transcript_accuracy(response.text, expected_transcript, min_accuracy=0.7)
        assert accuracy_valid, f"Transcript accuracy below 70%: '{response.text.lower()}' vs expected '{expected_transcript}'"

