# Given audio file path (mp3 or wav), load it and print the sample count.
from pydub import AudioSegment
from pydub.playback import play


def open_audio_file(file_path):
    sound = AudioSegment.from_file(file_path, format="mp3")
    return sound


def main():
    sound = open_audio_file("input/audio.mp3")
    play(sound)


if __name__ == "__main__":
    main()
