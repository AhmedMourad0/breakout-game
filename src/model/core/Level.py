class Level:
    def __init__(self, simple_name, file_name, index):
        self.display_name = f"{index + 1} - {simple_name}"
        self.file_name = file_name
        self._index = index

    def __str__(self):
        return f"({self.display_name}, {self.file_name}, {self._index})"

    def __repr__(self):
        return f"({self.display_name}, {self.file_name}, {self._index})"

    def create_fleet(self, window):
        from src.LevelsLoader import parse_level
        return parse_level(window, self)

    def is_last_level(self, all_levels):
        return self._index >= (len(all_levels) - 1)
