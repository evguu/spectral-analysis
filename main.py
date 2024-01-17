# Given audio file path (mp3 or wav), load it and print the sample count.
from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("input/audio.mp3", format="mp3")
play(sound)
