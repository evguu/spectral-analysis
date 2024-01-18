from fft_utils import TimeDomainRepresentation
from chord_helper import ChordHelper


def main():
    TimeDomainRepresentation()\
        .load_from("input/rick.MP3", 'mp3')\
        .to_frequency_domain()\
        .calculate_note_powers('Initial')\
        .to_time_domain(leave_every=5)\
        .save_to_wav("output/clean-0.wav")

    TimeDomainRepresentation() \
        .load_from("output/clean-0.wav", 'wav') \
        .to_frequency_domain() \
        .calculate_note_powers('Modified')


if __name__ == "__main__":
    main()
