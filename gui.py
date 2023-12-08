import tkinter as tk
from tkinter import filedialog


class AudioView:
    def __init__(self, root, controller):
        self.controller = controller

        # Title
        self.window = root
        self.window.title("Acoustic Modeler")

        # Greeting text
        self.label = tk.Label(self.window, text="Welcome to the Acoustic Modeler!")
        self.label.pack(pady=5)

        # Button to select an audio file
        self.load_button = tk.Button(self.window, text="Load Audio File", command=self.load_audio_file)
        self.load_button.pack(pady=0)

        self.duration_label = tk.Label(self.window, text="")
        self.duration_label.pack(pady=0)

        self.frequency_label = tk.Label(self.window, text="")
        self.frequency_label.pack(pady=0)

    def load_audio_file(self):
        file_path = filedialog.askopenfilename(title="Select Audio File")
        self.controller.load_audio_file(file_path)
        self.controller.strip_metadata()
        formatted_duration = "{:.2f}".format(self.controller.get_wave_duration())
        self.duration_label.config(text=f"Duration: {formatted_duration} seconds")
        self.controller.show_wav()
        formatted_frequency = "{:.2f}".format(self.controller.get_freq())
        self.frequency_label.config(text=f"Sample Rate: {formatted_frequency} Hz")
        self.controller.show_freq()
