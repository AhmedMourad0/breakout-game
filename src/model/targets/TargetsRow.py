from src.model.targets.TargetsGroup import EmptyTargetsGroup, TargetsGroup
from src.model.targets.specs.TargetsGroupSpecs import EmptyTargetsGroupSpecs


class TargetsRow:

    def __init__(self, spacing, left, position_on_screen, target_groups, width):
        self.spacing = spacing
        self.left = left
        self.position_on_screen = position_on_screen
        self.target_groups = target_groups
        self.width = width

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

    def targets_interacting_with(self, collider, fleet, window, row_index):

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
        self.position_on_screen = position_on_screen

    @staticmethod
    def from_specs(specs, position_on_screen):
        return EmptyTargetsRow(specs.sealed_balls, position_on_screen)


def _construct_targets_groups(row_left, row_spacing, targets_groups_specs):
    left = row_left
    groups = []
    for specs in targets_groups_specs:
        if type(specs) is EmptyTargetsGroupSpecs:
            groups.append(EmptyTargetsGroup.from_specs(specs, left))
        else:
            groups.append(TargetsGroup.from_specs(specs, left))
        left += (specs.width + row_spacing)
    left -= row_spacing
    return groups
