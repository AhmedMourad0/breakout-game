from enum import Enum


class CollisionDirection:

    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary

    class Primary(Enum):
        LEFT = 0,
        BOTTOM = 1,
        RIGHT = 2,
        TOP = 3

    class Secondary(Enum):
        LEFT_TOP = 0,
        LEFT_BOTTOM = 1,
        RIGHT_TOP = 2,
        RIGHT_BOTTOM = 3,
        TOP_LEFT = 4,
        TOP_RIGHT = 5,
        BOTTOM_LEFT = 6,
        BOTTOM_RIGHT = 7
