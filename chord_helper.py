class ChordHelper:
    def __init__(self, amplitude=1):
        self.arr = [0 for i in range(12)]
        self.amplitude = amplitude

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
        return self.arr * self.amplitude

    def maj(self):
        # Find root note (i), then set i + 4 and i + 7 to 1
        for i in range(12):
            if self.arr[i] == 1:
                self.arr[(i + 4) % 12] = 1
                self.arr[(i + 7) % 12] = 1
                break

        return self

    def min(self):
        # Find root note (i), then set i + 3 and i + 7 to 1
        for i in range(12):
            if self.arr[i] == 1:
                self.arr[(i + 3) % 12] = 1
                self.arr[(i + 7) % 12] = 1
                break

        return self

    def dim(self):
        # Find root note (i), then set i + 3 and i + 6 to 1
        for i in range(12):
            if self.arr[i] == 1:
                self.arr[(i + 3) % 12] = 1
                self.arr[(i + 6) % 12] = 1

        return self

    def aug(self):
        # Find root note (i), then set i + 4 and i + 8 to 1
        for i in range(12):
            if self.arr[i] == 1:
                self.arr[(i + 4) % 12] = 1
                self.arr[(i + 8) % 12] = 1
                break

        return self
