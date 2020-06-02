class Mouse:

    def __init__(self, x, y, x_lower_limit, x_upper_limit, move_pointer):
        self._x = int(x)
        self._y = int(y)
        self.delta_x = 0
        self.delta_y = 0
        self.x_lower_limit = int(x_lower_limit)
        self.x_upper_limit = int(x_upper_limit)
        self.move_pointer = move_pointer

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def move(self, x, y):
        x = int(x)
        y = int(y)
        x = self._confine_within_x_limits(x)
        self.delta_x = self._x - x
        self.delta_y = self._y - y
        self._x = x
        self._y = y

    def _confine_within_x_limits(self, x):
        if x > self.x_upper_limit:
            self.move_pointer(self.x_upper_limit, self._y)
            return self.x_upper_limit
        elif x < self.x_lower_limit:
            self.move_pointer(self.x_lower_limit, self._y)
            return self.x_lower_limit
        else:
            return x
