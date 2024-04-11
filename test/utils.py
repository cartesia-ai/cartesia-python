# Utility functions used for testing

import wave

import numpy as np


# Primarily used for testing
def pcm_to_wav(
    pcm_data, output_file, sample_rate=44100, sample_width=2, num_channels=1, is_bytes=False
):
    if is_bytes:
        # Convert bytes to int16
        pcm_data = np.frombuffer(pcm_data, dtype=np.int16)
    else:
        # Convert float32 PCM data to int16
        pcm_data = (pcm_data * 32767).astype(np.int16)

    # Open a new WAV file for writing
    wav_file = wave.open(output_file, "wb")

    # Set the WAV file parameters
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)  # 2 bytes for int16
    wav_file.setframerate(sample_rate)

    # Write the PCM data to the WAV file
    wav_file.writeframes(pcm_data.tobytes())

    # Close the WAV file
    wav_file.close()
