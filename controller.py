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

