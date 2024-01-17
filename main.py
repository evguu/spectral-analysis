from fft_utils import TimeDomainRepresentation


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/audio.mp3")

    sound.to_frequency_domain()\
        .calculate_note_powers('Clean:') \
        .boost_note(semitones=0, boost_level=5) \
        .boost_note(semitones=1, boost_level=0) \
        .boost_note(semitones=2, boost_level=0) \
        .boost_note(semitones=3, boost_level=0) \
        .boost_note(semitones=4, boost_level=5) \
        .boost_note(semitones=5, boost_level=0) \
        .boost_note(semitones=6, boost_level=0) \
        .boost_note(semitones=7, boost_level=5) \
        .boost_note(semitones=8, boost_level=0) \
        .boost_note(semitones=9, boost_level=0) \
        .boost_note(semitones=10, boost_level=0) \
        .boost_note(semitones=11, boost_level=0) \
        .calculate_note_powers('Boost:') \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-0.wav")

    sound.normalize()\
        .save_to_wav("output/src.wav")


if __name__ == "__main__":
    main()
