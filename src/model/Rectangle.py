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

    def update_bottom(self, new_value):
        self.top = new_value + self.height()
        self.bottom = new_value

    def update_right(self, new_value):
        self.left = new_value - self.width()
        self.right = new_value

    def update_left(self, new_value):
        self.right = new_value + self.width()
        self.left = new_value
