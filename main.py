from fft_utils import TimeDomainRepresentation


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/audio.mp3")

    sound.to_frequency_domain()\
        .boost_note(semitones=0, boost_level=1) \
        .boost_note(semitones=4, boost_level=0) \
        .boost_note(semitones=7, boost_level=0) \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-0.wav")

    sound.to_frequency_domain()\
        .boost_note(semitones=0, boost_level=0) \
        .boost_note(semitones=4, boost_level=1) \
        .boost_note(semitones=7, boost_level=0) \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-4.wav")

    sound.to_frequency_domain()\
        .boost_note(semitones=0, boost_level=0) \
        .boost_note(semitones=4, boost_level=0) \
        .boost_note(semitones=7, boost_level=1) \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-7.wav")

    sound.normalize()\
        .save_to_wav("output/src.wav")


if __name__ == "__main__":
    main()
