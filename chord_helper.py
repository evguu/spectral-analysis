class ChordHelper:
    def __init__(self, amplitude, resting):
        self.arr = [0 for i in range(12)]
        self.amplitude = amplitude
        self.resting = resting

    def set_note(self, note_name):
        name_dict = {
            'C': 0,
            'C#': 1,
            'D': 2,
            'D#': 3,
            'E': 4,
            'F': 5,
            'F#': 6,
            'G': 7,
            'G#': 8,
            'A': 9,
            'A#': 10,
            'B': 11
        }

        self.arr[name_dict[note_name]] = 1
        return self

    def get_notes(self):
        return [self.amplitude if i else self.resting for i in self.arr]

    def chord(self, chord_name):
        chord_configs = {
            'maj': [4, 7],
            'min': [3, 7],
            'dim': [3, 6],
            'aug': [4, 8]
        }

        for i in range(12):
            if self.arr[i] == 1:
                for j in chord_configs[chord_name]:
                    self.arr[(i + j) % 12] = 1
                break
        return self