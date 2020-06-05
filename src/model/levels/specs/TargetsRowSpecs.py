from src.model.levels.specs.TargetsGroupSpecs import EmptyTargetsGroupSpecs


class TargetsRowSpecs:
    def __init__(self, spacing, *target_groups_specs):
        self.target_groups_specs = target_groups_specs
        self.spacing = spacing
        # A row's height is the height of the tallest of its groups
        self.height = _find_group_height(max(target_groups_specs, key=_find_group_height))
        # A row's width is the sum of its groups width and the spacing between them
        self.width = sum(group.width for group in self.target_groups_specs) + \
                     (len(self.target_groups_specs) - 1) * self.spacing


class EmptyTargetsRowSpecs:
    def __init__(self, sealed_balls):
        self.sealed_balls = sealed_balls


def _find_group_height(group):
    """
    :param group: the group to find the height of
    :return: The height of the group, 0 if it's an empty group
    """
    if type(group) is EmptyTargetsGroupSpecs:
        return 0
    else:
        return group.target_specs.height
