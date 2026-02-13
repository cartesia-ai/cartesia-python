"""
Async Examples for Cartesia Python SDK v3.x
"""

import asyncio
import datetime

from cartesia import (
    AsyncCartesia,
)

# =============================================================================
# TTS Bytes (Async)
# =============================================================================

async def tts_generate_async(client: AsyncCartesia):
    """Async TTS generation to file."""
    response = await client.tts.generate(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
    )
    await response.write_to_file("output_async.wav")
    print("Saved audio to output_async.wav")
    print("Play with: ffplay -f wav output_async.wav")

async def tts_bytes_async(client: AsyncCartesia):
    """Async bytes iterator."""
    response = await client.tts.bytes(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "wav", "encoding": "pcm_f32le", "sample_rate": 44100},
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

async def tts_sse_basic_async(client: AsyncCartesia):
    """Async SSE streaming."""
    stream = await client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
                raise Exception(f"Error: {event.error}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

async def tts_sse_with_timestamps_async(client: AsyncCartesia):
    """Async SSE streaming with timestamps."""
    stream = await client.tts.generate_sse(
        model_id="sonic-3",
        transcript="Hello, world!",
        voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
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
                raise Exception(f"Error: {event.error}")

    print(f"Saved audio to {filename}")
    print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

# =============================================================================
# TTS WebSocket (Async)
# =============================================================================

async def tts_websocket_basic_async(client: AsyncCartesia):
    """Async WebSocket usage with websocket_connect()."""
    async with client.tts.websocket_connect() as connection:
        await connection.send({
            "model_id": "sonic-3",
            "transcript": "Hello, world!",
            "voice": {"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            "output_format": {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
        })

        filename = f"tts_ws_basic_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in connection:
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)
                elif response.done:
                    break
        
        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

async def tts_websocket_continuations_async(client: AsyncCartesia):
    """Async streaming multiple transcripts with continuations."""
    transcripts = ["The only thing we have to fear ", "is ", "fear itself."]
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context()

        for transcript in transcripts:
            await ctx.send(
                model_id="sonic-3",
                transcript=transcript,
                voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
                output_format=output_format,
                continue_=True,
            )

        await ctx.no_more_inputs()

        filename = f"tts_ws_continuations_async_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pcm"

        with open(filename, "wb") as f:
            async for response in ctx.receive():
                if response.type == "chunk" and response.audio:
                    f.write(response.audio)

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

async def tts_websocket_flushing_async(client: AsyncCartesia):
    """Async manual flushing example."""
    transcripts = ["First transcript.", "Second transcript."]
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context()

        # 1. Send first transcript
        print("Sending first transcript...")
        await ctx.send(
            model_id="sonic-3",
            transcript=transcripts[0],
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            continue_=True,
        )

        # 2. Flush!
        print("Flushing...")
        await ctx.send(
            model_id="sonic-3",
            transcript="",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            continue_=True,
            flush=True,
        )

        # 3. Send second transcript
        print("Sending second transcript...")
        await ctx.send(
            model_id="sonic-3",
            transcript=transcripts[1],
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format,
            continue_=True,
        )

        await ctx.no_more_inputs()

        import datetime
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        files = {}

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

async def tts_websocket_emotion_async(client: AsyncCartesia):
    """Async emotion changing example."""
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format
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

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

async def tts_websocket_speed_async(client: AsyncCartesia):
    """Async speed changing example."""
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}

    async with client.tts.websocket_connect() as connection:
        ctx = connection.context(
            model_id="sonic-3",
            voice={"mode": "id", "id": "6ccbfb76-1fc6-48f7-b71d-91ac6298247b"},
            output_format=output_format
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

        print(f"Saved audio to {filename}")
        print(f"Play with: ffplay -f f32le -ar 44100 {filename}")

async def tts_async_concurrent_contexts(client: AsyncCartesia):
    """
    Demonstrates using a single WebSocket connection to manage multiple contexts concurrently.
    
    We spawn separate tasks to push audio to 3 different contexts.
    We use a single receiver loop to demultiplex the responses to the correct files.
    """
    output_format = {"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100}
    voice_id = "6ccbfb76-1fc6-48f7-b71d-91ac6298247b" # Standard voice
    
    async with client.tts.websocket_connect() as connection:
        # Create 3 contexts
        contexts = []
        for i in range(3):
            ctx = connection.context(
                model_id="sonic-3",
                voice={"mode": "id", "id": voice_id},
                output_format=output_format
            )
            contexts.append(ctx)
            print(f"Created context {i}: {ctx._context_id}")

        # Define a sender function
        async def send_transcript(ctx_index, ctx):
            all_quotes = [
                ["Ask not what your country can do for you, ", "ask what you can do ", "for your country."],
                ["I have a dream ", "that one day this nation ", "will rise up."],
                ["In the end, it's not the years in your life that count. ", "It's the life ", "in your years."]
            ]
            transcripts = all_quotes[ctx_index]
            for part in transcripts:
                print(f"Sending '{part.strip()}' to context {ctx_index}")
                # Use the new push() helper
                await ctx.push(part)
                # Small delay to simulate real-time input and interleave requests
                await asyncio.sleep(0.1)
            
            await ctx.no_more_inputs()
            print(f"Finished sending to context {ctx_index}")

        # Start sender tasks
        send_tasks = [
            asyncio.create_task(send_transcript(i, ctx)) 
            for i, ctx in enumerate(contexts)
        ]

        # Receiver loop
        files = {}
        active_contexts = {ctx._context_id for ctx in contexts}
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        print("Starting receiver loop...")
        
        # Iterate over the connection directly to receive all events
        async for event in connection:
            if event.type == "chunk" and event.audio:
                ctx_id = event.context_id
                if ctx_id not in files:
                    # Find which context index this matches for filename
                    ctx_idx = next((i for i, c in enumerate(contexts) if c._context_id == ctx_id), "unknown")
                    filename = f"tts_concurrent_{ctx_idx}_{timestamp}.pcm"
                    files[ctx_id] = open(filename, "wb")
                    print(f"Created file for context {ctx_idx}: {filename}")
                
                files[ctx_id].write(event.audio)
            
            elif event.type == "done":
                ctx_id = event.context_id
                print(f"Context {ctx_id} finished.")
                if ctx_id in active_contexts:
                    active_contexts.remove(ctx_id)
                
                if not active_contexts:
                    print("All contexts finished.")
                    break
        
        # Clean up
        for f in files.values():
            f.close()
            
        # Ensure all send tasks are done (they should be by now if we got "done" events)
        await asyncio.gather(*send_tasks)

        print("\nFinished.")
        print("You can play the generated audio files with these commands:")
        for ctx_id, f in files.items():
            ctx_idx = next((i for i, c in enumerate(contexts) if c._context_id == ctx_id), "unknown")
            print(f"  Context {ctx_idx}: ffplay -f f32le -ar 44100 {f.name}")

# =============================================================================
# Infill API (Async)
# =============================================================================

async def infill_create_async(client: AsyncCartesia):
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
        available_functions = [name for name, obj in globals().items() 
                             if inspect.iscoroutinefunction(obj) and obj.__module__ == __name__]
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
        
    extra_headers = {}
    if os.environ.get("CARTESIA_VERSION"):
        extra_headers["Cartesia-Version"] = os.environ.get("CARTESIA_VERSION")

    async def run():
        async with AsyncCartesia(api_key=api_key, default_headers=extra_headers) as client:
            await func(client)

    try:
        asyncio.run(run())
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        sys.exit(1)
