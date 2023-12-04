import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import wave
plt.figure(figsize=(14, 10))

class AudioView:
    def __init__(self, root, controller):
        self.controller = controller

        self.window = root
        self.window.title("Acoustic Modeler")

        self.label = tk.Label(self.window, text="Welcome to the Acoustic Modeler!")
        self.label.pack(pady=10)

        self.load_button = tk.Button(self.window, text="Load Audio File", command=self.load_audio_file)
        self.load_button.pack(pady=10)

        self.duration_label = tk.Label(self.window, text="")
        self.duration_label.pack(pady=10)

    def load_audio_file(self):
        file_path = filedialog.askopenfilename(title="Select Audio File")
        self.controller.load_audio_file(file_path)
        self.controller.strip_metadata()
        duration_seconds = self.controller.get_wave_duration()
        formatted_duration = "{:.2f}".format(duration_seconds)
        self.duration_label.config(text=f"Duration: {formatted_duration} seconds")

    def show_graph(self, time):
        wav_obj = wave.open(file_path, 'rb')

        sample_freq = wav_obj.getframerate()
        n_samples = wav_obj.getnframes()
        t_audio = n_samples / sample_freq
        signal_wave = wav_obj.readframes(n_samples)
        signal_array = np.frombuffer(signal_wave, dtype=np.int16)
        times = np.linspace(0, n_samples / sample_freq, num=n_samples)
        plt.figure(figsize=(15, 5))
        plt.plot(times, l_channel)
        plt.title('Left Channel')
        plt.ylabel('Signal Value')
        plt.xlabel('Time (s)')
        plt.xlim(0, t_audio)
        plt.show()

