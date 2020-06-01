from src.model.Rectangle import *
from src.model.TargetsSpecs import *


class Fleet:

    def __init__(
            self,
            window,
            spacing,
            horizontal_padding,
            initially_visible_rows_count,
            slide_down_time_gap,
            *target_rows_specs
    ):
        self.row_height = max(target_rows_specs, key=_find_row_height).height
        self.spacing = spacing
        self.horizontal_padding = horizontal_padding
        self.slide_down_time_gap = slide_down_time_gap
        self.width_scale = self._width_scale_for(window, target_rows_specs)
        self.rows = _construct_targets_rows(
            initially_visible_rows_count,
            target_rows_specs,
            window.inner.left + self.horizontal_padding
        )
        self._apply_width_scale()

    def _apply_width_scale(self):
        for row in self.rows:
            if type(row) is not EmptyTargetsRow:
                row.apply_width_scale(self.width_scale)

    def _width_scale_for(self, window, target_rows_specs):
        max_row_width = max(target_rows_specs, key=_find_row_width).width
        return (window.inner.width() - self.horizontal_padding * 2) / max_row_width

    def _visible_rows_count(self):
        return len(self.rows) + self.rows[0].position_on_screen

    def slide_down_if_needed(self):
        if self._visible_rows_count() < len(self.rows):
            for row in self.rows:
                row.position_on_screen += 1

    def bottom(self, window):
        visible_rows_count = self._visible_rows_count()
        return window.inner.top - visible_rows_count * self.row_height - (visible_rows_count - 1) * self.spacing

    def _is_interacting_with(self, collider, window):
        return collider.top >= self.bottom(window)

    def targets_interacting_with(self, collider, window):

        if not self._is_interacting_with(collider, window):
            return []

        interacting_targets = []

        for row in self.rows:
            if type(row) is not EmptyTargetsRow and row.position_on_screen >= 0:
                interacting_targets += row.targets_interacting_with(collider, self, window)

        return interacting_targets


class TargetsRow:

    def __init__(self, specs, left, position_on_screen):
        self.spacing = specs.spacing
        self.left = left
        self.position_on_screen = position_on_screen
        self.target_groups = _construct_targets_groups(left, self.spacing, specs.target_groups_specs)
        self.width = specs.width

    def apply_width_scale(self, width_scale):
        self.left *= width_scale
        self.width *= width_scale
        self.spacing *= width_scale
        for group in self.target_groups:
            group.apply_width_scale(width_scale)

    def bottom(self, fleet, window):
        return window.inner.top - self.position_on_screen * (
                fleet.row_height + fleet.spacing
        ) - fleet.row_height

    def _is_interacting_with(self, collider, fleet, window):
        row_bottom = self.bottom(fleet, window)
        row_top = row_bottom + fleet.row_height
        return collider.top >= row_bottom and collider.bottom <= row_top

    def targets_interacting_with(self, collider, fleet, window):

        if not self._is_interacting_with(collider, fleet, window):
            return []

        interacting_targets = []

        for group in self.target_groups:
            if type(group) is not EmptyTargetsGroup:
                interacting_targets += group.targets_interacting_with(
                    collider,
                    self.bottom(fleet, window),
                    fleet.row_height
                )

        return interacting_targets


class EmptyTargetsRow:
    def __init__(self, specs, position_on_screen):
        self.sealed_balls = specs.sealed_balls
        self.position_on_screen = position_on_screen


class TargetsGroup:

    def __init__(self, specs, left):
        self.left = left
        self.target_specs = specs.target_specs
        self.spacing = specs.spacing
        self.width = specs.width
        self.size = specs.size

    def apply_width_scale(self, width_scale):
        self.left *= width_scale
        self.width *= width_scale
        self.spacing *= width_scale
        self.target_specs.width *= width_scale

    def bottom(self, row_bottom, row_height):
        return int(row_bottom + (row_height - self.target_specs.height) / 2)

    def target_left(self, position):
        return self.left + position * (self.target_specs.width + self.spacing)

    def target_right(self, target_left):
        return target_left + self.target_specs.width

    def is_interacting_with(self, collider, row_bottom, row_height):
        group_left = self.left
        group_right = self.left + self.width
        group_bottom = self.bottom(row_bottom, row_height)
        group_top = group_bottom + self.target_specs.height
        return collider.right >= group_left and collider.left <= group_right and \
               collider.top >= group_bottom and collider.bottom <= group_top

    def targets_interacting_with(self, collider, row_bottom, row_height):

        if not self.is_interacting_with(collider, row_bottom, row_height):
            return []

        interacting_targets = []

        for index in range(self.size):
            target_left = self.target_left(index)
            interacting_targets.append(
                Rectangle(
                    target_left,
                    self.bottom(row_bottom, row_height),
                    target_left + self.target_specs.width,
                    self.bottom(row_bottom, row_height) + self.target_specs.height
                )
            )

        return interacting_targets


class EmptyTargetsGroup:

    def __init__(self, specs, left):
        self.left = left
        self.width = specs.width
        self.sealed_balls = specs.sealed_balls

    def apply_width_scale(self, width_scale):
        self.left *= width_scale
        self.width *= width_scale


def _find_row_width(row):
    if type(row) is EmptyTargetsRowSpecs:
        return 0
    else:
        return row.width


def _find_row_height(row):
    if type(row) is EmptyTargetsRowSpecs:
        return 0
    else:
        return row.height


def _construct_targets_rows(initially_visible_rows_count, targets_rows_specs, left):
    starting_position = initially_visible_rows_count - len(targets_rows_specs)
    rows = []
    for index, specs in enumerate(targets_rows_specs):
        if type(specs) is EmptyTargetsRowSpecs:
            rows.append(EmptyTargetsRow(specs, starting_position + index))
        else:
            rows.append(TargetsRow(specs, left, starting_position + index))
    return rows


def _construct_targets_groups(row_left, row_spacing, targets_groups_specs):
    left = row_left
    groups = []
    for specs in targets_groups_specs:
        if type(specs) is EmptyTargetsGroupSpecs:
            groups.append(EmptyTargetsGroup(specs, left))
        else:
            groups.append(TargetsGroup(specs, left))
        left += (specs.width + row_spacing)
    left -= row_spacing
    return groups
