import pyaudio
import wave
import os

def record():
    # Parameters
    FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
    CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
    RATE = 48000              # Sample rate (samples per second)
    CHUNK = 2048              # Number of frames per buffer
    RECORD_SECONDS = 15        # Duration of recording
    WAVE_OUTPUT_FILENAME = "output.wav"  # Output file

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Record data
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PyAudio object
    audio.terminate()

    # Save recorded data as a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

#odpalenie reszty
#os.system('python count_coughs.py 2 output.wav')
