from src.model.CollisionDirection import *


def detect_ball_wall_collision(ball, window):
    if ball.right >= window.inner.right:
        return CollisionDirection(CollisionDirection.Primary.RIGHT, None)
    elif ball.left <= window.inner.left:
        return CollisionDirection(CollisionDirection.Primary.LEFT, None)
    elif ball.top >= window.inner.top:
        return CollisionDirection(CollisionDirection.Primary.TOP, None)
    elif ball.bottom <= window.inner.bottom:
        return CollisionDirection(CollisionDirection.Primary.BOTTOM, None)
    else:
        return None


def detect_ball_bat_collision(ball, bat):
    if ball.bottom <= bat.top and ball.top >= bat.bottom:  # ball is in the bat's row
        # the ball.right part is to prevent the case where the ball just falls on the bat's left side
        if ball.left <= bat.right <= ball.right:  # ball hit the bat's right side
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
        # the ball.left part is to prevent the case where the ball just falls on the bat's right side
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
        elif bat.left <= ball.right <= bat.right or bat.right >= ball.left >= bat.left:  # ball is above the bat
            return CollisionDirection(CollisionDirection.Primary.TOP, None)
        else:
            return None
    else:
        return None
