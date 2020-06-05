class Level:

    def __init__(self, simple_name, file_name, index):
        """
        :param simple_name: the name of the level without indexing or suffixes, eg. 'Arrested'
        :param file_name: the name of the file containing the levels details, without
         its path, eg. '2-Arrested.json'
        :param index: the zero-based order of this level
        """
        self.display_name = f"{index + 1} - {simple_name}"
        self.file_name = file_name
        self.index = index

    def create_fleet(self, window):
        """
        Creates the fleet corresponding to this level
        :param window: the window this level is displayed in
        :returns this level's fleet
        """
        from src.LevelsLoader import parse_level
        return parse_level(window, self)

    def is_last_level(self, all_levels):
        """
        Calculates whether or not this's the last level in `all_levels`
        :param all_levels: a list containing all the levels to check against, including this one
        :returns True if this's the last level in the list, False otherwise
        """
        return self.index >= (len(all_levels) - 1)

    def is_first_level(self):
        """
        Calculates whether or not this's the first level in its levels set
        :returns True if this's the first level, False otherwise
        """
        return self.index <= 0
