import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
import record

class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(True,True)
        self.button = tk.Button(text="🎤", font=("Arial", 120, "bold"), command=self.click_handler)
        self.button.pack()

        self.label = tk.Label(text="00:00:00")
        self.label.pack()

        self.recording = False


        self.root.mainloop()

    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.recording = True
            self.button.config(fg="red")
            threading.Thread(target=self.record).start()

    def record(self):

        FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
        CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
        RATE = 48000  # Sample rate (samples per second)
        CHUNK = 2048  # Number of frames per buffer
        RECORD_SECONDS = 15  # Duration of recording
        WAVE_OUTPUT_FILENAME = "output.wav"  # Output file

        # Initialize PyAudio
        audio = pyaudio.PyAudio()

        # Open stream
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, input=True,
                            frames_per_buffer=CHUNK)

        print("Recording...")

        frames = []

        start = time.time()

        while self.recording:

            data = stream.read(CHUNK)
            frames.append(data)

            passed = time.time() - start
            seconds = passed % 60
            minutes = passed // 60
            hours = minutes // 60
            self.label.config(text=f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

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



VoiceRecorder()