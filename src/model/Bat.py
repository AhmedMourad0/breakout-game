from src.model.base.Rectangle import Rectangle


class Bat(Rectangle):

    def __init__(self, initial_x, y, width, height):
        super().__init__(initial_x, y, initial_x + width, y + height)

    def follow_mouse(self, mouse):
        """
        Moves the bat so that it's horizontal center matches the `mouse`'s x coordinate
        :param mouse: the mouse to follow
        """
        half_width = self.width() / 2
        self.left = mouse.get_x() - half_width
        self.right = mouse.get_x() + half_width
