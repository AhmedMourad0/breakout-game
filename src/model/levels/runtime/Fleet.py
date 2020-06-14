import copy

from src.model.levels.runtime.TargetsGroup import EmptyTargetsGroup, TargetsGroup
from src.model.levels.runtime.TargetsRow import EmptyTargetsRow
from src.model.levels.runtime.TargetsRow import TargetsRow
from src.model.levels.specs.TargetsRowSpecs import EmptyTargetsRowSpecs


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
        """
        :return: The number of rows visible to the user, empty rows are included only if
         they are not at the bottom of the fleet
        """
        return len(self.rows) + self.rows[0].position_on_screen

    def slide_down_if_needed(self):
        """
        Moves this fleet down by one row, if there are any rows that are not, yet, visible to the user
        """
        if len(self.rows) > 0 and self._visible_rows_count() < len(self.rows):
            for row in self.rows:
                row.position_on_screen += 1

    def bottom(self, window):
        """
        :param window: The windows this fleet is rendered in
        :return: The y coordinate of the bottom of this fleet
        """
        visible_rows_count = self._visible_rows_count()
        return window.inner.top - \
               visible_rows_count * self.row_height - \
               (visible_rows_count - 1) * self.spacing

    def _is_intersecting_with(self, collider, window):
        """
        :param collider: the collider to check against
        :param window: the window the fleet is rendered in
        :return: True if this fleet is in the collider's reach and the collider
         can interact with it, False otherwise
        """
        return collider.top >= self.bottom(window)

    def targets_intersecting_with(self, collider, window):
        """
        Find the targets from this fleet that are in the collider's reach
        :param collider: the collider to check against
        :param window: the window the fleet is rendered in
        :return: All the targets from the groups that are in the collider's reach
        """

        if not self._is_intersecting_with(collider, window):
            return []

        intersecting_targets = []

        for index, row in enumerate(self.rows):
            if type(row) is not EmptyTargetsRow and row.position_on_screen >= 0:
                intersecting_targets += row.targets_intersecting_with(collider, self, window, index)

        return intersecting_targets

    def is_destroyed(self):
        """
        :return: True if this fleet is destroyed, False otherwise
        """
        return len(self.rows) == 0

    def remove_targets(self, targets_to_remove):
        """
        Removes `targets_to_remove` from the fleet and optimizes the fleet
        :param targets_to_remove: The targets to remove from the fleet
        """

        # The rows affected by the removal of these targets
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

        row = self.rows[target.row_index]
        group = row.target_groups[target.group_index]

        def tweak(added_groups_count, targets_removed_from_group_count):
            """
            Since all colliding levels are removed at once, the target_index and
             group_index of one target may be affected be the removal of another ant that
             is because we replace the removed target with an empty group, to fix this
             we tweak other levels to update their attributes
            :param added_groups_count: the number of groups added to the `target`'s row
            :param targets_removed_from_group_count:  the number targets removed from the `target`'s group
            """
            for target_to_tweak in targets_to_tweak:
                if target_to_tweak.row_index == target.row_index:
                    if target_to_tweak.group_index == target.group_index:
                        if target_to_tweak.target_index > target.target_index:
                            target_to_tweak.target_index -= targets_removed_from_group_count
                            target_to_tweak.group_index += added_groups_count
                    elif target_to_tweak.group_index > target.group_index:
                        target_to_tweak.group_index += added_groups_count

        def on_target_at_head_of_group():
            empty_group = EmptyTargetsGroup(target.left, target.width() + group.spacing)
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

        def on_target_at_tail_of_group():
            empty_group = EmptyTargetsGroup(
                target.left - group.spacing,
                target.width() + group.spacing
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

        def on_target_at_middle_of_group():
            empty_group = EmptyTargetsGroup(
                target.left - group.spacing,
                target.width() + 2 * group.spacing
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

        def on_single_target_group():
            empty_group = EmptyTargetsGroup(
                target.left,
                target.width()
            )
            row.target_groups[target.group_index] = empty_group

        if group.size > 1:
            if target.target_index == 0:
                on_target_at_head_of_group()
            elif target.target_index == group.size - 1:
                on_target_at_tail_of_group()
            else:
                on_target_at_middle_of_group()
        else:
            on_single_target_group()

        return targets_to_tweak

    def _optimize_fleet(self, shallow):
        """
        If shallow is False, all rows of this fleet are optimized then the fleet itself
         is optimized by removing the empty rows at its tail

        If shallow is True, no rows are optimized and empty rows at the tail are directly removed
        :param shallow: Whether this is a shallow or deep optimization
        """

        if not shallow:
            for i in range(len(self.rows)):
                self._optimize_row(i)

        while len(self.rows) > 0 and type(self.rows[-1]) is EmptyTargetsRow:
            self.rows.pop(-1)

    def _optimize_row(self, row_index):
        """
        Optimizes this row by collapsing all consecutive empty groups into one empty group.

        If a row only has empty groups, it is collapsed into an empty row.
        :param row_index: The index of the row to optimize
        """

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
                            last_group.width + group.width
                        )

        if len(groups) == 1 and type(groups[0]) is EmptyTargetsGroup:
            self.rows[row_index] = EmptyTargetsRow(row.position_on_screen)
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
        """
        Creates an instance of this class using the specs provided
        :param window: The window the fleet is rendered in
        :param spacing: The spacing between rows of this fleet
        :param horizontal_padding: The horizontal padding of the fleet
        :param initially_visible_rows_count: The number of rows visible to the user
         when the fleet is first rendered
        :param slide_down_time_gap: The time gap between each slide down for the fleet and the next one
        :param target_rows_specs: The specs of the rows of this fleet
        :return: The fleet
        """
        rows = _rows_specs_to_rows(
            initially_visible_rows_count,
            target_rows_specs,
            window.inner.left + horizontal_padding
        )
        # Although our window has a fixed size, the width of the fleet described by the specs
        # is and should be agnostic to it, therefore, when creating the fleet, we scale
        # its width up or down to match our windows' size
        width_scale = Fleet._width_scale_for(horizontal_padding, window, target_rows_specs)
        Fleet._apply_width_scale(window, rows, width_scale)
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
        """
        Finds the appropriate width scale to apply on all the rows to match the window's width
        :param horizontal_padding: The fleet's horizontal padding
        :param window: The window the fleet is rendered in and should match the width of
        :param target_rows_specs: The rows specs of this fleet
        :return: the appropriate width scale for this fleet
        """
        max_row_width = max(target_rows_specs, key=_find_row_width).width + horizontal_padding * 2
        return window.inner.width() / max_row_width

    @staticmethod
    def _apply_width_scale(window, rows, width_scale):
        """
        Applies the width scale to all the rows of this fleet
        :param window: The window the fleet is rendered in, this is required because
         the playground is not the entire window and the window's decorations, ie. the wall, should
         not be scaled up or down along with the fleet
        :param rows: the rows to apply the width scale on
        :param width_scale: the width wcale
        """
        for row in rows:
            if type(row) is not EmptyTargetsRow:
                row.apply_width_scale(window, width_scale)


def _find_row_width(row):
    """
    :param row: the row to find the width of
    :return: The width of the row, 0 if it's an empty row
    """
    if type(row) is EmptyTargetsRowSpecs:
        return 0
    else:
        return row.width


def _find_row_height(row):
    """
    :param row: the row to find the height of
    :return: The height of the row, 0 if it's an empty row
    """
    if type(row) is EmptyTargetsRowSpecs:
        return 0
    else:
        return row.height


def _rows_specs_to_rows(initially_visible_rows_count, targets_rows_specs, left):
    """
    Constructs the fleet's rows from their specs
    :param initially_visible_rows_count: the initial number of rows visible on the screen
    :param targets_rows_specs: the specs of the fleet's rows
    :param left: The x coordinate the rows should start from
    :return: The constructed rows
    """
    # Positive if visible on the screen, negative if not (zero-based)
    starting_position = initially_visible_rows_count - len(targets_rows_specs)
    rows = []
    for index, specs in enumerate(targets_rows_specs):
        if type(specs) is EmptyTargetsRowSpecs:
            rows.append(EmptyTargetsRow.from_specs(specs, starting_position + index))
        else:
            rows.append(TargetsRow.from_specs(specs, left, starting_position + index))
    return rows
