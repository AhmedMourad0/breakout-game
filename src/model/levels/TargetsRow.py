from src.model.levels.TargetsGroup import EmptyTargetsGroup, TargetsGroup
from src.model.levels.specs.TargetsGroupSpecs import EmptyTargetsGroupSpecs


class TargetsRow:

    def __init__(self, spacing, left, position_on_screen, target_groups, width):
        self.spacing = spacing
        self.left = left
        # This's negative if the row is visible on the screen (zero-based)
        self.position_on_screen = position_on_screen
        self.target_groups = target_groups
        self.width = width

    def apply_width_scale(self, window, width_scale):
        """
        Applies the width scale to to this row and all its groups
        :param window: The window the rows are rendered in, this is required because
         the playground is not the entire window and the window's decorations, ie. its wall, should
         not be scaled up or down along with the fleet
        :param width_scale: the width scale
        """
        self.left = (self.left - window.inner.left) * width_scale + window.inner.left
        self.width *= width_scale
        self.spacing *= width_scale
        for group in self.target_groups:
            group.apply_width_scale(window, width_scale)

    def bottom(self, fleet, window):
        """
        :param fleet: The fleet this row is part of
        :param window: The window this row is rendered in
        :return: The y coordinate of the bottom of this row
        """
        return window.inner.top - self.position_on_screen * (
                fleet.row_height + fleet.spacing
        ) - fleet.row_height

    def _is_interacting_with(self, collider, fleet, window):
        """
        :param collider: the collider to check against
        :param fleet: the fleet this row is part of
        :param window: the window the row is rendered in
        :return: True if this row is in the collider's reach and the collider
         can interact with it, False otherwise
        """
        row_bottom = self.bottom(fleet, window)
        row_top = row_bottom + fleet.row_height
        return collider.top >= row_bottom and collider.bottom <= row_top

    def targets_interacting_with(self, collider, fleet, window, row_index):
        """
        Find the targets from this row that are in the collider's reach
        :param collider: the collider to check against
        :param fleet: the fleet this row is part of
        :param window: the window the row is rendered in
        :param row_index: the zero-based index of this row in the fleet it's part of
        :return: All the targets from the groups that are in the collider's reach
        """
        if not self._is_interacting_with(collider, fleet, window):
            return []

        interacting_targets = []

        for index, group in enumerate(self.target_groups):
            if type(group) is not EmptyTargetsGroup:
                interacting_targets += group.targets_interacting_with(
                    collider,
                    self.bottom(fleet, window),
                    fleet.row_height,
                    row_index,
                    index
                )

        return interacting_targets

    @staticmethod
    def from_specs(specs, left, position_on_screen):
        """
         Creates an instance of this class using the specs provided
         :param specs: The specs of this row
         :param left: The x coordinate this row should start from
         :param position_on_screen: The zero-based position of this row on the screen
         :return: The row
         """
        return TargetsRow(
            spacing=specs.spacing,
            left=left,
            position_on_screen=position_on_screen,
            target_groups=_construct_targets_groups(left, specs.spacing, specs.target_groups_specs),
            width=specs.width
        )


class EmptyTargetsRow:

    def __init__(self, sealed_balls, position_on_screen):
        self.sealed_balls = sealed_balls
        # This's negative if the row is visible on the screen
        self.position_on_screen = position_on_screen

    @staticmethod
    def from_specs(specs, position_on_screen):
        """
        Creates an instance of this class using the specs provided
        :param specs: The specs of this row
        :param position_on_screen: The zero-based position of this row on the screen
        :return: The row
        """
        return EmptyTargetsRow(specs.sealed_balls, position_on_screen)


def _construct_targets_groups(row_left, row_spacing, targets_groups_specs):
    """
    Constructs the fleet's groups from their specs
    :param row_left: The x coordinate this row starts from
    :param row_spacing: The spacing between the groups of this row
    :param targets_groups_specs: the specs of the rows's groups
    :return: The constructed groups
    """
    left = row_left
    groups = []
    for specs in targets_groups_specs:
        if type(specs) is EmptyTargetsGroupSpecs:
            groups.append(EmptyTargetsGroup.from_specs(specs, left))
        else:
            groups.append(TargetsGroup.from_specs(specs, left))
        left += (specs.width + row_spacing)
    left -= row_spacing  # Remove extra spacing at the end
    return groups
