from src.model.core.Rectangle import Rectangle


class Bat(Rectangle):

    def __init__(self, initial_x, y, width, height):
        super().__init__(initial_x, y, initial_x + width, y + height)

    def move_by_horizontal_center(self, mouse):
        half_width = self.width() / 2
        self.left = mouse.get_x() - half_width
        self.right = mouse.get_x() + half_width
