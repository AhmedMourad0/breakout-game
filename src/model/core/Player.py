class Player:

    def __init__(self, score, lives, has_infinite_lives):
        self.score = score
        self._lives = lives
        self._has_infinite_lives = has_infinite_lives

    def get_lives(self):
        return self._lives

    def has_infinite_lives(self):
        return self._has_infinite_lives

    def lose_one_life(self):
        if not self._has_infinite_lives:
            self._lives -= 1

    def has_remaining_lives(self):
        return self._has_infinite_lives or self._lives > 0

    @staticmethod
    def infinite_lives(score):
        return Player(score, 1, True)

    @staticmethod
    def limited_lives(score, lives):
        return Player(score, lives, False)
