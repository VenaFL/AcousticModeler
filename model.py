import os
from pydub import AudioSegment

class AudioModel:
    def __init__(self):
        self.audio_data = None
        self.wav_path = None

    def load_audio_file(self, file_path):
        # Takes the audio's file path and separates the extension before attaching .wav onto it
        output_filepath = os.path.splitext(file_path)[0] + '.wav'
        # Assigns the audio file's extension to the variable "extension"
        _, extension = os.path.splitext(file_path)
        # Makes the extension lowercase
        file_type = extension.lower()

        if extension == '.mp3':
            # Takes the mp3 file sound
            audio_data = AudioSegment.from_mp3(file_path)
            # Exports it to output_filepath as a wav file
            audio_data.export(output_filepath, format='wav')

        self.audio_data = AudioSegment.from_wav(output_filepath)
        self.wav_path = output_filepath

    def strip_metadata(self):
        if self.audio_data:
            if self.audio_data.channels > 1:
                self.audio_data = self.audio_data.set_channels(1)

            if self.audio_data.sample_width > 2:
                self.audio_data = self.audio_data.set_sample_width(2)

    def get_wave_duration(self):
        return self.audio_data.duration_seconds
