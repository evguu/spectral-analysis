# Given audio file path (mp3 or wav), load it and print the sample count.
from pydub import AudioSegment
from pydub.playback import play
from scipy.fft import rfft, rfftfreq, irfft
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


def open_audio_file(file_path):
    sound = AudioSegment.from_file(file_path, format="mp3")
    return sound


def main():
    sound = open_audio_file("input/audio.mp3")
    fft_res = graph_wav_freq(sound.get_array_of_samples(), sound.frame_rate)
    fft_flt = filter_fft(fft_res, sound.frame_rate, {4000: 1e9})
    new_sig = irfft(fft_flt)
    graph_wav_freq(new_sig, sound.frame_rate, True)

    norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
    write("output/clean.wav", sound.frame_rate, norm_new_sig)


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
