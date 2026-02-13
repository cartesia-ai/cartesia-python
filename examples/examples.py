"""
Examples for Cartesia Python SDK v3.x

These examples are extracted from MIGRATING.md for type inspection in editors.
"""

from __future__ import annotations

from typing import IO

from cartesia import (
    APIError,
    Cartesia,
    NotFoundError,
    RateLimitError,
    BadRequestError,
    AuthenticationError,
)

# =============================================================================
# Client Initialization
# =============================================================================

def create_client():
    client = Cartesia(api_key="your-api-key")
    return client


# =============================================================================
# TTS Bytes (Synchronous Generation)
# =============================================================================

def tts_generate_to_file(client: Cartesia):
    """Use generate() and write_to_file() to write a wav file."""
    response = client.tts.generate(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    )
    response.write_to_file("output.wav")
    print(f"Saved audio to output.wav")
    print(f"Play with: ffplay -f wav output.wav")


def tts_bytes_to_file(client: Cartesia):
    """Backwards compatibility: use the bytes() method to write a wav file."""
    response = client.tts.bytes(  # pyright: ignore[reportDeprecated]
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    )
    with open("output.wav", "wb") as f:
        for chunk in response:
            f.write(chunk)
    print(f"Saved audio to output.wav")
    print(f"Play with: ffplay -f wav output.wav")


# =============================================================================
# TTS SSE (Server-Sent Events)
# =============================================================================

def tts_sse_basic(client: Cartesia):
    """Basic SSE streaming."""
    stream = client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
                raise Exception(f"Error: {event.error}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def tts_sse_with_timestamps(client: Cartesia):
    """SSE streaming with word timestamps."""
    stream = client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
                raise Exception(f"Error: {event.error}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def tts_sse_with_phoneme_timestamps(client: Cartesia):
    """SSE streaming with phoneme timestamps."""
    stream = client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
                raise Exception(f"Error: {event.error}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def tts_sse_with_match(client: Cartesia):
    """SSE streaming using match statement."""
    stream = client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    )

    import datetime
    filename = f"tts_sse_with_match_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        for event in stream:
            if event.type == "chunk":
                # Audio chunk - event.audio contains bytes
                if event.audio:
                    f.write(event.audio)
                    process_audio(event.audio)
            elif event.type == "timestamps":
                # Word timestamps - event.word_timestamps
                process_timestamps(event.word_timestamps)
            elif event.type == "done":
                # Stream complete
                break
            elif event.type == "error":
                # Error occurred
                raise Exception(event.error)

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def process_audio(audio: bytes) -> None:
    pass


def process_timestamps(timestamps: object) -> None:
    pass


# =============================================================================
# TTS WebSocket
# =============================================================================

def tts_websocket_basic(client: Cartesia):
    """Basic WebSocket usage with websocket_connect() context manager."""
    with client.tts.websocket_connect() as connection:
        connection.send({
            "model_id": "sonic-3",
            "transcript": "Hello, world!",
            "voice": {"mode": "id", "id": "voice-id"},
            "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        })

        import datetime
        filename = f"tts_websocket_basic_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        # Write chunks to file as they arrive.
        # You could also send chunks over the network, play them in real-time, etc.
        with open(filename, "wb") as f:
            for response in connection:
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.done:
                    break

        print(f"Saved audio to {filename}")
        print(f"Play with:\n  $ ffplay -f f32le -ar 44100 {filename}")


def tts_websocket_continuations(client: Cartesia):
    """Streaming a transcript split into multiple parts, using continuations.
    Useful for streaming transcripts generated by an LLM."""
    with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={
                "container": "raw",
                "encoding": "pcm_f32le",
                "sample_rate": 44100,
            },
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

        print(f"Saved audio to {filename}")
        print(f"Play with:\n  $ ffplay -f f32le -ar 44100 {filename}")


def tts_websocket_flushing(client: Cartesia):
    """Demonstrates manual flushing to separate audio from different transcripts."""
    transcripts = ["Stay hungry, ", "stay foolish."]
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format
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
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

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

        # Close all open files
        for f in files.values():
            f.close()

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for flush_id, f in files.items():
            print(f"  Flush ID {flush_id}: ffplay -f f32le -ar 44100 {f.name}")


def tts_websocket_emotion(client: Cartesia):
    """Demonstrates changing emotion mid-stream using generation_config."""
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format
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

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def tts_websocket_speed(client: Cartesia):
    """Demonstrates changing speed mid-stream using generation_config."""
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format
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

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


def tts_websocket_response_handling(client: Cartesia):
    """WebSocket response type handling."""
    with client.tts.websocket_connect() as connection:
        connection.send({
            "model_id": "sonic-3",
            "transcript": "Hello, world!",
            "voice": {"mode": "id", "id": "voice-id"},
            "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        })

        import datetime
        filename = f"tts_websocket_response_handling_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        # Write chunks to file as they arrive.
        # You could also send chunks over the network, play them in real-time, etc.
        with open(filename, "wb") as f:
            for response in connection:
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "timestamps":
                    process_timestamps(response.word_timestamps)
                elif response.type == "done" or response.done:
                    break
                elif response.type == "error":
                    raise Exception(response.error)

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


# =============================================================================
# Voices API
# =============================================================================

def voices_list(client: Cartesia):
    """List voices with pagination."""
    voices = client.voices.list(limit=10)
    for voice in voices:
        print(voice.name)


def voices_get(client: Cartesia):
    """Get a specific voice."""
    voice = client.voices.get("voice-id")
    return voice


def voices_clone(client: Cartesia):
    """Clone a voice from an audio clip."""
    with open("sample.wav", "rb") as clip:
        voice = client.voices.clone(
            clip=clip,
            name="My Voice",
            description="A custom voice",
            language="en",
        )
    return voice


def voices_update(client: Cartesia, voice_id: str):
    """Update a voice."""
    client.voices.update(
        voice_id,
        name="Updated Name",
        description="Updated description",
    )


def voices_delete(client: Cartesia, voice_id: str):
    """Delete a voice."""
    client.voices.delete(voice_id)


# =============================================================================
# Infill API
# =============================================================================

def infill_create(client: Cartesia):
    """Create infill audio between two clips."""
    from pathlib import Path
    # Can pass file paths directly (as Path objects)
    response = client.tts.infill(
        model_id="sonic-3",
        language="en",
        transcript="Infill text",
        left_audio=Path("left.wav"),
        right_audio=Path("right.wav"),
        voice_id="6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    )
    response.write_to_file("infill_output.wav")
    print(f"Saved audio to infill_output.wav")
    print(f"Play with: ffplay -f wav infill_output.wav")


# =============================================================================
# STT (Speech-to-Text)
# =============================================================================

def stt_transcribe(client: Cartesia):
    """Transcribe audio with word timestamps."""
    with open("audio.wav", "rb") as f:
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


# =============================================================================
# Error Handling
# =============================================================================

def error_handling_example(client: Cartesia):
    """Example of error handling with SDK exceptions."""
    try:
        _response = client.tts.generate(
            model_id="sonic-3",
            transcript="Hello, world!",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
        )
    except BadRequestError as e:
        print(f"Bad request: {e}")
    except AuthenticationError as e:
        print(f"Auth failed: {e}")
    except NotFoundError as e:
        print(f"Not found: {e}")
    except RateLimitError as e:
        print(f"Rate limited: {e}")
    except APIError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    import os
    import sys
    import inspect

    if len(sys.argv) < 2:
        print("Usage: python examples.py <function_name>")
        available_functions = [name for name, obj in globals().items()
                             if inspect.isfunction(obj) and obj.__module__ == __name__]
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

    # Allow overriding version via env var (helpful if default version has issues)
    extra_headers: dict[str, str] = {}
    cartesia_version = os.environ.get("CARTESIA_VERSION")
    if cartesia_version:
        extra_headers["Cartesia-Version"] = cartesia_version

    try:
        client = Cartesia(api_key=api_key, default_headers=extra_headers)
        func(client)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
