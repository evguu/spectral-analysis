from fft_utils import TimeDomainRepresentation


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/audio.mp3")

    sound.to_frequency_domain()\
        .calculate_note_powers('Clean:') \
        .multiband_boost([5, 0, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0]) \
        .calculate_note_powers('Boost:') \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-0.wav")

    sound.normalize()\
        .save_to_wav("output/src.wav")


if __name__ == "__main__":
    main()
