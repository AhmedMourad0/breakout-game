from src.model.base.Rectangle import Rectangle


class Window:
    def __init__(self, width, height, wall):
        # The real border of the window
        self.outer = Rectangle(0, 0, width, height)
        # The border of the playground that everything should take place in
        self.inner = Rectangle(
            wall.left_thickness,
            wall.bottom_thickness,
            width - wall.right_thickness,
            height - wall.top_thickness
        )
        self.wall = wall
