# Given audio file path (mp3 or wav), load it and print the sample count.
from pydub import AudioSegment
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt


def open_audio_file(file_path):
    sound = AudioSegment.from_file(file_path, format="mp3")
    return sound


def main():
    sound = open_audio_file("input/audio.mp3")
    graph_wav_freq(sound.get_array_of_samples(), sound.frame_rate)


def graph_wav_freq(np_arr, sample_rate):
    N = len(np_arr)
    yf = fft(np_arr)
    xf = fftfreq(N, 1 / sample_rate)

    plt.plot(xf, np.abs(yf))
    plt.show()


if __name__ == "__main__":
    main()
