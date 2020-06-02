from src.model.core.Rectangle import Rectangle


class Ball(Rectangle):

    def __init__(self, window, initial_x, initial_y, length, delta_x=3, delta_y=3, is_glued_to_bat=True):
        super().__init__(initial_x, initial_y, initial_x + length, initial_y + length)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.window = window
        self.is_glued_to_bat = is_glued_to_bat

    def move_by_right(self, new_value):
        new_value = self._confine_x_within_walls(new_value)
        self.left = new_value - self.width()
        self.right = new_value

    def move_by_left(self, new_value):
        new_value = self._confine_x_within_walls(new_value)
        self.right = new_value + self.width()
        self.left = new_value

    def move_by_bottom(self, new_value):
        self.top = new_value + self.height()
        self.bottom = new_value

    def move_by_horizontal_center(self, new_value):
        self.move_by_left(new_value - self.width() / 2)

    def _confine_x_within_walls(self, x):
        if self.left < self.window.inner.left:
            return self.window.inner.left
        elif self.right > self.window.inner.right:
            return self.window.inner.right
        else:
            return x

    def move_one_frame(self, bat):
        if self.is_glued_to_bat:
            self.move_by_horizontal_center(bat.horizontal_center())
            self.move_by_bottom(bat.top)
        else:
            self.left = self.left + self.delta_x
            self.right = self.right + self.delta_x
            self.top = self.top + self.delta_y
            self.bottom = self.bottom + self.delta_y
