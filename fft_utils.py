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


def fletcher_munson_coefficient(frequencies):
    # Convert frequencies to log scale
    f = np.log10(frequencies)

    # Initialize output array
    coefficients = np.zeros_like(f)

    # Calculate Fletcher-Munson coefficient for each frequency
    mask1 = (f >= -0.594) & (f <= 0.466)
    mask2 = (f > 0.466) & (f <= 1.160)
    mask3 = f > 1.160

    coefficients[mask1] = 10 * (f[mask1] + 0.594)
    coefficients[mask2] = 10 * (f[mask2] - 0.466) ** 2 / (1 + 0.04 * (f[mask2] - 0.466))
    coefficients[mask3] = 10 * ((f[mask3] - 1.160) ** 2 / (1 + 0.04 * (f[mask3] - 1.160))) ** 0.5

    return coefficients


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
        order = -4  # To reach low frequency notes too.
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

            self.fft_res[low_idx:high_idx] = self.fft_res[low_idx:high_idx]*(10 ** (boost_level / 10))
        return self

    def multiband_boost(self, boost_array):
        for i in range(len(boost_array)):
            self.boost_note(i, boost_array[i])
        return self

    def calculate_note_powers(self, text):
        results = [0 for i in range(12)]
        for semitones in range(12):
            target_frequencies = []
            max_freq = self.sample_rate / 2
            order = -4  # To reach low frequency notes too.
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

                cut = np.abs(self.fft_res[low_idx:high_idx])
                inner_freqs = np.linspace(low_idx, high_idx, high_idx - low_idx) / fft_bars_per_freq
                results[semitones] += np.sum(cut * fletcher_munson_coefficient(inner_freqs))
        print(text, [floor(log10(i + 1)*1000)/100 for i in results])
        return self
