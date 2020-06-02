from src.model.targets.specs.TargetsGroupSpecs import EmptyTargetsGroupSpecs


class TargetsRowSpecs:
    def __init__(self, spacing, *target_groups_specs):
        self.target_groups_specs = target_groups_specs
        self.spacing = spacing
        self.height = _find_group_height(max(target_groups_specs, key=_find_group_height))
        self.width = sum(group.width for group in self.target_groups_specs) + \
                     (len(self.target_groups_specs) - 1) * self.spacing


class EmptyTargetsRowSpecs:
    def __init__(self, sealed_balls=0):
        self.sealed_balls = sealed_balls


def _find_group_height(group):
    if type(group) is EmptyTargetsGroupSpecs:
        return 0
    else:
        return group.target_specs.height
