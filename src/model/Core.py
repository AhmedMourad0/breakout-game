from src.model.Rectangle import *


class Result:
    def __init__(self, player=0, pc=0):
        self.player = player
        self.pc = pc


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


class Window:
    def __init__(self, width, height, wall):
        self.outer = Rectangle(0, 0, width, height)
        self.inner = Rectangle(
            wall.left_thickness,
            wall.bottom_thickness,
            width - wall.right_thickness,
            height - wall.top_thickness
        )
        self.wall = wall


class Wall:

    def __init__(self, left_thickness, bottom_thickness, right_thickness, top_thickness):
        self.left_thickness = left_thickness
        self.bottom_thickness = bottom_thickness
        self.right_thickness = right_thickness
        self.top_thickness = top_thickness

    @staticmethod
    def bottomless(thickness):
        return Wall(thickness, 0, thickness, thickness)


class Bat(Rectangle):

    def __init__(self, initial_x, y, width, height):
        super().__init__(initial_x, y, initial_x + width, y + height)

    def move_by_horizontal_center(self, mouse):
        half_width = self.width() / 2
        self.left = mouse.get_x() - half_width
        self.right = mouse.get_x() + half_width
