
class Rectangle:
    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def width(self):
        return self.right - self.left

    def height(self):
        return self.top - self.bottom

    def vertical_center(self):
        return self.bottom + (self.height() / 2)

    def horizontal_center(self):
        return self.left + (self.width() / 2)
