class Wall:

    def __init__(self, left_thickness, bottom_thickness, right_thickness, top_thickness):
        self.left_thickness = left_thickness
        self.bottom_thickness = bottom_thickness
        self.right_thickness = right_thickness
        self.top_thickness = top_thickness

    @staticmethod
    def bottomless(thickness):
        """
        :return: A wall object with zero thickness at its bottom (bottomless)
        """
        return Wall(thickness, 0, thickness, thickness)
