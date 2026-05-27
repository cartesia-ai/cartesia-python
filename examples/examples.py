"""
Examples for Cartesia Python SDK v3.x

Run an example:
    uv sync && CARTESIA_API_KEY=... uv run examples/examples.py <functionName>
"""

from __future__ import annotations

from typing_extensions import TYPE_CHECKING

from cartesia import Cartesia

if TYPE_CHECKING:
    from cartesia.types import Voice, VoiceMetadata

# =============================================================================
# Client Initialization
# =============================================================================


def create_client() -> Cartesia:
    import os

    client = Cartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    return client


def tts_generate_to_file(client: Cartesia) -> None:
    """Use generate() and write_to_file() to write a wav file."""
    response = client.tts.generate(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )
    response.write_to_file("output.wav")
    print(f"Saved audio to output.wav")
    print(f"Play with: ffplay -f wav output.wav")


def tts_bytes_to_file(client: Cartesia) -> None:
    """Backwards compatibility: use the bytes() method to write a wav file."""
    response = client.tts.bytes(  # pyright: ignore[reportDeprecated]
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )
    with open("output.wav", "wb") as f:
        for chunk in response:
            f.write(chunk)
    print(f"Saved audio to output.wav")
    print(f"Play with: ffplay -f wav output.wav")


# =============================================================================
# TTS SSE (Server-Sent Events)
# =============================================================================


def tts_sse_basic(client: Cartesia) -> None:
    """Basic SSE streaming."""
    stream = client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )

    import datetime

    filename = f"tts_sse_basic_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        for event in stream:
            if event.type == "chunk":
                # v3.x returns raw bytes in event.audio
                if event.audio:
                    f.write(event.audio)
            elif event.type == "done":
                break
            elif event.type == "error":
                raise Exception(f"{event.title}: {event.message}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


def tts_sse_with_timestamps(client: Cartesia) -> None:
    """SSE streaming with word timestamps."""
    stream = client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
        add_timestamps=True,
    )

    import datetime

    filename = f"tts_sse_with_timestamps_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        for event in stream:
            if event.type == "timestamps":
                wt = event.word_timestamps
                if wt:
                    print(f"Words: {wt.words}, Starts: {wt.start}, Ends: {wt.end}")
            elif event.type == "chunk":
                if event.audio:
                    f.write(event.audio)
            elif event.type == "done":
                break
            elif event.type == "error":
                raise Exception(f"{event.title}: {event.message}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


def tts_sse_with_phoneme_timestamps(client: Cartesia) -> None:
    """SSE streaming with phoneme timestamps."""
    stream = client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
        add_phoneme_timestamps=True,
    )

    import datetime

    filename = f"tts_sse_with_phoneme_timestamps_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        for event in stream:
            if event.type == "phoneme_timestamps":
                pt = event.phoneme_timestamps
                if pt:
                    print(f"Phonemes: {pt.phonemes}, Starts: {pt.start}, Ends: {pt.end}")
            elif event.type == "chunk":
                if event.audio:
                    f.write(event.audio)
            elif event.type == "done":
                break
            elif event.type == "error":
                raise Exception(f"{event.title}: {event.message}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


def tts_sse_with_match(client: Cartesia) -> None:
    """SSE streaming using match statement."""
    stream = client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )

    import datetime

    filename = f"tts_sse_with_match_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        for event in stream:
            if event.type == "chunk":
                # Audio chunk - event.audio contains bytes
                if event.audio:
                    f.write(event.audio)
            elif event.type == "timestamps":
                # Word timestamps - event.word_timestamps
                print("got timestamps")
            elif event.type == "done":
                # Stream complete
                break
            elif event.type == "error":
                # Error occurred
                raise Exception(f"{event.title}: {event.message}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


# =============================================================================
# TTS WebSocket
# =============================================================================


def tts_websocket_basic(client: Cartesia) -> None:
    """Basic WebSocket usage with websocket_connect() context manager."""
    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )
        ctx.push("Hello, world!")
        ctx.no_more_inputs()

        import datetime

        filename = f"tts_websocket_basic_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        # Write chunks to file as they arrive.
        # You could also send chunks over the network, play them in real-time, etc.
        with open(filename, "wb") as f:
            for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with:\n  $ ffplay -f s16le -ar 44100 {filename}")


def tts_websocket_continuations(client: Cartesia) -> None:
    """Streaming a transcript split into multiple parts, using continuations.
    Useful for streaming transcripts generated by an LLM."""
    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 44100,
            },
            language="en",
        )

        for part in ["The road ", "goes ever ", "on and ", "on."]:
            ctx.push(part)

        ctx.no_more_inputs()

        import datetime

        filename = f"tts_websocket_continuations_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        # Write chunks to file as they arrive.
        # You could also send chunks over the network, play them in real-time, etc.
        with open(filename, "wb") as f:
            for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with:\n  $ ffplay -f s16le -ar 44100 {filename}")


def tts_websocket_flushing(client: Cartesia) -> None:
    """Demonstrates manual flushing to separate audio from different transcripts."""
    from typing_extensions import IO

    transcripts = ["Stay hungry, ", "stay foolish."]

    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )  # Auto-generates context_id

        # 1. Send first transcript
        print("Sending first transcript...")
        ctx.push(transcripts[0])

        # 2. Flush! This forces all buffered audio for the first transcript to be generated
        # and increments the flush_id counter on the server.
        print("Flushing...")
        ctx.push("", flush=True)

        # 3. Send second transcript
        print("Sending second transcript...")
        ctx.push(transcripts[1])

        ctx.no_more_inputs()

        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # We'll save audio to separate files based on flush_id
        files: dict[int, IO[bytes]] = {}

        for response in ctx.receive():
            if response.type == "chunk" and response.audio:
                # Get flush_id from response (defaults to 0 if not present)
                flush_id = response.flush_id or 0

                if flush_id not in files:
                    filename = f"tts_flush_{flush_id}_{timestamp}.pcm"
                    files[flush_id] = open(filename, "wb")
                    print(f"Created new file for flush_id {flush_id}: {filename}")

                files[flush_id].write(response.audio)

            elif response.type == "flush_done":
                print(f"Flush done received for flush_id: {response.flush_id}")

            elif response.type == "error":
                print(f"error: {response.message or response.title}")

        # Close all open files
        for f in files.values():
            f.close()

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for flush_id, f in files.items():
            print(f"  Flush ID {flush_id}: ffplay -f s16le -ar 44100 {f.name}")


def tts_websocket_emotion(client: Cartesia) -> None:
    """Demonstrates changing emotion mid-stream using generation_config."""
    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )

        print("Sending neutral text...")
        ctx.push("Well maybe if you just ")

        print("Sending angry text...")
        ctx.push("loosen up a little!", generation_config={"emotion": "angry"})

        ctx.no_more_inputs()

        import datetime

        filename = f"tts_emotion_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


def tts_websocket_speed(client: Cartesia) -> None:
    """Demonstrates changing speed mid-stream using generation_config."""

    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )

        print("Sending normal speed text...")
        ctx.push("I am speaking at a normal pace. ")

        print("Sending fast speed text...")
        ctx.push("But now I am speaking much faster!", generation_config={"speed": 1.5})

        ctx.no_more_inputs()

        import datetime

        filename = f"tts_speed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


def tts_websocket_concurrent_receives(client: Cartesia) -> None:
    """Two contexts on one connection, each using ctx.receive() to get their own audio.

    Since sync code can't receive from both contexts concurrently, we collect
    them sequentially — but the lazy-routing in receive() ensures that events
    consumed while reading context 1 are queued for context 2 (and vice-versa).
    """
    from cartesia.types import RawOutputFormatParam

    output_format: RawOutputFormatParam = {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100}

    with client.tts.websocket_connect() as connection:
        ctx1 = connection.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
        )
        ctx2 = connection.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
        )

        # Send to both contexts before receiving
        ctx1.push(
            "Context one is speaking now. This is a longer transcript to ensure that audio chunks from both contexts are interleaved on the wire. The quick brown fox jumps over the lazy dog."
        )
        ctx1.no_more_inputs()

        ctx2.push(
            "Context two has a different message. We want to verify that the routing logic correctly separates the audio streams. Pack my box with five dozen liquor jugs."
        )
        ctx2.no_more_inputs()

        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Receive from ctx1 — any ctx2 events read from the wire get queued
        filename1 = f"tts_concurrent_ctx1_{timestamp}.pcm"
        with open(filename1, "wb") as f:
            for response in ctx1.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        # Receive from ctx2 — picks up queued events first
        filename2 = f"tts_concurrent_ctx2_{timestamp}.pcm"
        with open(filename2, "wb") as f:
            for response in ctx2.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved context 1 audio to {filename1}")
        print(f"Saved context 2 audio to {filename2}")
        print(f"Play with:")
        print(f"  ffplay -f s16le -ar 44100 {filename1}")
        print(f"  ffplay -f s16le -ar 44100 {filename2}")


def tts_websocket_response_handling(client: Cartesia) -> None:
    """WebSocket response type handling."""
    with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )
        ctx.push(
            "Hello, world!",
            continue_=False,  # equivalent to ctx.push() then ctx.no_more_inputs()
        )

        import datetime

        filename = f"tts_websocket_response_handling_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        # Write chunks to file as they arrive.
        # You could also send chunks over the network, play them in real-time, etc.
        with open(filename, "wb") as f:
            for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "timestamps":
                    print("got timestamps")
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

                if response.done:
                    break

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


# =============================================================================
# Voices API
# =============================================================================


def voices_list(client: Cartesia) -> None:
    """List voices with pagination."""
    print("loading page 1...")
    page = client.voices.list()
    voices = list(page.data)

    # loaded 1 page
    print("loaded", len(voices))

    for i in range(2, 4):
        if not page.has_next_page():
            break
        print(f"loading page {i}...")
        page = page.get_next_page()
        voices.extend(page.data)
        print("loaded", len(voices))

    print([voices[0], "..."])


def voices_get(client: Cartesia, *args: str) -> "Voice":
    """Get a specific voice."""
    voice_id = args[0] if args else "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"
    voice = client.voices.get(voice_id)
    if hasattr(voice, "embedding"):
        voice.embedding = ["..."]  # pyright: ignore[reportAttributeAccessIssue]
    print(voice)
    return voice


def voices_clone(client: Cartesia, *args: str) -> "VoiceMetadata":
    """Clone a voice from an audio clip."""
    import sys

    if len(args) < 2:
        print("Usage: voices_clone <path to audio file> <language> [<name>]")
        print(
            "See https://docs.cartesia.ai/build-with-cartesia/tts-models/latest for supported languages: en, fr, de, es, ..."
        )
        sys.exit(1)
    clip_path, language, *name_parts = args
    name = " ".join(name_parts) if name_parts else "My Voice"
    with open(clip_path, "rb") as clip:
        voice = client.voices.clone(
            clip=clip,
            language=language,
            name=name,
        )
    print(f"Cloned voice: {voice.id}")
    return voice


def voices_update(client: Cartesia, *args: str) -> None:
    """Update a voice."""
    import sys

    if len(args) < 2:
        print("Usage: voices_update <voice_id> <name>")
        sys.exit(1)
    voice_id, *name_parts = args
    voice = client.voices.update(voice_id, name=" ".join(name_parts))
    print(voice)


def voices_delete(client: Cartesia, *args: str) -> None:
    """Delete a voice."""
    import sys

    if not args:
        print("Usage: voices_delete <voice_id>")
        sys.exit(1)
    client.voices.delete(args[0])


# =============================================================================
# Infill API
# =============================================================================


def infill_create(client: Cartesia, *args: str) -> None:
    """Create infill audio between two clips."""
    from pathlib import Path

    if len(args) < 3:
        print("Usage: stt_transcribe <audio_file_before> <audio_file_after> <transcript>")
        sys.exit(1)

    left_file, right_file, *transcript_parts = args

    # Can pass file paths directly (as Path objects)
    response = client.tts.infill(
        model_id="sonic-3",
        language="en",
        transcript=" ".join(transcript_parts),
        left_audio=Path(left_file),
        right_audio=Path(right_file),
        voice_id="6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
    )
    response.write_to_file("infill_output.wav")
    print(f"Saved audio to infill_output.wav")
    print(f"Play with: ffplay -f wav infill_output.wav")


# =============================================================================
# STT (Speech-to-Text)
# =============================================================================


def stt_transcribe(client: Cartesia, *args: str) -> None:
    """Transcribe audio with word timestamps."""
    import sys

    if not args:
        print("Usage: stt_transcribe <file_path>")
        sys.exit(1)
    with open(args[0], "rb") as f:
        response = client.stt.transcribe(
            file=f,
            model="ink-whisper",
            language="en",
            timestamp_granularities=["word"],  # Optional: get word timestamps
        )
    print(response.text)
    if response.words:
        for word in response.words:
            print(f"{word.word}: {word.start}s - {word.end}s")


def stt_turn_detecting_websocket(client: Cartesia, *args: str) -> None:
    """Realtime STT with native turn detection (recommended for voice agents).

    The model signals when a user turn starts and ends, so your agent reacts
    to events rather than running its own VAD.

    Pass a mono uncompressed PCM WAV file (16-bit or 32-bit) as an argument,
    or call with no args to synthesize sample audio via TTS.
    """
    import sys
    import time
    import wave

    from cartesia.types import STTEncoding, RawOutputFormatParam

    encoding: STTEncoding
    chunks: list[bytes]
    if args:
        with wave.open(args[0], "rb") as wf:
            if wf.getnchannels() != 1:
                print(f"Error: WAV must be mono, got {wf.getnchannels()} channels.")
                sys.exit(1)
            if wf.getcomptype() != "NONE":
                print(f"Error: WAV must be uncompressed PCM, got {wf.getcomptype()!r}.")
                sys.exit(1)
            sample_width = wf.getsampwidth()
            if sample_width == 2:
                encoding = "pcm_s16le"
            elif sample_width == 4:
                encoding = "pcm_s32le"
            else:
                print(f"Error: unsupported sample width {sample_width} bytes (expected 2 or 4).")
                sys.exit(1)
            sample_rate = wf.getframerate()
            chunks = []
            while True:
                data = wf.readframes(sample_rate // 10)  # 100ms per chunk
                if not data:
                    break
                chunks.append(data)
    else:
        output_format: RawOutputFormatParam = {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 16000}
        encoding = output_format["encoding"]
        sample_rate = output_format["sample_rate"]
        generation_transcript = "Hello, world! The quick brown fox jumps over the lazy dog."
        print(f"No WAV file provided — synthesizing audio with TTS: {generation_transcript!r}")
        audio = client.tts.generate(
            model_id="sonic-latest",
            transcript=generation_transcript,
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": encoding, "sample_rate": sample_rate},
            language="en",
        ).read()
        chunk_bytes = (sample_rate * 2) // 10  # 100ms of pcm_s16le (2 bytes/sample)
        chunks = [audio[i : i + chunk_bytes] for i in range(0, len(audio), chunk_bytes)]

    # Concatenate transcripts from all turn.end events to get the full transcript
    # Do not strip or add whitespace!
    full_transcript = ""

    with client.stt.turn_detecting.websocket(
        encoding=encoding,
        model="ink-2",
        sample_rate=sample_rate,
    ) as connection:
        for chunk in chunks:
            connection.send_raw(chunk)
            time.sleep(0.1)  # each chunk is 100ms of audio — pace sends to match real time

        # Flush remaining audio and close the session cleanly.
        connection.send({"type": "close"})

        for event in connection:
            if event.type == "connected":
                print(f"connected      | request_id={event.request_id}")
            elif event.type == "turn.start":
                print("turn.start     |")
            elif event.type == "turn.update":
                # event.transcript is cumulative within a turn.
                print(f"turn.update    | {event.transcript}")
            elif event.type == "turn.eager_end":
                print(f"turn.eager_end | {event.transcript}")
            elif event.type == "turn.resume":
                print("turn.resume     |")
            elif event.type == "turn.end":
                print(f"turn.end       | {event.transcript}")
                full_transcript += event.transcript
            elif event.type == "error":
                print(f"error          | {event.message}")

        print(f"\nFull transcript: {full_transcript!r}")


def stt_external_vad_websocket(client: Cartesia, *args: str) -> None:
    """Realtime STT without turn detection (push-to-talk style).

    You control when the model emits transcripts by sending `finalize`.
    Transcript events are deltas — concatenate `text` from `is_final` events
    (without stripping whitespace) to assemble the full transcript.

    Pass a mono uncompressed PCM WAV file (16-bit or 32-bit) as an argument,
    or call with no args to synthesize sample audio via TTS.
    """
    import sys
    import time
    import wave

    from cartesia.types import STTEncoding, RawOutputFormatParam

    encoding: STTEncoding
    chunks: list[bytes]
    if args:
        with wave.open(args[0], "rb") as wf:
            if wf.getnchannels() != 1:
                print(f"Error: WAV must be mono, got {wf.getnchannels()} channels.")
                sys.exit(1)
            if wf.getcomptype() != "NONE":
                print(f"Error: WAV must be uncompressed PCM, got {wf.getcomptype()!r}.")
                sys.exit(1)
            sample_width = wf.getsampwidth()
            if sample_width == 2:
                encoding = "pcm_s16le"
            elif sample_width == 4:
                encoding = "pcm_s32le"
            else:
                print(f"Error: unsupported sample width {sample_width} bytes (expected 2 or 4).")
                sys.exit(1)
            sample_rate = wf.getframerate()
            chunks = []
            while True:
                data = wf.readframes(sample_rate // 10)  # 100ms per chunk
                if not data:
                    break
                chunks.append(data)
    else:
        output_format: RawOutputFormatParam = {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 16000}
        encoding = output_format["encoding"]
        sample_rate = output_format["sample_rate"]
        transcript = "Hello, world! The quick brown fox jumps over the lazy dog."
        print(f"No WAV file provided — synthesizing audio with TTS: {transcript!r}")
        audio = client.tts.generate(
            model_id="sonic-latest",
            transcript=transcript,
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            language="en",
        ).read()
        chunk_bytes = (sample_rate * 2) // 10  # 100ms of pcm_s16le (2 bytes/sample)
        chunks = [audio[i : i + chunk_bytes] for i in range(0, len(audio), chunk_bytes)]

    with client.stt.external_vad.websocket(
        encoding=encoding,
        model="ink-2",
        sample_rate=sample_rate,
    ) as connection:
        for chunk in chunks:
            connection.send_raw(chunk)
            time.sleep(0.1)  # each chunk is 100ms of audio — pace sends to match real time

        # Trigger transcription of buffered audio, then close cleanly.
        connection.send("finalize")
        connection.send("close")

        transcript = ""
        for event in connection:
            if event.type == "transcript":
                if event.is_final:
                    print(f"transcript | {event.text}")
                    transcript += event.text
            elif event.type == "flush_done":
                print("flush_done |")
            elif event.type == "done":
                print("done       |")
            elif event.type == "error":
                print(f"error    | {event.message}")

        print(f"\nFull transcript: {transcript!r}")


# =============================================================================
# Error Handling
# =============================================================================


def error_handling_example(client: Cartesia) -> None:
    """Example of error handling with SDK exceptions."""
    from cartesia import APIError, NotFoundError, RateLimitError, BadRequestError, AuthenticationError

    try:
        client.tts.generate(
            model_id="sonic-latest",
            transcript="",  # empty transcript will cause a 400 bad request response
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )
    except BadRequestError as e:
        print(f"Bad request (expected): {e.message}")
    except AuthenticationError as e:
        print(f"Auth failed: {e.message}")
    except NotFoundError as e:
        print(f"Not found: {e.message}")
    except RateLimitError as e:
        print(f"Rate limited: {e.message}")
    except APIError as e:
        print(f"API error: {e.message}")


if __name__ == "__main__":
    import os
    import sys
    import inspect

    if len(sys.argv) < 2:
        print("Usage: python examples.py <function_name>")
        available_functions = [
            name
            for name, obj in globals().items()
            if inspect.isfunction(obj) and obj.__module__ == __name__ and obj != create_client
        ]
        print(f"Available functions: {', '.join(available_functions)}")
        sys.exit(1)

    func_name = sys.argv[1]
    if func_name not in globals():
        print(f"Error: Function '{func_name}' not found.")
        sys.exit(1)

    func = globals()[func_name]

    api_key = os.environ.get("CARTESIA_API_KEY")
    if not api_key:
        print("Error: CARTESIA_API_KEY environment variable not set.")
        sys.exit(1)

    try:
        client = Cartesia(api_key=api_key)
        func(client, *sys.argv[2:])
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
