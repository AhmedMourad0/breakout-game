class TargetsRowSpecs:
    def __init__(self, *target_groups_specs):
        self.target_groups_specs = target_groups_specs
        self.height = _find_group_height(max(target_groups_specs, key=_find_group_height))


class EmptyTargetsRowSpecs:
    def __init__(self, sealed_balls=0):
        self.sealed_balls = sealed_balls


class TargetsGroupSpecs:
    def __init__(self, target_specs, spacing, size):
        self.target_specs = target_specs
        self.size = size
        self.spacing = spacing
        self.width = target_specs.width * size + spacing * (size - 1)


class EmptyTargetsGroupSpecs:
    def __init__(self, width, sealed_balls=0):
        self.width = width
        self.sealed_balls = sealed_balls


class TargetSpecs:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color


def _find_group_height(group):
    if type(group) is EmptyTargetsGroupSpecs:
        return 0
    else:
        return group.target_specs.height
