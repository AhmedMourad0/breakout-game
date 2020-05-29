from src.model.Rectangle import *


class Result:
    def __init__(self, player=0, pc=0):
        self.player = player
        self.pc = pc


class Ball(Rectangle):
    def __init__(self, initial_x, initial_y, length, delta_x=3, delta_y=3):
        super().__init__(initial_x, initial_y, initial_x + length, initial_y + length)
        self.delta_x = delta_x
        self.delta_y = delta_y


class Wall(Rectangle):

    def __init__(self, width, height, left_inset, bottom_inset, right_inset, top_inset):
        super().__init__(left_inset, bottom_inset, width - right_inset, height - top_inset)

    @classmethod
    def bottomless(cls, width, height, insets):
        return Wall(width, height, insets, 0, insets, insets)


class Bat(Rectangle):
    def __init__(self, initial_x, y, width, height):
        super().__init__(initial_x, y, initial_x + width, y + height)


class Fleet:
    def __init__(self, *rows):
        self.rows = rows


class Row:
    def __init__(self, *target_groups_specs):
        targets_count = 0
        groups = []
        for spec in target_groups_specs:
            groups.append(TargetGroup(spec, targets_count))
            targets_count += spec.count
        self.target_groups = groups
        self.height = max(target_groups_specs, key=lambda group: group.height)


class TargetSpecs:
    def __init__(self, width, height, horizontal_padding, color):
        self.width = width
        self.height = height
        self.horizontal_padding = horizontal_padding
        self.color = color


class TargetGroup:
    def __init__(self, group_specs, starting_position):
        self.group_specs = group_specs
        self.starting_position = starting_position


class TargetGroupSpecs:
    def __init__(self, target_specs, vertical_padding, count):
        self.target_specs = target_specs
        self.vertical_padding = vertical_padding
        self.count = count
        self.height = target_specs.height + (2 * vertical_padding)


class EmptyTargetGroupSpecs:
    def __init__(self, count, sealed_balls=0):
        self.count = count
        self.sealed_balls = sealed_balls
