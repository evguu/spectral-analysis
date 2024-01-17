import numpy as np
import matplotlib.pyplot as plt

from fft_utils import TimeDomainRepresentation


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/audio.mp3")\
        .to_frequency_domain()\
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean.wav")


def filter_fft(fft_res, sample_rate, modification_dict):
    points_per_freq = len(fft_res) / (sample_rate / 2)
    for freq, amp in modification_dict.items():
        target_idx = int(points_per_freq * freq)
        fft_res[target_idx - 1: target_idx + 2] = amp
    return fft_res


def graph_wav_freq(np_arr, sample_rate, enable_graph=False):
    N = len(np_arr)
    yf = rfft(np_arr)
    xf = rfftfreq(N, 1 / sample_rate)

    if enable_graph:
        plt.plot(xf, np.abs(yf))
        plt.show()

    return yf


if __name__ == "__main__":
    main()
