# import asyncio

import numpy as np
from utils import pcm_to_wav

from cartesia.tts import AsyncCartesiaTTS, CartesiaTTS


async def test_async_websockets():
    """
    Test the websockets for the Async Client by instantiating a client
    and sending two long messages through the `generate` function in succession.
    """
    async with AsyncCartesiaTTS(
        api_key="API_KEY_HERE", experimental_ws_handle_interrupts=False
    ) as client:
        voices = client.get_voices()
        voice = client.get_voice_embedding(voice_id=voices["Graham"]["id"])

        """asyncio.create_task(
            client.generate(
                transcript="I am a computer program that can generate speech from text and I am very good at it. I can generate speech in many different languages and accents. I can also generate speech in different voices and styles. I can generate speech that sounds like a human or a robot. I can generate speech that sounds happy or sad. I can generate speech that sounds excited or bored. I can generate speech that sounds like a child or an adult. I can generate speech",
                voice=voice,
            ),
        )"""

        """transcript1 = "I am a computer program that can generate speech from text and I am very good at it. I can generate speech in many different languages and accents. I can also generate speech in different voices and styles. I can generate speech that sounds like a human or a robot. I can generate speech that sounds happy or sad. I can generate speech that sounds excited or bored."
        transcript2 = "Hello, how are you doing today? I am doing well, thank you for asking. I have had a very good day. I enjoy talking to you."
        transcript3 = "I'm going to add a few more of these transcripts to see if there's any issues with running sequential TTS tasks."
        transcript4 = "We'll see if there are any residual issues from not flushing the websocket, though candidly I'm not too sure what flushing refers to in this context."

        transcripts = [transcript1, transcript2, transcript3, transcript4]
        test_generations = []
        for index, transcript in enumerate(transcripts):
            print(f"Generating audio for transcript {index + 1}...")
            test_generations.append(
                await client.generate(
                    transcript=transcript,
                    voice=voice,
                )
            )"""

        test_generations = []
        transcript = "Hi"
        long_transcript = "I am a computer program that can generate speech from text and I am very good at it. I can generate speech in many different languages and accents. I can also generate speech in different voices and styles. I can generate speech that sounds like a human or a robot. I can generate speech that sounds happy or sad. I can generate speech that sounds excited or bored."
        for index in range(10):
            print(f"Generating audio for transcript... {index * 5 + 1} to {index * 5 + 5}")
            for _ in range(4):
                test_generations.append(
                    await client.generate(
                        transcript=transcript,
                        voice=voice,
                    )
                )
            test_generations.append(
                await client.generate(
                    transcript=long_transcript,
                    voice=voice,
                )
            )

        for index, test_generation in enumerate(test_generations):
            print(f"Saving audio for transcript {index + 1}...")
            pcm_to_wav(
                pcm_data=np.frombuffer(test_generation["audio"], dtype=np.float32),
                output_file=f"test_websocket_rapid_{index + 1}.wav",
                # is_bytes=True
            )


def test_sync_websockets():
    """
    Test the websockets for the Sync Client by instantiating a client
    and sending two long messages through the `generate` function in succession.
    """
    client = CartesiaTTS(api_key="API_KEY_HERE")
    voices = client.get_voices()
    voice = client.get_voice_embedding(voice_id=voices["Graham"]["id"])

    """transcript1 = "I am a computer program that can generate speech from text and I am very good at it. I can generate speech in many different languages and accents. I can also generate speech in different voices and styles. I can generate speech that sounds like a human or a robot. I can generate speech that sounds happy or sad. I can generate speech that sounds excited or bored."
    transcript2 = "Hello, how are you doing today? I am doing well, thank you for asking. I have had a very good day. I enjoy talking to you."
    transcript3 = "I'm going to add a few more of these transcripts to see if there's any issues with running sequential TTS tasks."
    transcript4 = "We'll see if there are any residual issues from not flushing the websocket, though candidly I'm not too sure what flushing refers to in this context."

    transcripts = [transcript1, transcript2, transcript3, transcript4]
    test_generations = []
    for index, transcript in enumerate(transcripts):
        print(f"Generating audio for transcript {index + 1}...")
        test_generations.append(
            client.generate(
                transcript=transcript,
                voice=voice,
            )
        )"""

    test_generations = []
    transcript = "Hi"
    long_transcript = "I am a computer program that can generate speech from text and I am very good at it. I can generate speech in many different languages and accents. I can also generate speech in different voices and styles. I can generate speech that sounds like a human or a robot. I can generate speech that sounds happy or sad. I can generate speech that sounds excited or bored."
    for index in range(10):
        print(f"Generating audio for transcript... {index * 5 + 1} to {index * 5 + 5}")
        for _ in range(4):
            test_generations.append(
                client.generate(
                    transcript=transcript,
                    voice=voice,
                )
            )
        test_generations.append(
            client.generate(
                transcript=long_transcript,
                voice=voice,
            )
        )

    for index, test_generation in enumerate(test_generations):
        print(f"Saving audio for transcript {index + 1}...")
        pcm_to_wav(
            pcm_data=np.frombuffer(test_generation["audio"], dtype=np.float32),
            output_file=f"test_sync_rapid_websocket_{index + 1}.wav",
            # is_bytes=True
        )


if __name__ == "__main__":
    # asyncio.run(test_async_websockets())
    test_sync_websockets()
