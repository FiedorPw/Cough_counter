import os
import wave
import time
import threading
import tkinter as tk
from tkinter import ttk
import pyaudio
import shutil
import re


import count_coughs
import record

class VoiceRecorder:
    def __init__(self):

        self.coughs = {}
        home_directory = os.environ.get('HOME')
        #trzeba stworzyć folder kaszlometr na pulpicie
        self.working_dir = f'{home_directory}/Desktop/kaszlometr'

        self.initialize_gui()

        self.recording = False

        self.root.mainloop()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.iconphoto(False, tk.PhotoImage(file='./Icons/kaszlometr-icon.png'))
        self.root.title("Kaszlometr")

        self.setup_treeview()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.LEFT)

        self.button = tk.Button(self.button_frame, text="🎤", font=("Arial", 140, "bold"), command=self.click_handler)
        self.button.pack(side=tk.TOP)

        # self.label = tk.Label(self.button_frame, text="00:placek00:00")
        # self.label.pack(side=tk.BOTTOM)

        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.record_time_label = tk.Label(self.info_frame, font=("Arial", 15), text="Czas nagrywania:")
        self.record_time_label.pack(side=tk.TOP)

        self.label = tk.Label(self.info_frame, font=("Arial", 30, "bold"), text="00:00:00")
        self.label.pack(side=tk.TOP)

        self.patient_name_label = tk.Label(self.info_frame, font=("Arial", 20,), text="Imię pacjenta:")
        self.patient_name_label.pack(side=tk.TOP)

        self.patient_name_entry = tk.Entry(self.info_frame)
        self.patient_name_entry.pack(side=tk.TOP)
    def click_handler(self):
        if self.recording:
            self.recording = False
            self.button.config(fg="black")
        else:
            self.button.config(fg="red")
            self.recording = True
            #czyszczenie listy graficznej
            self.coughs = {}
            for item in self.tree.get_children():
                self.tree.delete(item)
            #odpalenie słuchania asynchronicznie
            threading.Thread(target=self.record).start()

    def setup_treeview(self):
        self.columns = ('kaszel', 'prawdopodobienstwo')
        # Create a frame for the treeview
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create the Treeview widget
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show='headings')

        # Define headings
        self.tree.heading('kaszel', text='Wykryty kaszel')
        self.tree.heading('prawdopodobienstwo', text='Prawdopodobieństwo')

        # Define column width and alignment
        self.tree.column('kaszel', width=150, anchor='center')
        self.tree.column('prawdopodobienstwo', width=100, anchor='center')

        # Create a scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack the scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Pack the treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add some sample data
        # coughs = {
        #     './chunk-01.wav': 0.8895571,
        #     './chunk-02.wav': 0.6795571,
        #     # Add more coughs as needed...
        # }
        #
        # # Insert data into the treeview
        # for filename, score in coughs.items():
        #     self.tree.insert('', tk.END, values=(filename, score))

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

        self.analyze_chunks()

    def move_files_to_directory(self,file_list, destination_directory):
        #pobiera z gui
        subdir_name = self.patient_name_entry.get()

        #jeżeli puste pole tworzy nowy folder kaszle (ostatni numer folderu +1)
        if subdir_name == "":
            highest_number_dir = self.get_highest_numbered_folder(self.working_dir)
            subdir_name = highest_number_dir + 1

        subdir_name = f"{destination_directory}/{subdir_name}"

        # Create the destination directory if it doesn't exist
        if not os.path.exists(subdir_name):
            os.makedirs(subdir_name)

        # Move each file from the list to the destination directory
        for file_path in file_list:
            # Get the file name from the file path
            file_name = os.path.basename(file_path)
            # Construct the new file path in the destination directory
            new_file_path = os.path.join(subdir_name, file_name)
            # Move the file to the destination directory
            shutil.move(file_path, new_file_path)
            print(f"Moved {file_path} to {new_file_path}")

    # Example usage
    # file_list = ['/path/to/file1.txt', '/path/to/file2.txt', '/path/to/file3.txt']
    # destination_directory = '/path/to/destination'
    # move_files_to_directory(file_list, destination_directory)

    def get_highest_numbered_folder(self,directory):
        # Get a list of all folders in the directory
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        # If there are no folders, return 1
        if not folders:
            return 1

        # Extract numbers from folder names and find the highest number
        max_number = 0
        for folder in folders:
            match = re.search(r'\d+', folder)
            if match:
                number = int(match.group())
                if number > max_number:
                    max_number = number

        # Return the highest number found + 1
        return max_number + 1



    def analyze_chunks(self):
        # CAŁA OBRÓBKA KASZLI DZIELENIE I SPRAWDZANIE

        # /print(count_coughs.count_coughs('output.wav',2))
        self.coughs = count_coughs.count_coughs('output.wav', 2)

        #wrzucanie do tabeli w gui
        for filename, score in self.coughs.items():
            self.tree.insert('', tk.END, values=(filename, score))

        cough_file_list = list(self.coughs.keys())

        self.move_files_to_directory(cough_file_list,self.working_dir)


VoiceRecorder()