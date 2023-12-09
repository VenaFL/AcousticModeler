from model import AudioModel
from gui import AudioView
from controller import AudioController
import tkinter as tk

audio_model = AudioModel()
audio_view = AudioView(tk.Tk(), AudioController(audio_model, None))

audio_view.controller.view = audio_view

# Entry point for the program
audio_view.window.mainloop()
