from fft_utils import TimeDomainRepresentation
from chord_helper import ChordHelper


def main():
    sound = TimeDomainRepresentation()\
        .load_from_mp3("input/rick.MP3")

    sound.to_frequency_domain()\
        .calculate_note_powers('Clean:') \
        .multiband_boost(ChordHelper(amplitude=-500, resting=0).set_note('C#').chord('maj').get_notes()) \
        .calculate_note_powers('Boost:') \
        .to_time_domain()\
        .normalize()\
        .save_to_wav("output/clean-0.wav")

    sound.normalize()\
        .save_to_wav("output/src.wav")


if __name__ == "__main__":
    main()
