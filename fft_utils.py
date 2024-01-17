from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt


class TimeDomainRepresentation:
    def __init__(self, samples=None, sample_rate=None):
        self.samples = samples
        self.sample_rate = sample_rate

    def to_frequency_domain(self):
        n = len(self.samples)
        yf = rfft(self.samples)
        xf = rfftfreq(n, 1 / self.sample_rate)
        return FrequencyDomainRepresentation(yf, self.sample_rate, n)

    def save_to_wav(self, output_file):
        write(output_file, self.sample_rate, self.samples)
        return self

    def load_from_mp3(self, input_file):
        sound = AudioSegment.from_file(input_file, format="mp3")
        self.samples = sound.get_array_of_samples()
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
    def __init__(self, fft_res, sample_rate, sample_count):
        self.fft_res = fft_res
        self.sample_rate = sample_rate
        self.sample_count = sample_count

    def to_time_domain(self):
        n = len(self.fft_res)
        return TimeDomainRepresentation(irfft(self.fft_res), self.sample_rate)

    def graph(self, title):
        xf = rfftfreq(self.sample_count, 1 / self.sample_rate)
        plt.figure(num=title)
        plt.plot(xf, np.abs(self.fft_res))
        plt.show()
        return self

    def boost_note(self, reference_freq, semitones, boost_level):
        target_frequencies = []
        max_freq = self.sample_rate / 2
        order = -3  # To reach low frequency notes too.
        while True:
            freq = reference_freq * 2 ** (semitones / 12 + order)
            if freq >= max_freq:
                break
            target_frequencies.append(freq)
            order += 1

        fft_bars_per_freq = len(self.fft_res) / max_freq
        for freq in target_frequencies:
            target_idx = int(fft_bars_per_freq * freq)
            half_fft_resolution = int(fft_bars_per_freq / 2)
            low_idx = max(0, target_idx - half_fft_resolution)
            high_idx = min(len(self.fft_res), target_idx + half_fft_resolution)
            self.fft_res[low_idx:high_idx] = self.fft_res[low_idx:high_idx]*boost_level
        return self

