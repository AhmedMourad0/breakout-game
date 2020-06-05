class Player:

    def __init__(self, score, lives, has_infinite_lives):
        self.score = score
        self._lives = lives
        self._has_infinite_lives = has_infinite_lives

    def get_lives(self):
        """
        :returns The count of remaining lives this player has
        """
        return self._lives

    def has_infinite_lives(self):
        """
        :returns True if this player is immortal, False otherwise
        """
        return self._has_infinite_lives

    def lose_one_life(self):
        """
        Reduces the lives count of this player by one
        """
        if not self._has_infinite_lives:
            self._lives -= 1

    def has_remaining_lives(self):
        """
        :returns True is this player has any remaining lives, False if he's dead
        """
        return self._has_infinite_lives or self._lives > 0

    def is_player_a_cat(self):
        """
        Check's if this player, is indeed, a cat
        :returns True if this player is a cat, False otherwise
        """
        return self._lives == 9

    @staticmethod
    def infinite_lives(score):
        """
        :param score: the initial score of this player
        :returns A new player object with infinite lives
        """
        return Player(score, 1, True)

    @staticmethod
    def limited_lives(score, lives):
        """
        :param score: the initial score of this player
        :param lives: the initial number of lives this player has
        :returns A new player object with a given number of lives
        """
        return Player(score, lives, False)
