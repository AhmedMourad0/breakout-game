class Player:

    def __init__(self, score=0, lives=5, has_infinite_lives=False):  # TODO: infinite mode
        self.score = score
        self._lives = lives
        self.has_infinite_lives = has_infinite_lives

    def get_lives(self):
        return self._lives

    def lose_one_life(self):
        if not self.has_infinite_lives:
            self._lives -= 1

    def has_remaining_lives(self):
        return self.has_infinite_lives or self._lives > 0

    @staticmethod
    def infinite_lives(score=0):
        return Player(score, 1, True)
