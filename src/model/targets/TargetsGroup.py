from src.model.targets.Target import Target


class TargetsGroup:

    def __init__(self, left, target_specs, spacing, width, size):
        self.left = left
        self.target_specs = target_specs
        self.spacing = spacing
        self.width = width
        self.size = size

    def apply_width_scale(self, window_inner_left, width_scale):
        self.left = (self.left - window_inner_left) * width_scale + window_inner_left
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

    def targets_interacting_with(self, collider, row_bottom, row_height, row_index, group_index):

        if not self.is_interacting_with(collider, row_bottom, row_height):
            return []

        interacting_targets = []

        for index in range(self.size):
            target_left = self.target_left(index)
            interacting_targets.append(
                Target(
                    target_left,
                    self.bottom(row_bottom, row_height),
                    self.target_specs,
                    row_index,
                    group_index,
                    index
                )
            )

        return interacting_targets

    @staticmethod
    def from_specs(specs, left):
        return TargetsGroup(
            left=left,
            target_specs=specs.target_specs,
            spacing=specs.spacing,
            width=specs.width,
            size=specs.size
        )


class EmptyTargetsGroup:

    def __init__(self, left, width, sealed_balls):
        self.left = left
        self.width = width
        self.sealed_balls = sealed_balls

    def apply_width_scale(self, window_inner_left, width_scale):
        self.left = (self.left - window_inner_left) * width_scale + window_inner_left
        self.width *= width_scale

    @staticmethod
    def from_specs(specs, left):
        return EmptyTargetsGroup(
            left=left,
            width=specs.width,
            sealed_balls=specs.sealed_balls
        )
