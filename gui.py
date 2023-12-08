import tkinter as tk
from tkinter import filedialog


class AudioView:
    def __init__(self, root, controller):
        self.controller = controller

        self.window = root
        self.window.title("Acoustic Modeler")

        self.label = tk.Label(self.window, text="Welcome to the Acoustic Modeler!")
        self.label.pack(pady=5)

        self.load_button = tk.Button(self.window, text="Load Audio File", command=self.load_audio_file)
        self.load_button.pack(pady=0)

        self.duration_label = tk.Label(self.window, text="")
        self.duration_label.pack(pady=0)

        self.frequency_label = tk.Label(self.window, text="")
        self.frequency_label.pack(pady=0)

        self.file_name_label = tk.Label(self.window, text="")
        self.file_name_label.pack(pady=1)

        self.low_label = tk.Label(self.window, text="")
        self.low_label.pack(pady=1)

        self.med_label = tk.Label(self.window, text="")
        self.med_label.pack(pady=1)

        self.high_label = tk.Label(self.window, text="")
        self.high_label.pack(pady=1)

    def load_audio_file(self):
        file_path = filedialog.askopenfilename(title="Select Audio File")
        self.controller.load_audio_file(file_path)

        file_name = file_path.split("//")[-1]
        self.file_name_label.config(text=f"File: {file_name}")

        self.controller.strip_metadata()
        formatted_duration = "{:.2f}".format(self.controller.get_wave_duration())
        self.duration_label.config(text=f"Duration: {formatted_duration} seconds")
        self.controller.show_wav()
        formatted_frequency = "{:.2f}".format(self.controller.get_freq())
        self.frequency_label.config(text=f"Sample Rate: {formatted_frequency} Hz")

        target_frequency, rt60 = self.controller.plot_rt60(500)
        self.low_label.config(text=f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')
        target_frequency, rt60 = self.controller.plot_rt60(1000)
        self.med_label.config(text=f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')
        target_frequency, rt60 = self.controller.plot_rt60(5000)
        self.high_label.config(text=f'The RT60 reverb time at freq {int(target_frequency)}Hz is {round(abs(rt60), 2)} seconds')

