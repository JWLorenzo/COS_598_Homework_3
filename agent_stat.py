class Stat:
    def __init__(self, name: str, values: list, index=0):
        self.name = name
        self.values = values
        self.index = index

    def get_value(self):
        return self.values[self.index]

    def set_index(self, i: int):
        self.index = i
        if self.index < 0:
            self.index = (self.index + len(self.values)) % len(self.values)
        if self.index >= len(self.values):
            self.index = self.index % len(self.values)

    def change_index(self, delta: int):
        new_index = self.index + delta
        self.set_index(new_index)
