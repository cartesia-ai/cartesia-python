"""
Async Examples for Cartesia Python SDK v3.x

Run an example:
    uv sync && CARTESIA_API_KEY=... uv run examples/async_examples.py <functionName>
"""

from __future__ import annotations

from cartesia import (
    AsyncCartesia,
)

# =============================================================================
# TTS Bytes (Async)
# =============================================================================


async def tts_generate_async(client: AsyncCartesia) -> None:
    """Async TTS generation to file."""
    response = await client.tts.generate(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )
    await response.write_to_file("output_async.wav")
    print("Saved audio to output_async.wav")
    print("Play with: ffplay -f wav output_async.wav")


async def tts_bytes_async(client: AsyncCartesia) -> None:
    """Async bytes iterator."""
    response = await client.tts.bytes(  # pyright: ignore[reportDeprecated]
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )

    filename = "output_bytes_async.wav"
    with open(filename, "wb") as f:
        async for chunk in response:
            f.write(chunk)

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f wav {filename}")


# =============================================================================
# TTS SSE (Async)
# =============================================================================


async def tts_sse_basic_async(client: AsyncCartesia) -> None:
    """Async SSE streaming."""
    import datetime

    stream = await client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
    )

    filename = f"tts_sse_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        async for event in stream:
            if event.type == "chunk":
                if event.audio:
                    f.write(event.audio)
            elif event.type == "done":
                break
            elif event.type == "error":
                raise Exception(f"{event.title}: {event.message}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


async def tts_sse_with_timestamps_async(client: AsyncCartesia) -> None:
    """Async SSE streaming with timestamps."""
    import datetime

    stream = await client.tts.generate_sse(
        model_id="sonic-latest",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        language="en",
        add_timestamps=True,
    )

    filename = f"tts_sse_timestamps_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

    with open(filename, "wb") as f:
        async for event in stream:
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


# =============================================================================
# TTS WebSocket (Async)
# =============================================================================


async def tts_websocket_basic_async(client: AsyncCartesia) -> None:
    """Async WebSocket usage with websocket_connect()."""
    import datetime

    async with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )
        await ctx.push("Hello, world!")
        await ctx.no_more_inputs()

        filename = f"tts_ws_basic_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


async def tts_websocket_continuations_async(client: AsyncCartesia) -> None:
    """Async streaming multiple transcripts with continuations."""
    import datetime

    transcripts = ["The only thing we have to fear ", "is ", "fear itself."]

    async with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
        )

        for transcript in transcripts:
            await ctx.push(transcript)

        await ctx.no_more_inputs()

        filename = f"tts_ws_continuations_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


async def tts_websocket_flushing_async(client: AsyncCartesia) -> None:
    """Async manual flushing example."""
    from typing_extensions import IO

    transcripts = ["First transcript.", "Second transcript."]

    async with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )

        # 1. Send first transcript
        print("Sending first transcript...")
        await ctx.push(transcripts[0])

        # 2. Flush!
        print("Flushing...")
        await ctx.push("", flush=True)

        # 3. Send second transcript
        print("Sending second transcript...")
        await ctx.push(transcripts[1])

        await ctx.no_more_inputs()

        import datetime

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        files: dict[int, IO[bytes]] = {}

        async for response in ctx.receive():
            if response.type == "chunk" and response.audio:
                flush_id = response.flush_id or 0

                if flush_id not in files:
                    filename = f"tts_flush_async_{flush_id}_{timestamp}.pcm"
                    files[flush_id] = open(filename, "wb")
                    print(f"Created new file for flush_id {flush_id}: {filename}")

                files[flush_id].write(response.audio)

            elif response.type == "flush_done":
                print(f"Flush done received for flush_id: {response.flush_id}")

            elif response.type == "error":
                print(f"error: {response.message or response.title}")

        for f in files.values():
            f.close()

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for flush_id, f in files.items():
            print(f"  Flush ID {flush_id}: ffplay -f s16le -ar 44100 {f.name}")


async def tts_websocket_emotion_async(client: AsyncCartesia) -> None:
    """Async emotion changing example."""

    async with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )

        print("Sending neutral text...")
        await ctx.push("Well maybe if you just ")

        print("Sending angry text...")
        await ctx.push("loosen up a little!", generation_config={"emotion": "angry"})

        await ctx.no_more_inputs()

        import datetime

        filename = f"tts_emotion_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


async def tts_websocket_speed_async(client: AsyncCartesia) -> None:
    """Async speed changing example."""

    async with client.tts.websocket_connect() as ws:
        ctx = ws.context(
            model_id="sonic-latest",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100},
            language="en",
        )

        print("Sending normal speed text...")
        await ctx.push("I am speaking at a normal pace. ")

        print("Sending fast speed text...")
        await ctx.push("But now I am speaking much faster!", generation_config={"speed": 1.5})

        await ctx.no_more_inputs()

        import datetime

        filename = f"tts_speed_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.type == "error":
                    print(f"error: {response.message or response.title}")

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f s16le -ar 44100 {filename}")


async def tts_websocket_concurrent_receives_async(client: AsyncCartesia) -> None:
    """Two contexts on one connection, each using ctx.receive() concurrently via tasks.

    The lazy-routing in receive() ensures that whichever task happens to read an
    event from the wire routes it to the correct context's queue.
    """
    import asyncio
    import datetime

    from cartesia.types import RawOutputFormatParam
    from cartesia.resources.tts import AsyncWebSocketContext

    output_format: RawOutputFormatParam = {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100}

    async with client.tts.websocket_connect() as connection:
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

        # Send to both contexts
        await ctx1.push(
            "Context one is speaking now. This is a longer transcript to ensure that audio chunks from both contexts are interleaved on the wire. The quick brown fox jumps over the lazy dog."
        )
        await ctx1.no_more_inputs()

        await ctx2.push(
            "Context two has a different message. We want to verify that the routing logic correctly separates the audio streams. Pack my box with five dozen liquor jugs."
        )
        await ctx2.no_more_inputs()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Receive concurrently via tasks, writing to files
        async def collect(ctx: AsyncWebSocketContext, filename: str) -> None:
            with open(filename, "wb") as f:
                async for response in ctx.receive():
                    if response.type == "chunk" and response.audio:
                        f.write(response.audio)
                    elif response.type == "error":
                        print(f"error: {response.message or response.title}")

        filename1 = f"tts_concurrent_async_ctx1_{timestamp}.pcm"
        filename2 = f"tts_concurrent_async_ctx2_{timestamp}.pcm"

        await asyncio.gather(
            collect(ctx1, filename1),
            collect(ctx2, filename2),
        )

        print(f"Saved context 1 audio to {filename1}")
        print(f"Saved context 2 audio to {filename2}")
        print(f"Play with:")
        print(f"  ffplay -f s16le -ar 44100 {filename1}")
        print(f"  ffplay -f s16le -ar 44100 {filename2}")


async def tts_async_concurrent_contexts(client: AsyncCartesia) -> None:
    """
    Demonstrates using a single WebSocket connection to manage multiple contexts concurrently.

    We spawn separate sender and receiver tasks per context. The connection runs a
    background listener that routes events into per-context queues, and each
    ``ctx.receive()`` iterator drains its own queue.
    """
    import asyncio
    import datetime

    from cartesia.resources.tts import AsyncWebSocketContext

    output_format = {"container": "raw", "encoding": "pcm_s16le", "sample_rate": 44100}
    voice_id = "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"  # Standard voice

    async with client.tts.websocket_connect() as connection:
        # Create 3 contexts
        contexts: list[AsyncWebSocketContext] = []
        for i in range(3):
            ctx = connection.context(
                model_id="sonic-latest", voice={"mode": "id", "id": voice_id}, output_format=output_format
            )
            contexts.append(ctx)
            print(f"Created context {i}: {ctx._context_id}")

        async def send_transcript(ctx_index: int, ctx: AsyncWebSocketContext) -> None:
            all_quotes = [
                ["Ask not what your country can do for you, ", "ask what you can do ", "for your country."],
                ["I have a dream ", "that one day this nation ", "will rise up."],
                ["In the end, it's not the years in your life that count. ", "It's the life ", "in your years."],
            ]
            transcripts = all_quotes[ctx_index]
            for part in transcripts:
                print(f"Sending '{part.strip()}' to context {ctx_index}")
                await ctx.push(part)
                # Small delay to simulate real-time input and interleave requests
                await asyncio.sleep(0.1)

            await ctx.no_more_inputs()
            print(f"Finished sending to context {ctx_index}")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filenames: dict[str, str] = {}

        async def receive_for(ctx_index: int, ctx: AsyncWebSocketContext) -> None:
            filename = f"tts_concurrent_{ctx_index}_{timestamp}.pcm"
            filenames[ctx._context_id or ""] = filename
            file_created = False
            with open(filename, "wb") as f:
                async for event in ctx.receive():
                    if event.type == "chunk" and event.audio:
                        if not file_created:
                            print(f"Created file for context {ctx_index}: {filename}")
                            file_created = True
                        f.write(event.audio)
                    elif event.type == "done":
                        print(f"Context {ctx._context_id} finished.")
                        return
                    elif event.type == "error":
                        raise RuntimeError(f"Context {ctx_index} error: {getattr(event, 'error', 'Unknown')}")

        send_tasks = [asyncio.create_task(send_transcript(i, ctx)) for i, ctx in enumerate(contexts)]
        recv_tasks = [asyncio.create_task(receive_for(i, ctx)) for i, ctx in enumerate(contexts)]

        await asyncio.gather(*send_tasks, *recv_tasks)
        print("All contexts finished.")

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for ctx_id, filename in filenames.items():
            ctx_idx = next((i for i, c in enumerate(contexts) if c._context_id == ctx_id), "unknown")
            print(f"  Context {ctx_idx}: ffplay -f s16le -ar 44100 {filename}")


# =============================================================================
# STT Realtime WebSockets (Async)
# =============================================================================


async def stt_turn_detecting_websocket_async(client: AsyncCartesia, *args: str) -> None:
    """Async realtime STT with native turn detection (recommended for voice agents).

    The model signals when a user turn starts and ends, so your agent reacts
    to events rather than running its own VAD.

    Streams audio and receives events concurrently using ``asyncio.gather`` —
    the realistic pattern for real-time agents.

    Pass a mono uncompressed PCM WAV file (16-bit or 32-bit) as an argument,
    or call with no args to synthesize sample audio via TTS.
    """
    import sys
    import wave
    import asyncio

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
                encoding = "pcm_s16le"
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
        tts_response = await client.tts.generate(
            model_id="sonic-latest",
            transcript=transcript,
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            language="en",
        )
        audio = await tts_response.read()
        chunk_bytes = (sample_rate * 2) // 10  # 100ms of pcm_s16le (2 bytes/sample)
        chunks = [audio[i : i + chunk_bytes] for i in range(0, len(audio), chunk_bytes)]

    async with client.stt.turn_detecting.websocket(
        encoding=encoding,
        model="ink-2",
        sample_rate=sample_rate,
    ) as connection:

        async def send_audio() -> None:
            for chunk in chunks:
                await connection.send_raw(chunk)
                # Pace at real-time (100ms per chunk)
                await asyncio.sleep(0.1)
            # Flush remaining audio and close the session.
            await connection.send({"type": "close"})

        async def receive_events() -> None:
            async for event in connection:
                if event.type == "connected":
                    print(f"Connected: {event.request_id}")
                elif event.type == "turn.start":
                    print("Turn started")
                elif event.type == "turn.update":
                    print(f"  {event.transcript}")
                elif event.type == "turn.eager_end":
                    print(f"[preview] Eager end: {event.transcript!r}")
                elif event.type == "turn.resume":
                    print("[preview] Turn resumed")
                elif event.type == "turn.end":
                    print(f"Turn ended: {event.transcript!r}")
                elif event.type == "error":
                    print(f"Error: {event.title}: {event.message}")

        await asyncio.gather(send_audio(), receive_events())


async def stt_external_vad_websocket_async(client: AsyncCartesia, *args: str) -> None:
    """Async realtime STT without turn detection (push-to-talk style).

    You control when the model emits transcripts by sending `finalize`.
    Transcript events are deltas — concatenate `text` from `is_final` events
    (without stripping whitespace) to assemble the full transcript.

    Pass a mono uncompressed PCM WAV file (16-bit or 32-bit) as an argument,
    or call with no args to synthesize sample audio via TTS.
    """
    import sys
    import wave
    import asyncio

    from cartesia.types import STTEncoding, RawOutputFormatParam

    encoding: STTEncoding
    sample_rate: int
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
        tts_response = await client.tts.generate(
            model_id="sonic-latest",
            transcript=transcript,
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            language="en",
        )
        audio = await tts_response.read()
        chunk_bytes = (sample_rate * 2) // 10  # 100ms of pcm_s16le (2 bytes/sample)
        chunks = [audio[i : i + chunk_bytes] for i in range(0, len(audio), chunk_bytes)]

    transcript = ""

    async with client.stt.external_vad.websocket(
        encoding=encoding,
        model="ink-whisper",
        sample_rate=sample_rate,
    ) as connection:

        async def send_audio() -> None:
            for chunk in chunks:
                await connection.send_raw(chunk)
                await asyncio.sleep(0.1)
            # Trigger transcription of buffered audio, then close cleanly.
            await connection.send("finalize")
            await connection.send("close")

        async def receive_events() -> None:
            nonlocal transcript
            async for event in connection:
                if event.type == "transcript":
                    label = "final" if event.is_final else "interim"
                    print(f"[{label}] {event.text!r}")
                    if event.is_final:
                        transcript += event.text
                elif event.type == "flush_done":
                    print("Flush acknowledged")
                elif event.type == "done":
                    print("Connection closing")
                elif event.type == "error":
                    print(f"Error: {event.title}: {event.message}")

        await asyncio.gather(send_audio(), receive_events())

    print(f"\nFull transcript: {transcript!r}")


# =============================================================================
# Infill API (Async)
# =============================================================================


async def infill_create_async(client: AsyncCartesia, *args: str) -> None:
    """Async infill creation."""
    import sys
    from pathlib import Path

    if len(args) < 3:
        print("Usage: infill_create_async <audio_file_before> <audio_file_after> <transcript>")
        sys.exit(1)

    left_file, right_file, *transcript_parts = args

    response = await client.tts.infill(
        model_id="sonic-3",
        language="en",
        transcript=" ".join(transcript_parts),
        left_audio=Path(left_file),
        right_audio=Path(right_file),
        voice_id="6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
        output_format={"container": "wav", "encoding": "pcm_s16le", "sample_rate": 44100},
    )
    await response.write_to_file("infill_output_async.wav")
    print("Saved audio to infill_output_async.wav")
    print("Play with: ffplay -f wav infill_output_async.wav")


if __name__ == "__main__":
    import os
    import sys
    import asyncio
    import inspect

    if len(sys.argv) < 2:
        print("Usage: python async_examples.py <function_name>")
        available_functions = [
            name for name, obj in globals().items() if inspect.iscoroutinefunction(obj) and obj.__module__ == __name__
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

    async def run() -> None:
        async with AsyncCartesia(api_key=api_key) as client:
            await func(client, *sys.argv[2:])

    try:
        asyncio.run(run())
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
