from src.model.TargetsSpecs import *


class Fleet:

    def __init__(self, spacing, horizontal_padding, initially_visible_rows_count, *target_rows_specs):
        self.row_height = max(target_rows_specs, key=_find_row_height).height
        self.rows = _construct_targets_rows(
            initially_visible_rows_count,
            target_rows_specs,
            horizontal_padding
        )
        self.spacing = spacing
        self.horizontal_padding = horizontal_padding

    def width_scale_for(self, window):
        max_row_width = max(self.rows, key=_find_row_width).width
        return window.inner.width() / max_row_width


class TargetsRow:
    def __init__(self, specs, left, position_on_screen):
        self.target_groups = _construct_targets_groups(left, specs.target_groups_specs)
        self.left = left
        self.position_on_screen = position_on_screen
        self.width = sum(group.width for group in self.target_groups)


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


class EmptyTargetsGroup:
    def __init__(self, specs, left):
        self.left = left
        self.width = specs.width
        self.sealed_balls = specs.sealed_balls


def _find_row_width(row):
    if type(row) is EmptyTargetsRow:
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


def _construct_targets_groups(row_left, targets_groups_specs):
    left = row_left
    groups = []
    for specs in targets_groups_specs:
        if type(specs) is EmptyTargetsGroupSpecs:
            groups.append(EmptyTargetsGroup(specs, left))
            left += specs.width
        else:
            groups.append(TargetsGroup(specs, left))
            left += specs.width + specs.spacing
    return groups
