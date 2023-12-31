import os
from pydub import AudioSegment
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import wave


# Holds the logic of the program
class AudioModel:
    def __init__(self):
        self.audio_data = None
        self.wav_path = None
        self.channels = 0

    # Loads file and converts to .wav if necessary
    def load_audio_file(self, file_path):
        _, extension = os.path.splitext(file_path)
        file_type = extension.lower()

        file_path = os.path.splitext(file_path)[0] + '.wav'

        if extension == '.mp3':
            mp3_data = AudioSegment.from_mp3(file_path)
            mp3_data.export(file_path, format='wav')

        self.audio_data = AudioSegment.from_wav(file_path)
        self.wav_path = file_path

    # Converts .wav file to mono if necessary
    def strip_metadata(self):
        with wave.open(self.wav_path, 'rb') as file:
            self.channels = file.getnchannels()
        if self.channels > 1:
            print(self.audio_data.channels)
            self.audio_data = self.audio_data.set_channels(1)
            self.audio_data.export(self.wav_path, format='wav')
            print(self.audio_data.channels)

    def get_wave_duration(self):
        return self.audio_data.duration_seconds

    # Plots the .wav file graph
    def show_wav(self):
        samplerate, data = wavfile.read(self.wav_path)
        length = data.shape[0] / samplerate
        time = np.linspace(0., length, data.shape[0])
        plt.plot(time, data, label="Mono channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    # Returns the resonance frequency
    def get_freq(self):
        sample_rate, data = wavfile.read(self.wav_path)
        result = np.fft.fft(data)
        frequencies = np.fft.fftfreq(len(data), d=1 / sample_rate)

        index = np.argmax(np.abs(result))
        peak_frequency = np.abs(frequencies[index])

        return peak_frequency

    # Plots RT60 for given target frequency (low, mid, or high)
    def show_freq(self, target):
        if self.channels == 1:
            sample_rate, data = wavfile.read(self.wav_path)
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            plt.close()

        def find_target_frequency(freqs, t):
            for x in freqs:
                if x > t:
                    break
            return x

        def frequency_check():
            global target_frequency
            target_frequency = find_target_frequency(freqs, target)
            index_of_frequency = np.where(freqs == target_frequency)[0][0]
            data_for_frequency = spectrum[index_of_frequency]
            data_for_frequency = np.maximum(data_for_frequency, 1e-10)
            data_in_db = 10 * np.log10(data_for_frequency)
            return data_in_db

        data_in_db = frequency_check()
        plt.figure(2)
        plt.title(self.get_title(target))
        plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color='#004bc6')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (dB)')
        index_of_max = np.argmax(data_in_db)
        value_of_max = data_in_db[index_of_max]
        plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
        sliced_array = data_in_db[index_of_max:]
        value_of_max_less_5 = value_of_max - 5

        def find_nearest_value(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]

        value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
        index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
        plt.plot(t[index_of_max_less_5], data_in_db[index_of_max], 'yo')

        value_of_max_less_25 = value_of_max - 25
        value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
        index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
        plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

        rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
        rt60 = 3 * rt20
        plt.grid()
        plt.show()
        return target_frequency, rt60

    # Creates labeled plot of all three frequency regions
    def combine_plots(self, targets):

        if self.channels == 1:
            sample_rate, data = wavfile.read(self.wav_path)
            spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
            plt.close()
        plt.figure(2)
        colors = ['blue', 'green', 'red']

        for i, color in enumerate(colors):
            def find_target_frequency(freqs, t):
                for x in freqs:
                    if x > t:
                        break
                return x

            def frequency_check():
                global target_frequency
                target_frequency = find_target_frequency(freqs, targets[i])
                index_of_frequency = np.where(freqs == target_frequency)[0][0]
                data_for_frequency = spectrum[index_of_frequency]
                data_for_frequency = np.maximum(data_for_frequency, 1e-10)
                data_in_db = 10 * np.log10(data_for_frequency)
                return data_in_db

            data_in_db = frequency_check()
            plt.plot(t, data_in_db, linewidth=1, alpha=0.7, color=color, label=f'{targets[i]} Hz')
            plt.xlabel('Time (s)')
            plt.ylabel('Power (dB)')
            index_of_max = np.argmax(data_in_db)
            value_of_max = data_in_db[index_of_max]
            plt.plot(t[index_of_max], data_in_db[index_of_max], 'go')
            sliced_array = data_in_db[index_of_max:]
            value_of_max_less_5 = value_of_max - 5

            def find_nearest_value(array, value):
                array = np.asarray(array)
                idx = (np.abs(array - value)).argmin()
                return array[idx]

            value_of_max_less_5 = find_nearest_value(sliced_array, value_of_max_less_5)
            index_of_max_less_5 = np.where(data_in_db == value_of_max_less_5)
            plt.plot(t[index_of_max_less_5], data_in_db[index_of_max], 'yo')

            value_of_max_less_25 = value_of_max - 25
            value_of_max_less_25 = find_nearest_value(sliced_array, value_of_max_less_25)
            index_of_max_less_25 = np.where(data_in_db == value_of_max_less_25)
            plt.plot(t[index_of_max_less_25], data_in_db[index_of_max_less_25], 'ro')

            rt20 = (t[index_of_max_less_5] - t[index_of_max_less_25])[0]
            rt60 = 3 * rt20
            plt.grid()
        plt.title("Combined Low, Mid, High Plots")
        plt.legend()
        plt.show()

    # Creates and displays a spectrogram of the .wav file
    def display_spectrogram(self):
        sample_rate, data = wavfile.read(self.wav_path)
        spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
        cbar = plt.colorbar(im)
        plt.xlabel('Time (s)')
        plt.ylabel('Frequency (Hz)')
        cbar.set_label('Intensity (dB)')
        plt.show()
        plt.figure(2)

    # Gets plot title corresponding to frequency
    def get_title(self, target):
        if target < 750:
            return "Low Plot"
        elif target < 2000:
            return "Mid Plot"
        else:
            return "High Plot"
