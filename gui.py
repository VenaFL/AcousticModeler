import tkinter as tk
from tkinter import filedialog

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


