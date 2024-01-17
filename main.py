from fft_utils import TimeDomainRepresentation


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/audio.mp3") \
        .to_frequency_domain()\
        .graph(title='Source Signal Frequency Domain')\
        .boost_note(reference_freq=440, semitones=2, boost_level=2) \
        .graph(title='D-Boosted Signal Frequency Domain') \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean.wav")


def filter_fft(fft_res, sample_rate, modification_dict):
    points_per_freq = len(fft_res) / (sample_rate / 2)
    for freq, amp in modification_dict.items():
        target_idx = int(points_per_freq * freq)
        fft_res[target_idx - 1: target_idx + 2] = amp
    return fft_res


if __name__ == "__main__":
    main()
