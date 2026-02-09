"""Integration tests against the production Cartesia API for SDK v3.

This test suite validates the SDK's functionality against the real API.
Different API keys may lead to different results, so we test for general
correctness rather than exact values.

Run with: pytest tests/test_integration.py -v
Requires: CARTESIA_API_KEY environment variable
"""

import asyncio
import logging
import os
import uuid
from typing import List

import pytest

from cartesia import AsyncCartesia, Cartesia
from cartesia.pagination import SyncCursorIDPage
from cartesia.types import Voice, VoiceMetadata

# Ignore asyncio resource warnings that occur during test teardown
pytestmark = pytest.mark.filterwarnings(
    "ignore::pytest.PytestUnraisableExceptionWarning",
    "ignore::ResourceWarning"
)

THISDIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.join(THISDIR, "resources")

# Ensure resources directory exists
os.makedirs(RESOURCES_DIR, exist_ok=True)

DEFAULT_MODEL_ID = "sonic-2"
DEFAULT_OUTPUT_FORMAT = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

# Sophie voice - a stable voice for testing
SAMPLE_VOICE_ID = "bf0a246a-8642-498a-9950-80c35e9276b5"
SAMPLE_TRANSCRIPT = "Hello, world! I'm generating audio on Cartesia."
SAMPLE_LANGUAGE = "en"

logger = logging.getLogger(__name__)


# ============================================================================
# Fixtures
# ============================================================================


def create_client():
    return Cartesia(api_key=os.environ.get("CARTESIA_API_KEY"))


def create_async_client():
    return AsyncCartesia(api_key=os.environ.get("CARTESIA_API_KEY"))


@pytest.fixture(scope="session")
def client():
    logger.info("Creating client")
    return create_client()


@pytest.fixture(scope="session")
def sample_audio_path():
    """Get a sample audio file for testing voice cloning."""
    # Try to find an existing audio file in resources
    possible_paths = [
        os.path.join(RESOURCES_DIR, "sample-speech-4s.wav"),
        os.path.join(RESOURCES_DIR, "sample-speech-4s-pcm_s16le-16000.wav"),
        os.path.join(RESOURCES_DIR, "test.wav"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path

    # If no file exists, skip tests that need it
    pytest.skip("No sample audio file found for voice cloning tests")


# ============================================================================
# Validation Helpers
# ============================================================================


def _validate_wav_response(data: bytes):
    """Validate WAV format audio data."""
    assert data.startswith(b"RIFF"), "WAV should start with RIFF"
    assert data[8:12] == b"WAVE", "WAV should contain WAVE marker"
    assert len(data) > 44, "WAV should have audio data beyond header"


def _validate_mp3_response(data: bytes):
    """Validate MP3 format audio data."""
    assert len(data) > 128, "MP3 data too short"

    # Search for MP3 sync word in first 1KB
    found_sync = False
    search_window = min(len(data), 1024)
    for i in range(search_window - 1):
        if data[i] == 0xFF and (data[i + 1] & 0xE0) == 0xE0:
            found_sync = True
            break
    assert found_sync, "No valid MP3 frame sync found"


def _validate_raw_response(data: bytes, sample_rate: int, min_duration_s: float = 0.5):
    """Validate raw audio data has minimum expected length."""
    # For pcm_f32le, each sample is 4 bytes
    expected_min_bytes = int(sample_rate * min_duration_s * 4)
    assert len(data) >= expected_min_bytes, f"Raw audio too short: {len(data)} < {expected_min_bytes}"


def _validate_audio_response(data: bytes, output_format: dict):
    """Validate audio data based on format."""
    assert len(data) > 0, "Audio data should not be empty"

    container = output_format.get("container", "raw")
    if container == "wav":
        _validate_wav_response(data)
    elif container == "mp3":
        _validate_mp3_response(data)
    elif container == "raw":
        _validate_raw_response(data, output_format.get("sample_rate", 44100))


def _validate_timestamps(words: List[str], starts: List[float], ends: List[float]):
    """Validate word timestamps are properly ordered."""
    assert len(words) > 0, "Should have words"
    assert len(starts) == len(words), "Start times count should match words"
    assert len(ends) == len(words), "End times count should match words"

    for i in range(len(starts)):
        assert starts[i] <= ends[i], f"Word {i} start time should be <= end time"

    for i in range(len(starts) - 1):
        assert starts[i] <= starts[i + 1], "Start times should be monotonically increasing"


# ============================================================================
# Voice Tests
# ============================================================================


def test_list_voices(client: Cartesia):
    """Test listing voices with pagination."""
    logger.info("Testing voices.list")
    voices = client.voices.list(limit=10)

    assert isinstance(voices, SyncCursorIDPage)

    # Get first page of results
    voice_list = list(voices)
    assert len(voice_list) > 0, "Should have at least one voice"
    assert all(isinstance(v, Voice) for v in voice_list)


def test_get_voice(client: Cartesia):
    """Test getting a specific voice by ID."""
    logger.info("Testing voices.get")
    voice = client.voices.get(SAMPLE_VOICE_ID)

    assert voice.id == SAMPLE_VOICE_ID
    assert voice.name is not None
    assert isinstance(voice, Voice)


def test_clone_voice(client: Cartesia, sample_audio_path: str):
    """Test voice cloning from an audio clip."""
    logger.info(f"Testing voices.clone with {sample_audio_path}")

    with open(sample_audio_path, "rb") as clip_file:
        voice = client.voices.clone(
            clip=clip_file,
            name="Test Cloned Voice",
            description="Test voice for SDK integration tests",
            language="en",
        )

    try:
        assert isinstance(voice, VoiceMetadata)
        assert voice.id is not None
        assert voice.name == "Test Cloned Voice"
        assert voice.language == "en"

        # Test TTS with the cloned voice
        response = client.tts.generate(
            model_id=DEFAULT_MODEL_ID,
            transcript="Testing the cloned voice.",
            voice={"mode": "id", "id": voice.id},
            output_format=DEFAULT_OUTPUT_FORMAT,
            language="en",
        )
        audio_data = b"".join(response.iter_bytes())
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)

    finally:
        # Clean up
        client.voices.delete(voice.id)


def test_update_voice(client: Cartesia, sample_audio_path: str):
    """Test updating a voice's metadata."""
    logger.info("Testing voices.update")

    # First create a voice to update
    with open(sample_audio_path, "rb") as clip_file:
        voice = client.voices.clone(
            clip=clip_file,
            name="Voice To Update",
            description="Original description",
            language="en",
        )

    try:
        # Update the voice
        updated = client.voices.update(
            voice.id,
            name="Updated Voice Name",
            description="Updated description",
        )

        assert updated.name == "Updated Voice Name"
        assert updated.description == "Updated description"

    finally:
        client.voices.delete(voice.id)


# ============================================================================
# TTS Bytes Tests
# ============================================================================


@pytest.mark.parametrize("output_format", [
    {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
    {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 16000},
    {"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    {"container": "mp3", "sample_rate": 44100, "bit_rate": 128000},
])
def test_tts_generate_sync(client: Cartesia, output_format: dict):
    """Test synchronous TTS generation with various output formats."""
    logger.info(f"Testing tts.generate with format {output_format}")

    response = client.tts.generate(
        model_id=DEFAULT_MODEL_ID,
        transcript=SAMPLE_TRANSCRIPT,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=output_format,
        language=SAMPLE_LANGUAGE,
    )

    audio_data = b"".join(response.iter_bytes())
    _validate_audio_response(audio_data, output_format)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_tts_generate_async():
    """Test asynchronous TTS generation."""
    logger.info("Testing async tts.generate")

    async with create_async_client() as client:
        response = await client.tts.generate(
            model_id=DEFAULT_MODEL_ID,
            transcript=SAMPLE_TRANSCRIPT,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
            language=SAMPLE_LANGUAGE,
        )

        chunks = []
        async for chunk in response.iter_bytes():
            chunks.append(chunk)

        audio_data = b"".join(chunks)
        _validate_wav_response(audio_data)


# ============================================================================
# TTS SSE Tests
# ============================================================================


def test_tts_sse_sync(client: Cartesia):
    """Test synchronous TTS SSE streaming."""
    logger.info("Testing tts.generate_sse")

    stream = client.tts.generate_sse(
        model_id=DEFAULT_MODEL_ID,
        transcript=SAMPLE_TRANSCRIPT,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT,
        language=SAMPLE_LANGUAGE,
    )

    audio_chunks = []
    for event in stream:
        if event.type == "chunk" and event.audio:
            audio_chunks.append(event.audio)
        elif event.type == "done":
            break
        elif event.type == "error":
            pytest.fail(f"SSE error: {getattr(event, 'error', 'Unknown')}")

    audio_data = b"".join(audio_chunks)
    _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


def test_tts_sse_with_timestamps(client: Cartesia):
    """Test TTS SSE with word timestamps."""
    logger.info("Testing tts.generate_sse with timestamps")

    stream = client.tts.generate_sse(
        model_id=DEFAULT_MODEL_ID,
        transcript=SAMPLE_TRANSCRIPT,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT,
        language=SAMPLE_LANGUAGE,
        add_timestamps=True,
    )

    audio_chunks = []
    all_words = []
    all_starts = []
    all_ends = []

    for event in stream:
        if event.type == "chunk" and event.audio:
            audio_chunks.append(event.audio)
        elif event.type == "timestamps":
            wt = getattr(event, "word_timestamps", None)
            if wt:
                # Handle dict, list, and object forms
                if isinstance(wt, dict):
                    all_words.extend(wt.get("words", []))
                    all_starts.extend(wt.get("start", []))
                    all_ends.extend(wt.get("end", []))
                elif isinstance(wt, list):
                    # List of timestamp entries
                    for ts in wt:
                        if isinstance(ts, dict):
                            if "word" in ts:
                                all_words.append(ts["word"])
                            if "start" in ts:
                                all_starts.append(ts["start"])
                            if "end" in ts:
                                all_ends.append(ts["end"])
                else:
                    all_words.extend(wt.words)
                    all_starts.extend(wt.start)
                    all_ends.extend(wt.end)
        elif event.type == "done":
            break

    audio_data = b"".join(audio_chunks)
    _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)

    if all_words:
        _validate_timestamps(all_words, all_starts, all_ends)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_tts_sse_async():
    """Test asynchronous TTS SSE streaming."""
    logger.info("Testing async tts.generate_sse")

    async with create_async_client() as client:
        stream = await client.tts.generate_sse(
            model_id=DEFAULT_MODEL_ID,
            transcript=SAMPLE_TRANSCRIPT,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT,
            language=SAMPLE_LANGUAGE,
        )

        audio_chunks = []
        async for event in stream:
            if event.type == "chunk" and event.audio:
                audio_chunks.append(event.audio)
            elif event.type == "done":
                break

        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


# ============================================================================
# TTS WebSocket Tests
# ============================================================================


def test_tts_websocket_sync(client: Cartesia):
    """Test synchronous TTS WebSocket streaming."""
    logger.info("Testing tts.websocket_connect (WebSocket)")

    with client.tts.websocket_connect() as connection:
        context_id = str(uuid.uuid4())
        connection.send({
            "context_id": context_id,
            "model_id": DEFAULT_MODEL_ID,
            "transcript": SAMPLE_TRANSCRIPT,
            "voice": {"mode": "id", "id": SAMPLE_VOICE_ID},
            "output_format": DEFAULT_OUTPUT_FORMAT,
            "language": SAMPLE_LANGUAGE,
        })

        audio_chunks = []
        for response in connection:
            if response.type == "chunk" and response.audio:
                audio_chunks.append(response.audio)
            elif response.type == "done" or response.done:
                break
            elif response.type == "error":
                pytest.fail(f"WebSocket error: {getattr(response, 'error', 'Unknown')}")

        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


def test_tts_websocket_with_timestamps(client: Cartesia):
    """Test TTS WebSocket with word timestamps."""
    logger.info("Testing tts.websocket_connect with timestamps")

    with client.tts.websocket_connect() as connection:
        context_id = str(uuid.uuid4())
        connection.send({
            "context_id": context_id,
            "model_id": DEFAULT_MODEL_ID,
            "transcript": SAMPLE_TRANSCRIPT,
            "voice": {"mode": "id", "id": SAMPLE_VOICE_ID},
            "output_format": DEFAULT_OUTPUT_FORMAT,
            "language": SAMPLE_LANGUAGE,
            "add_timestamps": True,
        })

        audio_chunks = []
        all_words = []
        all_starts = []
        all_ends = []

        for response in connection:
            if response.type == "chunk" and response.audio:
                audio_chunks.append(response.audio)
            elif response.type == "timestamps":
                wt = getattr(response, "word_timestamps", None)
                if wt:
                    # Handle both dict and object forms
                    if isinstance(wt, dict):
                        all_words.extend(wt.get("words", []))
                        all_starts.extend(wt.get("start", []))
                        all_ends.extend(wt.get("end", []))
                    else:
                        all_words.extend(wt.words)
                        all_starts.extend(wt.start)
                        all_ends.extend(wt.end)
            elif response.type == "done" or response.done:
                break

        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)

        if all_words:
            _validate_timestamps(all_words, all_starts, all_ends)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_tts_websocket_async():
    """Test asynchronous TTS WebSocket streaming."""
    logger.info("Testing async tts.websocket_connect")

    async with create_async_client() as client:
        async with client.tts.websocket_connect() as connection:
            context_id = str(uuid.uuid4())
            await connection.send({
                "context_id": context_id,
                "model_id": DEFAULT_MODEL_ID,
                "transcript": SAMPLE_TRANSCRIPT,
                "voice": {"mode": "id", "id": SAMPLE_VOICE_ID},
                "output_format": DEFAULT_OUTPUT_FORMAT,
                "language": SAMPLE_LANGUAGE,
            })

            audio_chunks = []
            async for response in connection:
                if response.type == "chunk" and response.audio:
                    audio_chunks.append(response.audio)
                elif response.type == "done" or response.done:
                    break

            audio_data = b"".join(audio_chunks)
            _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


def test_tts_websocket_context(client: Cartesia):
    """Test TTS WebSocket with context for continuations using .push()."""
    logger.info("Testing tts.websocket_connect with context")

    with client.tts.websocket_connect() as connection:
        # context_id must be alphanumeric with underscores/hyphens only
        context_id = str(uuid.uuid4())
        ctx = connection.context(
            context_id=context_id,
            model_id=DEFAULT_MODEL_ID,
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT,
            language=SAMPLE_LANGUAGE,
        )

        # Send multiple transcripts as continuation using .push()
        transcripts = ["Hello there!", "How are you today?"]
        for transcript in transcripts:
            ctx.push(transcript)

        ctx.no_more_inputs()

        audio_chunks = []
        for response in ctx.receive():
            if response.type == "chunk" and response.audio:
                audio_chunks.append(response.audio)

        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_tts_websocket_context_async():
    """Test async TTS WebSocket with context for continuations."""
    logger.info("Testing async tts.websocket_connect with context")

    async with create_async_client() as client:
        async with client.tts.websocket_connect() as connection:
            # context_id must be alphanumeric with underscores/hyphens only
            context_id = str(uuid.uuid4())
            ctx = connection.context(context_id)

            transcripts = ["Hello there!", "How are you today?"]
            for transcript in transcripts:
                await ctx.send(
                    model_id=DEFAULT_MODEL_ID,
                    transcript=transcript,
                    voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                    output_format=DEFAULT_OUTPUT_FORMAT,
                    language=SAMPLE_LANGUAGE,
                    continue_=True,
                )

            await ctx.no_more_inputs()

            audio_chunks = []
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    audio_chunks.append(response.audio)

            audio_data = b"".join(audio_chunks)
            _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_tts_websocket_push_overrides(client: Cartesia):
    """Test TTS WebSocket .push() with dynamic parameter overrides."""
    logger.info("Testing tts.websocket_connect .push() overrides")

    with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT,
            language=SAMPLE_LANGUAGE,
        )

        ctx.push("Normal speed. ")
        # Override generation_config via kwargs
        ctx.push("Fast speed!", generation_config={"speed": 1.5})
        ctx.no_more_inputs()

        audio_chunks = []
        for response in ctx.receive():
            if response.type == "chunk" and response.audio:
                audio_chunks.append(response.audio)

        audio_data = b"".join(audio_chunks)
        _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_tts_websocket_concurrent_contexts_async():
    """Test multiple concurrent contexts on a single WebSocket connection."""
    logger.info("Testing concurrent contexts on one WebSocket")

    async with create_async_client() as client:
        async with client.tts.websocket_connect() as connection:
            ctx1 = connection.context(
                model_id=DEFAULT_MODEL_ID,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT,
            )
            ctx2 = connection.context(
                model_id=DEFAULT_MODEL_ID,
                voice={"mode": "id", "id": SAMPLE_VOICE_ID},
                output_format=DEFAULT_OUTPUT_FORMAT,
            )

            async def send_to_ctx(ctx, text):
                await ctx.push(text)
                await ctx.no_more_inputs()

            # Start sending concurrently
            send_task1 = asyncio.create_task(send_to_ctx(ctx1, "Context one audio."))
            send_task2 = asyncio.create_task(send_to_ctx(ctx2, "Context two audio."))

            # Receiver loop to demultiplex
            audio1, audio2 = [], []
            active = {ctx1._context_id, ctx2._context_id}

            async for response in connection:
                if response.type == "chunk":
                    if response.context_id == ctx1._context_id:
                        audio1.append(response.audio)
                    elif response.context_id == ctx2._context_id:
                        audio2.append(response.audio)
                elif response.type == "done":
                    if response.context_id in active:
                        active.remove(response.context_id)
                    if not active:
                        break

            await asyncio.gather(send_task1, send_task2)

            _validate_audio_response(b"".join(audio1), DEFAULT_OUTPUT_FORMAT)
            _validate_audio_response(b"".join(audio2), DEFAULT_OUTPUT_FORMAT)


# ============================================================================
# TTS Infill Tests
# ============================================================================


def test_tts_infill(client: Cartesia, sample_audio_path: str):
    """Test TTS infill generation."""
    logger.info("Testing tts.infill")

    from pathlib import Path

    # Can pass file paths directly (as Path objects)
    response = client.tts.infill(
        model_id=DEFAULT_MODEL_ID,
        transcript="This is the infill text.",
        voice_id=SAMPLE_VOICE_ID,
        language=SAMPLE_LANGUAGE,
        left_audio=Path(sample_audio_path),
        right_audio=Path(sample_audio_path),
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    )

    audio_data = b"".join(response.iter_bytes())
    _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


# ============================================================================
# Multilingual Tests
# ============================================================================


@pytest.mark.parametrize("language", ["en", "es", "fr", "de", "ja", "pt", "zh"])
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_multilingual_tts(client: Cartesia, language: str):
    """Test TTS with different languages."""
    logger.info(f"Testing TTS with language: {language}")

    response = client.tts.generate(
        model_id=DEFAULT_MODEL_ID,
        transcript=SAMPLE_TRANSCRIPT,
        voice={"mode": "id", "id": SAMPLE_VOICE_ID},
        output_format=DEFAULT_OUTPUT_FORMAT,
        language=language,
    )

    audio_data = b"".join(response.iter_bytes())
    _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)


# ============================================================================
# Error Handling Tests
# ============================================================================


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_tts_invalid_voice_id(client: Cartesia):
    """Test that invalid voice ID returns an error."""
    logger.info("Testing error handling for invalid voice ID")

    with pytest.raises(Exception):
        client.tts.generate(
            model_id=DEFAULT_MODEL_ID,
            transcript=SAMPLE_TRANSCRIPT,
            voice={"mode": "id", "id": "invalid-voice-id"},
            output_format=DEFAULT_OUTPUT_FORMAT,
        )


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_get_nonexistent_voice(client: Cartesia):
    """Test that getting a nonexistent voice returns an error."""
    logger.info("Testing error handling for nonexistent voice")

    with pytest.raises(Exception):
        client.voices.get("nonexistent-voice-id")


# ============================================================================
# STT Tests (if available)
# ============================================================================


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
def test_stt_batch_transcription(client: Cartesia, sample_audio_path: str):
    """Test batch STT transcription."""
    logger.info("Testing stt.transcribe")

    try:
        with open(sample_audio_path, "rb") as audio_file:
            response = client.stt.transcribe(
                file=audio_file,
                model="ink-whisper",
                language="en",
            )

        assert hasattr(response, "text")
        assert isinstance(response.text, str)
        assert len(response.text.strip()) > 0
        logger.info(f"Transcribed: {response.text}")

    except Exception as e:
        # STT might not be available for all API keys
        if "not found" in str(e).lower() or "not available" in str(e).lower():
            pytest.skip("STT not available for this API key")
        raise


# ============================================================================
# Voice Embedding Tests
# ============================================================================




# ============================================================================
# Concurrent Request Tests
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
@pytest.mark.filterwarnings("ignore::ResourceWarning")
async def test_concurrent_tts_requests():
    """Test multiple concurrent TTS requests."""
    logger.info("Testing concurrent TTS requests")

    async def make_request(client, num):
        logger.info(f"Concurrent request {num} starting")
        response = await client.tts.generate(
            model_id=DEFAULT_MODEL_ID,
            transcript=f"This is request number {num}.",
            voice={"mode": "id", "id": SAMPLE_VOICE_ID},
            output_format=DEFAULT_OUTPUT_FORMAT,
            language=SAMPLE_LANGUAGE,
        )
        chunks = []
        async for chunk in response.iter_bytes():
            chunks.append(chunk)
        return b"".join(chunks)

    async with create_async_client() as client:
        tasks = [make_request(client, i) for i in range(4)]
        results = await asyncio.gather(*tasks)

        for i, audio_data in enumerate(results):
            _validate_audio_response(audio_data, DEFAULT_OUTPUT_FORMAT)
            logger.info(f"Request {i} completed with {len(audio_data)} bytes")


