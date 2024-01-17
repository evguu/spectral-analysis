from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
from math import log10, floor


class TimeDomainRepresentation:
    def __init__(self, samples=None, sample_rate=None):
        self.samples = samples
        self.sample_rate = sample_rate

    def to_frequency_domain(self, reference_freq=440):
        n = len(self.samples)
        yf = rfft(self.samples)
        xf = rfftfreq(n, 1 / self.sample_rate)
        return FrequencyDomainRepresentation(yf, self.sample_rate, n, reference_freq)

    def save_to_wav(self, output_file):
        write(output_file, self.sample_rate, self.samples)
        return self

    def load_from_mp3(self, input_file):
        sound = AudioSegment.from_file(input_file, format="mp3")
        self.samples = np.array(sound.get_array_of_samples())
        self.sample_rate = sound.frame_rate
        return self

    def normalize(self):
        self.samples = np.int16(self.samples * (32767 / self.samples.max()))
        return self

    def graph(self, title):
        plt.figure(num=title)
        plt.plot(self.samples)
        plt.show()
        return self


class FrequencyDomainRepresentation:
    def __init__(self, fft_res, sample_rate, sample_count, reference_freq=440):
        self.fft_res = fft_res
        self.sample_rate = sample_rate
        self.sample_count = sample_count
        self.reference_freq = reference_freq

    def to_time_domain(self):
        n = len(self.fft_res)
        return TimeDomainRepresentation(irfft(self.fft_res), self.sample_rate)

    def graph(self, title):
        xf = rfftfreq(self.sample_count, 1 / self.sample_rate)
        plt.figure(num=title)
        plt.plot(xf, np.abs(self.fft_res))
        plt.show()
        return self

    def boost_note(self, semitones, boost_level):
        target_frequencies = []
        max_freq = self.sample_rate / 2
        order = -3  # To reach low frequency notes too.
        while True:
            freq = self.reference_freq * 2 ** (semitones / 12 + order)
            if freq >= max_freq:
                break
            target_frequencies.append(freq)
            order += 1

        fft_bars_per_freq = len(self.fft_res) / max_freq
        for freq in target_frequencies:
            low_note_border = int(freq * fft_bars_per_freq * (2 ** -1 + 2 ** (-1 - 1/12)))
            high_note_border = int(freq * fft_bars_per_freq * (2 ** -1 + 2 ** (-1 + 1/12)))
            half_fft_resolution = int(fft_bars_per_freq / 2)

            low_idx = max(0, low_note_border - half_fft_resolution)
            high_idx = min(len(self.fft_res), high_note_border + half_fft_resolution)

            self.fft_res[low_idx:high_idx] = self.fft_res[low_idx:high_idx]*boost_level
        return self

    def calculate_note_powers(self, text):
        results = [0 for i in range(12)]
        for semitones in range(12):
            target_frequencies = []
            max_freq = self.sample_rate / 2
            order = -3  # To reach low frequency notes too.
            while True:
                freq = self.reference_freq * 2 ** (semitones / 12 + order)
                if freq >= max_freq:
                    break
                target_frequencies.append(freq)
                order += 1

            fft_bars_per_freq = len(self.fft_res) / max_freq
            for freq in target_frequencies:
                low_note_border = int(freq * fft_bars_per_freq * (2 ** -1 + 2 ** (-1 - 1 / 12)))
                high_note_border = int(freq * fft_bars_per_freq * (2 ** -1 + 2 ** (-1 + 1 / 12)))
                half_fft_resolution = int(fft_bars_per_freq / 2)

                low_idx = max(0, low_note_border - half_fft_resolution)
                high_idx = min(len(self.fft_res), high_note_border + half_fft_resolution)

                results[semitones] += np.sum(np.abs(self.fft_res[low_idx:high_idx]))
        print(text, [floor(log10(i + 1)*1000)/100 for i in results])
        return self

