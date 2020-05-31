from src.model.CollisionDirection import *


def detect_collision_from_inside(collider, obstacle):
    if collider.right >= obstacle.inner.right:
        return CollisionDirection(CollisionDirection.Primary.RIGHT, None)
    elif collider.left <= obstacle.inner.left:
        return CollisionDirection(CollisionDirection.Primary.LEFT, None)
    elif collider.top >= obstacle.inner.top:
        return CollisionDirection(CollisionDirection.Primary.TOP, None)
    elif collider.bottom <= obstacle.inner.bottom:
        return CollisionDirection(CollisionDirection.Primary.BOTTOM, None)
    else:
        return None


def detect_collision_from_outside(collider, container):
    if collider.bottom <= container.top and collider.top >= container.bottom:  # ball is in the bat's row
        # the ball.right part is to prevent the case where the ball just falls on the bat's left side
        if collider.left <= container.right <= collider.right:  # ball hit the bat's right side
            if collider.vertical_center() >= container.vertical_center():
                return CollisionDirection(
                    CollisionDirection.Primary.RIGHT,
                    CollisionDirection.Secondary.RIGHT_TOP
                )
            else:
                return CollisionDirection(
                    CollisionDirection.Primary.RIGHT,
                    CollisionDirection.Secondary.RIGHT_BOTTOM
                )
        # the ball.left part is to prevent the case where the ball just falls on the bat's right side
        elif collider.right >= container.left >= collider.left:  # ball hit the bat's left side
            if collider.vertical_center() >= container.vertical_center():
                return CollisionDirection(
                    CollisionDirection.Primary.LEFT,
                    CollisionDirection.Secondary.LEFT_TOP
                )
            else:
                return CollisionDirection(
                    CollisionDirection.Primary.LEFT,
                    CollisionDirection.Secondary.LEFT_BOTTOM
                )
        # ball is above the bat
        elif container.left <= collider.right <= container.right or container.right >= collider.left >= container.left:
            return CollisionDirection(CollisionDirection.Primary.TOP, None)
        else:
            return None
    else:
        return None
