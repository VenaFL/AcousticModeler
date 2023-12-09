# Communicates information between the gui and model modules
class AudioController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def load_audio_file(self, file_path):
        self.model.load_audio_file(file_path)

    def strip_metadata(self):
        self.model.strip_metadata()

    def get_wave_duration(self):
        return self.model.get_wave_duration()

    def show_wav(self):
        return self.model.show_wav()

    def get_freq(self):
        return self.model.get_freq()

    def plot_rt60(self, target):
        return self.model.show_freq(target=target)

    def combine_plots(self, targets):
        self.model.combine_plots(targets)

    def display_spectrogram(self):
        self.model.display_spectrogram()

