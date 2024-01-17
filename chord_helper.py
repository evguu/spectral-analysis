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
        chord_configs = {  # Warning: unverified code
            'maj': [4, 7],
            'min': [3, 7],
            'dim': [3, 6],
            'aug': [4, 8],
            'sus2': [2, 7],
            'sus4': [5, 7],
            'maj7': [4, 7, 11],
            'min7': [3, 7, 10],
            'dom7': [4, 7, 10],
            'dim7': [3, 6, 9],
            'aug7': [4, 8, 10],
            'maj9': [4, 7, 11, 14],
            'min9': [3, 7, 10, 14],
            'dom9': [4, 7, 10, 14],
            'aug9': [4, 8, 10, 14],
            'sus4b9': [5, 7, 10, 14],
            'add9': [4, 7, 14],
            'sus4b13': [5, 7, 10, 15],
            'add13': [4, 7, 15],
            'maj13': [4, 7, 11, 15],
            'min13': [3, 7, 10, 15],
            'dom13': [4, 7, 10, 15],
            'aug13': [4, 8, 10, 15],
            'sus4b5': [5, 7, 10, 6],
            'add5': [4, 7, 6]
        }

        for i in range(12):
            if self.arr[i] == 1:
                for j in chord_configs[chord_name]:
                    self.arr[(i + j) % 12] = 1
                break
        return self