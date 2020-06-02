from src.model.core.CollisionSide import CollisionSide


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
    if obstacle.top >= collider.bottom >= obstacle.vertical_center() \
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
    elif obstacle.bottom <= collider.top <= obstacle.vertical_center() \
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
    return collider.right >= obstacle.left and collider.left <= obstacle.right


def _is_within_obstacle_x_area(collider, obstacle):
    return collider.top >= obstacle.bottom and collider.bottom <= obstacle.top
