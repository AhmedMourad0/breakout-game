class TargetsGroupSpecs:
    def __init__(self, target_specs, spacing, size):
        self.target_specs = target_specs
        self.size = size
        self.spacing = spacing
        # A group's width is the sum of its levels width and the spacing between them
        self.width = target_specs.width * size + spacing * (size - 1)


class EmptyTargetsGroupSpecs:
    def __init__(self, spacing, size, target_width):
        # We take spacing, size and target_width instead of just raw width for convenience
        # A group's width is the sum of its levels width and the spacing between them
        self.width = target_width * size + spacing * (size - 1)
