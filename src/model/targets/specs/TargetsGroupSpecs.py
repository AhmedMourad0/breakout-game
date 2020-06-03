class TargetsGroupSpecs:
    def __init__(self, target_specs, spacing, size):
        self.target_specs = target_specs
        self.size = size
        self.spacing = spacing
        self.width = target_specs.width * size + spacing * (size - 1)


class EmptyTargetsGroupSpecs:
    def __init__(self, spacing, size, target_width, sealed_balls):
        self.width = target_width * size + spacing * (size - 1)
        self.sealed_balls = sealed_balls
