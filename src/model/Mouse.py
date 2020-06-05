class Mouse:

    def __init__(self, x, y, x_lower_limit, x_upper_limit, move_pointer):
        self._x = int(x)
        self._y = int(y)
        self.x_lower_limit = int(x_lower_limit)
        self.x_upper_limit = int(x_upper_limit)
        self.move_pointer = move_pointer

    def get_x(self):
        """
        Gets the x coordinate of the mouse
        :returns the mouse's x coordinate
        """
        return self._x

    def get_y(self):
        """
        Gets the y coordinate of the mouse
        :returns the mouse's y coordinate
        """
        return self._y

    def move(self, x, y):
        """
        Notifies this object that the real mouse pointer has moved to new coordinates
        :param x: the real pointer's x coordinate
        :param y: the real pointer's y coordinate
        """
        x = int(x)
        y = int(y)
        x = self._confine_within_x_limits(x)
        self._x = x
        self._y = y

    def _confine_within_x_limits(self, x):
        """
        Forces the real mouse pointer to stay within its permitted `x` range
        :param x: the x value to force
        :returns `x` if it's valid, otherwise, the lower or upper limit, depending on `x`
        """
        if x > self.x_upper_limit:
            self.move_pointer(self.x_upper_limit, self._y)
            return self.x_upper_limit
        elif x < self.x_lower_limit:
            self.move_pointer(self.x_lower_limit, self._y)
            return self.x_lower_limit
        else:
            return x
