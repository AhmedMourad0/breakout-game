from src.model.base.Rectangle import Rectangle


class Ball(Rectangle):

    def __init__(self, window, initial_x, initial_y, length, delta_x, delta_y, is_glued_to_bat):
        super().__init__(initial_x, initial_y, initial_x + length, initial_y + length)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self._x_lower_limit = window.inner.left
        self._x_upper_limit = window.inner.right
        self.is_glued_to_bat = is_glued_to_bat

    def move_by_right(self, new_value):
        """
        Moves the ball by its right side while maintaining its width and height
        :param new_value: the new right coords
        """
        new_value = self._confine_x_within_limits(new_value)
        self.left = new_value - self.width()
        self.right = new_value

    def move_by_left(self, new_value):
        """
        Moves the ball by its left side while maintaining its width and height
        :param new_value: the new left coords
        """
        new_value = self._confine_x_within_limits(new_value)
        self.right = new_value + self.width()
        self.left = new_value

    def move_by_bottom(self, new_value):
        """
        Moves the ball by its bottom side while maintaining its width and height
        :param new_value: the new bottom coords
        """
        self.top = new_value + self.height()
        self.bottom = new_value

    def move_by_horizontal_center(self, new_value):
        """
        Moves the ball by its horizontal center while maintaining its width and height
        :param new_value: the new horizontal center coords
        """
        self.move_by_left(new_value - self.width() / 2)

    def _confine_x_within_limits(self, x):
        """
        Forces `x` to be within the ball's permitted `x` range
        :param x: the x value to force
        :returns `x` if it's valid, otherwise, the lower or upper limit, depending on `x`
        """
        if self.left < self._x_lower_limit:
            return self._x_lower_limit
        elif self.right > self._x_upper_limit:
            return self._x_upper_limit
        else:
            return x

    def move_one_frame(self, bat):
        """
        Moves the ball to its next expected position
        :param bat: the bat interacting with the ball
        """
        if self.is_glued_to_bat:
            self.move_by_horizontal_center(bat.horizontal_center())
            self.move_by_bottom(bat.top)
        else:
            self.left = self.left + self.delta_x
            self.right = self.right + self.delta_x
            self.top = self.top + self.delta_y
            self.bottom = self.bottom + self.delta_y
