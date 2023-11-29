import os
from pydub import AudioSegment

class AudioModel:
    def __init__(self):
        self.audio_data = None
        self.wav_path = None

    def load_audio_file(self, file_path):
        output_filepath = os.path.splitext(file_path)[0] + '.wav'
        _, extension = os.path.splitext(file_path)
        file_type = extension.lower()

        self.audio_data = AudioSegment.from_wav(file_path)
        self.wav_path = file_path

    def strip_metadata(self):
        if self.audio_data:
            if self.audio_data.channels > 1:
                self.audio_data = self.audio_data.set_channels(1)

            if self.audio_data.sample_width > 2:
                self.audio_data = self.audio_data.set_sample_width(2)

    def get_wave_duration(self):
        return self.audio_data.duration_seconds
