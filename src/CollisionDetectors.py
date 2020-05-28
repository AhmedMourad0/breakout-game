from src.Models import *


def detect_ball_wall_collision(ball, wall):
    if ball.right >= wall.right:
        return CollisionDirection(CollisionDirection.Primary.RIGHT, None)
    elif ball.left <= wall.left:
        return CollisionDirection(CollisionDirection.Primary.LEFT, None)
    elif ball.top >= wall.top:
        return CollisionDirection(CollisionDirection.Primary.TOP, None)
    elif ball.bottom <= wall.bottom:
        return CollisionDirection(CollisionDirection.Primary.BOTTOM, None)
    else:
        return None


def detect_ball_bat_collision(ball, bat):
    if ball.bottom <= bat.top and ball.top >= bat.bottom:  # ball is in the bat's row
        if ball.right <= bat.right and ball.left >= bat.left:  # ball is above the bat
            return CollisionDirection(CollisionDirection.Primary.TOP, None)
        elif ball.left <= bat.right <= ball.right:  # ball hit the bat's right side
            if ball.vertical_center() >= bat.vertical_center():
                return CollisionDirection(
                    CollisionDirection.Primary.RIGHT,
                    CollisionDirection.Secondary.RIGHT_TOP
                )
            else:
                return CollisionDirection(
                    CollisionDirection.Primary.RIGHT,
                    CollisionDirection.Secondary.RIGHT_BOTTOM
                )
        elif ball.right >= bat.left >= ball.left:  # ball hit the bat's left side
            if ball.vertical_center() >= bat.vertical_center():
                return CollisionDirection(
                    CollisionDirection.Primary.LEFT,
                    CollisionDirection.Secondary.LEFT_TOP
                )
            else:
                return CollisionDirection(
                    CollisionDirection.Primary.LEFT,
                    CollisionDirection.Secondary.LEFT_BOTTOM
                )
        else:
            return None
    else:
        return None
