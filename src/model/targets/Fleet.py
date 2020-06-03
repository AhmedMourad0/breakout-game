import copy

from src.model.targets.TargetsGroup import EmptyTargetsGroup, TargetsGroup
from src.model.targets.TargetsRow import EmptyTargetsRow
from src.model.targets.TargetsRow import TargetsRow
from src.model.targets.specs.TargetsRowSpecs import EmptyTargetsRowSpecs


class Fleet:

    def __init__(
            self,
            row_height,
            spacing,
            horizontal_padding,
            slide_down_time_gap,
            width_scale,
            rows,
    ):
        self.row_height = row_height
        self.spacing = spacing
        self.horizontal_padding = horizontal_padding
        self.slide_down_time_gap = slide_down_time_gap
        self.width_scale = width_scale
        self.rows = rows
        self._optimize_fleet(shallow=False)

    def _visible_rows_count(self):
        return len(self.rows) + self.rows[0].position_on_screen

    def slide_down_if_needed(self):
        if len(self.rows) > 0 and self._visible_rows_count() < len(self.rows):
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

        for index, row in enumerate(self.rows):
            if type(row) is not EmptyTargetsRow and row.position_on_screen >= 0:
                interacting_targets += row.targets_interacting_with(collider, self, window, index)

        return interacting_targets

    def is_destroyed(self):
        return len(self.rows) == 0

    def remove_targets(self, targets_to_remove):

        rows_to_optimize = set()

        for target in targets_to_remove:
            rows_to_optimize.add(target.row_index)

        def do_remove_targets(targets):
            if len(targets) > 0:
                do_remove_targets(self._remove_single_target(targets.pop(0), targets))

        do_remove_targets(targets_to_remove)

        for row_index in rows_to_optimize:
            self._optimize_row(row_index)
        self._optimize_fleet(shallow=True)

    def _remove_single_target(self, target, targets_to_tweak):

        # since all colliding targets are removed at once, the target_index and
        # group_index of one target may be affected be the removal of another because
        # we replace the removed target with an empty group, to fix this we tweak other
        # targets to update their attributes
        def tweak(added_groups_count, targets_removed_from_group_count):
            for target_to_tweak in targets_to_tweak:
                if target_to_tweak.row_index == target.row_index:
                    if target_to_tweak.group_index == target.group_index:
                        if target_to_tweak.target_index > target.target_index:
                            target_to_tweak.target_index -= targets_removed_from_group_count
                            target_to_tweak.group_index += added_groups_count
                    elif target_to_tweak.group_index > target.group_index:
                        target_to_tweak.group_index += added_groups_count

        row = self.rows[target.row_index]
        group = row.target_groups[target.group_index]
        if group.size > 1:
            if target.target_index == 0:
                empty_group = EmptyTargetsGroup(target.left, target.width() + group.spacing, 0)
                remaining_of_group = TargetsGroup(
                    target.left + empty_group.width,
                    group.target_specs,
                    group.spacing,
                    group.width - empty_group.width,
                    group.size - 1
                )
                row.target_groups[target.group_index:target.group_index + 1] = [
                    empty_group,
                    remaining_of_group
                ]
                tweak(
                    added_groups_count=1,
                    targets_removed_from_group_count=1
                )
            elif target.target_index == group.size - 1:
                empty_group = EmptyTargetsGroup(
                    target.left - group.spacing,
                    target.width() + group.spacing,
                    0
                )
                remaining_of_group = TargetsGroup(
                    group.left,
                    group.target_specs,
                    group.spacing,
                    group.width - empty_group.width,
                    group.size - 1
                )
                row.target_groups[target.group_index:target.group_index + 1] = [
                    remaining_of_group,
                    empty_group
                ]
                tweak(
                    added_groups_count=1,
                    targets_removed_from_group_count=0
                )
            else:
                empty_group = EmptyTargetsGroup(
                    target.left - group.spacing,
                    target.width() + 2 * group.spacing,
                    0
                )
                left_remaining_of_group = TargetsGroup(
                    group.left,
                    group.target_specs,
                    group.spacing,
                    target.width() * target.target_index + group.spacing * (target.target_index - 1),
                    target.target_index
                )
                right_remaining_of_group = TargetsGroup(
                    empty_group.left + empty_group.width,
                    copy.deepcopy(group.target_specs),
                    group.spacing,
                    group.width - empty_group.width - left_remaining_of_group.width,
                    group.size - left_remaining_of_group.size - 1
                )
                row.target_groups[target.group_index:target.group_index + 1] = [
                    left_remaining_of_group,
                    empty_group,
                    right_remaining_of_group
                ]
                tweak(
                    added_groups_count=2,
                    targets_removed_from_group_count=target.target_index + 1
                )
        else:
            empty_group = EmptyTargetsGroup(
                target.left,
                target.width(),
                0
            )
            row.target_groups[target.group_index] = empty_group

        return targets_to_tweak

    def _optimize_fleet(self, shallow):

        if not shallow:
            for i in range(len(self.rows)):
                self._optimize_row(i)

        while len(self.rows) > 0 and type(self.rows[-1]) is EmptyTargetsRow:
            self.rows.pop(-1)

    def _optimize_row(self, row_index):

        row = self.rows[row_index]

        if type(row) is EmptyTargetsRow:
            return

        groups = []
        for group in row.target_groups:
            if type(group) is not EmptyTargetsGroup:
                groups.append(group)
            else:
                if len(groups) == 0:
                    groups.append(group)
                else:
                    last_group = groups[-1]
                    if type(last_group) is EmptyTargetsGroup:
                        groups[-1] = EmptyTargetsGroup(
                            last_group.left,
                            last_group.width + group.width,
                            last_group.sealed_balls + group.sealed_balls
                        )

        if len(groups) == 1 and type(groups[0]) is EmptyTargetsGroup:
            self.rows[row_index] = EmptyTargetsRow(groups[0].sealed_balls, row.position_on_screen)
        else:
            row.target_groups = groups

    @staticmethod
    def from_specs(
            window,
            spacing,
            horizontal_padding,
            initially_visible_rows_count,
            slide_down_time_gap,
            *target_rows_specs
    ):
        rows = _construct_targets_rows(
            initially_visible_rows_count,
            target_rows_specs,
            window.inner.left + horizontal_padding
        )
        width_scale = Fleet._width_scale_for(horizontal_padding, window, target_rows_specs)
        Fleet._apply_width_scale(rows, width_scale)
        return Fleet(
            row_height=max(target_rows_specs, key=_find_row_height).height,
            spacing=spacing,
            horizontal_padding=horizontal_padding * width_scale,
            slide_down_time_gap=slide_down_time_gap,
            width_scale=width_scale,
            rows=rows
        )

    @staticmethod
    def _width_scale_for(horizontal_padding, window, target_rows_specs):
        max_row_width = max(target_rows_specs, key=_find_row_width).width
        return (window.inner.width() - horizontal_padding * 2) / max_row_width

    @staticmethod
    def _apply_width_scale(rows, width_scale):
        for row in rows:
            if type(row) is not EmptyTargetsRow:
                row.apply_width_scale(width_scale)


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
            rows.append(TargetsRow.from_specs(specs, left, starting_position + index))
    return rows
