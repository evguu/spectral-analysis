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
    new_sig = irfft(fft_res)
    norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
    write("output/clean.wav", sound.frame_rate, norm_new_sig)



def graph_wav_freq(np_arr, sample_rate):
    N = len(np_arr)
    yf = rfft(np_arr)
    xf = rfftfreq(N, 1 / sample_rate)

    # plt.plot(xf, np.abs(yf))
    # plt.show()

    return yf

if __name__ == "__main__":
    main()
