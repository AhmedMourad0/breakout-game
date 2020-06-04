class Level:
    def __init__(self, simple_name, file_name, index):
        self.display_name = f"{index + 1} - {simple_name}"
        self.file_name = file_name
        self.index = index

    def create_fleet(self, window):
        from src.LevelsLoader import parse_level
        return parse_level(window, self)

    def is_last_level(self, all_levels):
        return self.index >= (len(all_levels) - 1)

    def is_first_level(self):
        return self.index <= 0
