"""
Async Examples for Cartesia Python SDK v3.x
"""

from __future__ import annotations

import asyncio
import datetime
from typing import IO

from cartesia import (
    AsyncCartesia,
)
from cartesia.resources.tts import AsyncTTSWSContext

# =============================================================================
# TTS Bytes (Async)
# =============================================================================


async def tts_generate_async(client: AsyncCartesia) -> None:
    """Async TTS generation to file."""
    response = await client.tts.generate(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
        language="en",
    )
    await response.write_to_file("output_async.wav")
    print("Saved audio to output_async.wav")
    print("Play with: ffplay -f wav output_async.wav")


async def tts_bytes_async(client: AsyncCartesia) -> None:
    """Async bytes iterator."""
    response = await client.tts.bytes(  # pyright: ignore[reportDeprecated]
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
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
    stream = await client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


async def tts_sse_with_timestamps_async(client: AsyncCartesia) -> None:
    """Async SSE streaming with timestamps."""
    stream = await client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


# =============================================================================
# TTS WebSocket (Async)
# =============================================================================


async def tts_websocket_basic_async(client: AsyncCartesia) -> None:
    """Async WebSocket usage with contexts_ws()."""
    async with client.tts.contexts_ws() as ws:
        ctx = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )
        await ctx.push("Hello, world!")
        await ctx.end()

        filename = f"tts_ws_basic_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.done:
                    break

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


async def tts_websocket_continuations_async(client: AsyncCartesia) -> None:
    """Async streaming multiple transcripts with continuations."""
    transcripts = ["The only thing we have to fear ", "is ", "fear itself."]

    async with client.tts.contexts_ws() as ws:
        ctx = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        )

        for transcript in transcripts:
            await ctx.push(transcript)

        await ctx.end()

        filename = f"tts_ws_continuations_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


async def tts_websocket_flushing_async(client: AsyncCartesia) -> None:
    """Async manual flushing example."""
    transcripts = ["First transcript.", "Second transcript."]

    async with client.tts.contexts_ws() as ws:
        ctx = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )

        # 1. Send first transcript
        print("Sending first transcript...")
        await ctx.push(transcripts[0])

        # 2. Flush!
        print("Flushing...")
        await ctx.flush()

        # 3. Send second transcript
        print("Sending second transcript...")
        await ctx.push(transcripts[1])

        await ctx.end()

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

        for f in files.values():
            f.close()

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for flush_id, f in files.items():
            print(f"  Flush ID {flush_id}: ffplay -f f32le -ar 44100 {f.name}")


async def tts_websocket_emotion_async(client: AsyncCartesia) -> None:
    """Async emotion changing example."""

    async with client.tts.contexts_ws() as ws:
        ctx = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )

        print("Sending neutral text...")
        await ctx.push("Well maybe if you just ")

        print("Sending angry text...")
        await ctx.push("loosen up a little!", generation_config={"emotion": "angry"})

        await ctx.end()

        import datetime

        filename = f"tts_emotion_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


async def tts_websocket_speed_async(client: AsyncCartesia) -> None:
    """Async speed changing example."""

    async with client.tts.contexts_ws() as ws:
        ctx = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )

        print("Sending normal speed text...")
        await ctx.push("I am speaking at a normal pace. ")

        print("Sending fast speed text...")
        await ctx.push("But now I am speaking much faster!", generation_config={"speed": 1.5})

        await ctx.end()

        import datetime

        filename = f"tts_speed_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")


async def tts_websocket_concurrent_receives_async(client: AsyncCartesia) -> None:
    """Two contexts on one connection, each using ctx.receive() concurrently via tasks.

    The lazy-routing in receive() ensures that whichever task happens to read an
    event from the wire routes it to the correct context's queue.
    """

    async with client.tts.contexts_ws() as ws:
        ctx1 = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )
        ctx2 = await ws.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
            language="en",
        )

        # Send to both contexts
        await ctx1.push(
            "Context one is speaking now. This is a longer transcript to ensure that audio chunks from both contexts are interleaved on the wire. The quick brown fox jumps over the lazy dog."
        )
        await ctx1.end()

        await ctx2.push(
            "Context two has a different message. We want to verify that the routing logic correctly separates the audio streams. Pack my box with five dozen liquor jugs."
        )
        await ctx2.end()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Receive concurrently via tasks, writing to files
        async def collect(ctx: AsyncTTSWSContext, filename: str) -> None:
            with open(filename, "wb") as f:
                async for response in ctx.receive():
                    if response.type == "chunk" and response.audio:
                        f.write(response.audio)

        filename1 = f"tts_concurrent_async_ctx1_{timestamp}.pcm"
        filename2 = f"tts_concurrent_async_ctx2_{timestamp}.pcm"

        await asyncio.gather(
            collect(ctx1, filename1),
            collect(ctx2, filename2),
        )

        print(f"Saved context 1 audio to {filename1}")
        print(f"Saved context 2 audio to {filename2}")
        print(f"Play with:")
        print(f"  ffplay -f f32le -ar 44100 {filename1}")
        print(f"  ffplay -f f32le -ar 44100 {filename2}")


async def tts_async_concurrent_contexts(client: AsyncCartesia) -> None:
    """
    Demonstrates using a single WebSocket connection to manage multiple contexts concurrently.

    We spawn separate tasks to push audio to 3 different contexts.
    We use a single receiver loop to de-multiplex the responses to the correct files.
    """
    from cartesia.types import GenerationRequestParam

    async with client.tts.generate_ws() as ws:
        all_quotes = [
            ["Ask not what your country can do for you, ", "ask what you can do ", "for your country."],
            ["I have a dream ", "that one day this nation ", "will rise up."],
            ["In the end, it's not the years in your life that count. ", "It's the life ", "in your years."],
        ]

        # Define a sender function
        async def send_transcript(ctx_index: int) -> None:
            transcripts = all_quotes[ctx_index]
            for part_idx, part in enumerate(transcripts):
                print(f"Sending '{part.strip()}' to context {ctx_index}")
                request: GenerationRequestParam = {
                    "model_id": "sonic-3",
                    "voice": {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
                    "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
                    "context_id": str(ctx_index),
                    "transcript": part,
                    "language": "en",
                    "continue": part_idx + 1 < len(transcripts),
                }
                await ws.send(request)
                # Small delay to simulate real-time input and interleave requests
                await asyncio.sleep(0.1)

            print(f"Finished sending to context {ctx_index}")

        # Start sender tasks
        send_tasks = [asyncio.create_task(send_transcript(i)) for i in range(len(all_quotes))]

        # Receiver loop
        files: dict[int, IO[bytes]] = {}
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        print("Starting receiver loop...")

        done_count = 0

        # Iterate over the ws directly to receive all events
        async for event in ws:
            if event.type == "chunk" and event.audio:
                ctx_index = int(event.context_id)
                if ctx_index not in files:
                    filename = f"tts_concurrent_{ctx_index}_{timestamp}.pcm"
                    files[ctx_index] = open(filename, "wb")
                    print(f"Created file for context {ctx_index}: {filename}")

                files[ctx_index].write(event.audio)

            elif event.type == "done":
                ctx_id = event.context_id
                print(f"Context {ctx_id} finished.")

                done_count += 1

                if done_count == len(all_quotes):
                    print("All contexts finished.")
                    break

        # Clean up
        for f in files.values():
            f.close()

        # Ensure all send tasks are done (they should be by now if we got "done" events)
        await asyncio.gather(*send_tasks)

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for ctx_index, f in files.items():
            print(f"  Context {ctx_index}: ffplay -f f32le -ar 44100 {f.name}")


# =============================================================================
# Infill API (Async)
# =============================================================================


async def infill_create_async(client: AsyncCartesia) -> None:
    """Async infill creation."""
    from pathlib import Path

    response = await client.tts.infill(
        model_id="sonic-3",
        language="en",
        transcript="Infill text",
        left_audio=Path("left.wav"),
        right_audio=Path("right.wav"),
        voice_id="6ccbfb76-1fc6-48f7-b71d-91ac6298247b",
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    )
    await response.write_to_file("infill_output_async.wav")
    print("Saved audio to infill_output_async.wav")
    print("Play with: ffplay -f wav infill_output_async.wav")


if __name__ == "__main__":
    import os
    import sys
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

    extra_headers: dict[str, str] = {}
    cartesia_version = os.environ.get("CARTESIA_VERSION")
    if cartesia_version:
        extra_headers["Cartesia-Version"] = cartesia_version

    async def run() -> None:
        async with AsyncCartesia(api_key=api_key, default_headers=extra_headers) as client:
            await func(client)

    try:
        asyncio.run(run())
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
