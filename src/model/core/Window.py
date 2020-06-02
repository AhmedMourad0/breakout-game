from src.model.core.Rectangle import Rectangle


class Window:
    def __init__(self, width, height, wall):
        self.outer = Rectangle(0, 0, width, height)
        self.inner = Rectangle(
            wall.left_thickness,
            wall.bottom_thickness,
            width - wall.right_thickness,
            height - wall.top_thickness
        )
        self.wall = wall
