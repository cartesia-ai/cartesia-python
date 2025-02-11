import uuid
import wave

from cartesia import Cartesia

MODEL_ID = "sonic"
DEFAULT_OUTPUT_FORMAT = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}
VOICE_ID = "f9836c6e-a0bd-460e-9d3c-f7299fa60f94"

filename = "tmp/test.wav"
wave_file = wave.open(filename, "wb")
wave_file.setnchannels(1)  # mono
wave_file.setsampwidth(2)  # size of each sample
wave_file.setframerate(44100)  # sampling rate

client = Cartesia(api_key="sk_car_TXJM5QRAWe70iwKC8_r7L")
ws = client.tts.websocket()  # type: ignore
context_id = str(uuid.uuid4())
output = ws.send(
    transcript="Hello, this is Cartesia",
    voice={"id": VOICE_ID},
    output_format=DEFAULT_OUTPUT_FORMAT,
    stream=False,
    model_id=MODEL_ID,
    language="en",
)
if output.audio is not None:
    print("Writing audio to file")
    wave_file.writeframes(output.audio)
wave_file.close()
ws.close()
