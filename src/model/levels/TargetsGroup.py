from src.model.levels.Target import Target


class TargetsGroup:

    def __init__(self, left, target_specs, spacing, width, size):
        self.left = left
        self.target_specs = target_specs
        self.spacing = spacing
        self.width = width
        self.size = size

    def apply_width_scale(self, window, width_scale):
        """
        Applies the width scale to to this group and all its targets
        :param window: The window the groups is rendered in, this is required because
         the playground is not the entire window and the window's decorations, ie. its wall, should
         not be scaled up or down along with the fleet
        :param width_scale: the width scale
        """
        self.left = (self.left - window.inner.left) * width_scale + window.inner.left
        self.width *= width_scale
        self.spacing *= width_scale
        self.target_specs.width *= width_scale

    def bottom(self, row_bottom, row_height):
        """
        :param row_bottom: The bottom of the row this group is part of
        :param row_height: The height of the row this group is part of
        :return: The y coordinate of the bottom of this group
        """
        return int(row_bottom + (row_height - self.target_specs.height) / 2)

    def target_left(self, position):
        """
        Calculates the x coordinate of the left of a target of this group
        :param position: The zero-based position of the target
        :return: The x coordinate of the left of this target
        """
        return self.left + position * (self.target_specs.width + self.spacing)

    def target_right(self, target_left):
        """
        Calculates the x coordinate of the right of a target of this group
        :param target_left: The x coordinate of the left of this target
        :return: The x coordinate of the right of this target
        """
        return target_left + self.target_specs.width

    def is_interacting_with(self, collider, row_bottom, row_height):
        """
        :param collider: the collider to check against
        :param row_bottom: The bottom of the row this group is part of
        :param row_height: The height of the row this group is part of
        :return: True if this group is in the collider's reach and the collider
         can interact with it, False otherwise
        """
        group_left = self.left
        group_right = self.left + self.width
        group_bottom = self.bottom(row_bottom, row_height)
        group_top = group_bottom + self.target_specs.height
        return collider.right >= group_left and collider.left <= group_right and \
               collider.top >= group_bottom and collider.bottom <= group_top

    def targets_interacting_with(self, collider, row_bottom, row_height, row_index, group_index):
        """
        Find the targets from this group that are in the collider's reach
        :param collider: the collider to check against
        :param row_bottom: The bottom of the row this group is part of
        :param row_height: The height of the row this group is part of
        :param row_index: the zero-based index of the row, this group is part of, in
         the fleet it's part of
        :param group_index: the zero-based index of this group in the row it's part of
        :return: All the targets from this group that are in the collider's reach
        """
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
        """
        Creates an instance of this class using the specs provided
        :param specs: The specs of this group
        :param left: The x coordinate this group should start from
        :return: The group
        """
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

    def apply_width_scale(self, window, width_scale):
        """
        Applies the width scale to to this group
        :param window: The window the groups is rendered in, this is required because
         the playground is not the entire window and the window's decorations, ie. its wall, should
         not be scaled up or down along with the fleet
        :param width_scale: the width scale
        """
        self.left = (self.left - window.inner.left) * width_scale + window.inner.left
        self.width *= width_scale

    @staticmethod
    def from_specs(specs, left):
        """
        Creates an instance of this class using the specs provided
        :param specs: The specs of this group
        :param left: The x coordinate this group should start from
        :return: The group
        """
        return EmptyTargetsGroup(
            left=left,
            width=specs.width,
            sealed_balls=specs.sealed_balls
        )
