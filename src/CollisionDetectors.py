from src.model.CollisionSide import *


def detect_collision_from_inside(collider, container):
    if collider.right >= container.right:
        if collider.vertical_center() >= container.vertical_center():
            return CollisionSide(
                CollisionSide.Primary.RIGHT,
                CollisionSide.Secondary.RIGHT_TOP
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.RIGHT,
                CollisionSide.Secondary.RIGHT_BOTTOM
            )
    elif collider.left <= container.left:
        if collider.vertical_center() >= container.vertical_center():
            return CollisionSide(
                CollisionSide.Primary.LEFT,
                CollisionSide.Secondary.LEFT_TOP
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.LEFT,
                CollisionSide.Secondary.LEFT_BOTTOM
            )
    elif collider.top >= container.top:
        if collider.horizontal_center() >= container.horizontal_center():
            return CollisionSide(
                CollisionSide.Primary.TOP,
                CollisionSide.Secondary.TOP_RIGHT
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.TOP,
                CollisionSide.Secondary.TOP_LEFT
            )
    elif collider.bottom <= container.bottom:
        if collider.horizontal_center() >= container.horizontal_center():
            return CollisionSide(
                CollisionSide.Primary.BOTTOM,
                CollisionSide.Secondary.BOTTOM_RIGHT
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.BOTTOM,
                CollisionSide.Secondary.BOTTOM_LEFT
            )
    else:
        return None


def detect_collision_from_outside(collider, obstacle):
    if obstacle.top >= collider.bottom >= (obstacle.top - abs(collider.delta_y)) \
            and _is_within_obstacle_y_area(collider, obstacle):
        if collider.horizontal_center() >= obstacle.horizontal_center():
            return CollisionSide(
                CollisionSide.Primary.TOP,
                CollisionSide.Secondary.TOP_RIGHT
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.TOP,
                CollisionSide.Secondary.TOP_LEFT
            )
    elif obstacle.bottom <= collider.top <= (obstacle.bottom + abs(collider.delta_y)) \
            and _is_within_obstacle_y_area(collider, obstacle):
        if collider.horizontal_center() >= obstacle.horizontal_center():
            return CollisionSide(
                CollisionSide.Primary.BOTTOM,
                CollisionSide.Secondary.BOTTOM_RIGHT
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.BOTTOM,
                CollisionSide.Secondary.BOTTOM_LEFT
            )
    elif obstacle.left <= collider.right <= obstacle.right \
            and _is_within_obstacle_x_area(collider, obstacle):
        if collider.vertical_center() >= obstacle.vertical_center():
            return CollisionSide(
                CollisionSide.Primary.LEFT,
                CollisionSide.Secondary.LEFT_TOP
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.LEFT,
                CollisionSide.Secondary.LEFT_BOTTOM
            )
    elif obstacle.right >= collider.left >= obstacle.left \
            and _is_within_obstacle_x_area(collider, obstacle):
        if collider.vertical_center() >= obstacle.vertical_center():
            return CollisionSide(
                CollisionSide.Primary.RIGHT,
                CollisionSide.Secondary.RIGHT_TOP
            )
        else:
            return CollisionSide(
                CollisionSide.Primary.RIGHT,
                CollisionSide.Secondary.RIGHT_BOTTOM
            )
    else:
        return None


def _is_within_obstacle_y_area(collider, obstacle):
    return obstacle.left <= collider.right <= obstacle.right or \
           obstacle.right >= collider.left >= obstacle.left


def _is_within_obstacle_x_area(collider, obstacle):
    return obstacle.top >= collider.bottom >= obstacle.bottom or \
           obstacle.bottom <= collider.top <= obstacle.top or \
           (collider.top >= obstacle.top and collider.bottom <= obstacle.bottom)
