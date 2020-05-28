from enum import Enum


class CollisionDirection:

    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary

    class Primary(Enum):
        LEFT = 0,
        BOTTOM = 1,
        RIGHT = 2,
        TOP = 3

    class Secondary(Enum):
        LEFT_TOP = 0,
        LEFT_BOTTOM = 1,
        RIGHT_TOP = 2,
        RIGHT_BOTTOM = 3,
        TOP_LEFT = 4,
        TOP_RIGHT = 5,
        BOTTOM_LEFT = 6,
        BOTTOM_RIGHT = 7


class Rectangle:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def width(self):
        return self.right - self.left

    def height(self):
        return self.top - self.bottom

    def vertical_center(self):
        return self.bottom + (self.height() / 2)

    def update_bottom(self, new_value):
        self.top = new_value + self.height()
        self.bottom = new_value

    def update_right(self, new_value):
        self.left = new_value - self.width()
        self.right = new_value

    def update_left(self, new_value):
        self.right = new_value + self.width()
        self.left = new_value


class Ball(Rectangle):
    def __init__(self, initial_x, initial_y, length):
        super().__init__(initial_x, initial_y, initial_x + length, initial_y + length)


class Wall(Rectangle):
    def __init__(self, width, height, insets):
        super().__init__(insets, 0, width - insets, height - insets)


class Bat(Rectangle):
    def __init__(self, initial_x, y, width, height):
        super().__init__(initial_x, y, initial_x + width, y + height)

# class Row:
#     def __init__(self, count):
#         self.targets = {}
#
# class Target(Rectangle):
#     def __init__(self, row, position,):
