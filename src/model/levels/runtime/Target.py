from src.model.base.Rectangle import Rectangle


class Target(Rectangle):
    def __init__(self, left, bottom, specs, row_index, group_index, target_index):
        super().__init__(left, bottom, left + specs.width, bottom + specs.height)
        self.color = specs.color
        self.row_index = row_index
        self.group_index = group_index
        self.target_index = target_index
