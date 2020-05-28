from src.CollisionDetectors import *
from src.Drawing import *
from src.Models import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_INSETS = 20

BAT_WIDTH = 100
BAT_HEIGHT = 10
# this doesn't matter because the mouse motion detector is instantly called when the app is launched
BAT_INITIAL_X = 0
BAT_Y = 40

BALL_LENGTH = 20
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 100

deltaX = 3
deltaY = 3

timeInterval = 1

pcResult = 0
playerResult = 0

ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)
wall = Wall(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_INSETS)
bat = Bat(BAT_INITIAL_X, BAT_Y, BAT_WIDTH, BAT_HEIGHT)

mouse_x = 0


# noinspection PyUnusedLocal
def timer(v):
    display()
    glutTimerFunc(timeInterval, timer, 1)


# noinspection PyUnusedLocal
def mouse_motion(x, y):
    global mouse_x
    mouse_x = x


# noinspection PyUnusedLocal
def keyboard(key, x, y):
    if key == b"q":
        sys.exit(0)


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def display():
    global pcResult
    global playerResult
    global deltaX
    global deltaY
    global ball

    glClear(GL_COLOR_BUFFER_BIT)

    draw_results_text()

    update_ball_position()
    glColor(1, 1, 1)
    draw_rectangle(ball)

    handle_ball_wall_collision()

    update_bat_position()
    draw_rectangle(bat)

    handle_ball_bat_collision()

    adjust_ball_position()

    glutSwapBuffers()


def draw_results_text():
    text = "PC: " + str(pcResult)
    pc_text_y = WINDOW_HEIGHT - 60
    draw_text(text, 10, pc_text_y)

    text = "Player: " + str(playerResult)
    draw_text(text, 10, pc_text_y - 40)


def handle_ball_wall_collision():
    global deltaX
    global deltaY
    global pcResult
    global ball

    ball_wall_collision = detect_ball_wall_collision(ball, wall)

    if ball_wall_collision is None:
        return

    if ball_wall_collision.primary == CollisionDirection.Primary.RIGHT:
        deltaX = -abs(deltaX)
    elif ball_wall_collision.primary == CollisionDirection.Primary.LEFT:
        deltaX = abs(deltaX)
    elif ball_wall_collision.primary == CollisionDirection.Primary.TOP:
        deltaY = -abs(deltaY)
    elif ball_wall_collision.primary == CollisionDirection.Primary.BOTTOM:
        if ball.top < wall.bottom:  # game over
            ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)
            deltaX = abs(deltaX)
            deltaY = abs(deltaY)
            pcResult = pcResult + 1


def handle_ball_bat_collision():
    global deltaX
    global deltaY
    global playerResult

    ball_bat_collision = detect_ball_bat_collision(ball, bat)

    if ball_bat_collision is None:
        return

    if ball_bat_collision.primary == CollisionDirection.Primary.RIGHT:
        if ball_bat_collision.secondary == CollisionDirection.Secondary.RIGHT_TOP:
            deltaX = abs(deltaX)
            deltaY = abs(deltaY)
            ball.update_left(bat.right)
        elif ball_bat_collision.secondary == CollisionDirection.Secondary.RIGHT_BOTTOM:
            deltaX = abs(deltaX)
            deltaY = -abs(deltaY)
            ball.update_left(bat.right)
    elif ball_bat_collision.primary == CollisionDirection.Primary.LEFT:
        if ball_bat_collision.secondary == CollisionDirection.Secondary.LEFT_TOP:
            deltaX = -abs(deltaX)
            deltaY = abs(deltaY)
            ball.update_right(bat.left)
        elif ball_bat_collision.secondary == CollisionDirection.Secondary.LEFT_BOTTOM:
            deltaX = -abs(deltaX)
            deltaY = -abs(deltaY)
            ball.update_right(bat.left)
    elif ball_bat_collision.primary == CollisionDirection.Primary.TOP:
        deltaY = abs(deltaY)
        ball.update_bottom(bat.top)
        playerResult = playerResult + 1


def update_ball_position():
    ball.left = ball.left + deltaX
    ball.right = ball.right + deltaX
    ball.top = ball.top + deltaY
    ball.bottom = ball.bottom + deltaY


def update_bat_position():
    bat_half_width = bat.width() / 2
    bat.left = mouse_x - bat_half_width
    bat.right = mouse_x + bat_half_width


def adjust_ball_position():
    if ball.left < wall.left:
        ball.update_left(wall.left)
    elif ball.right > wall.right:
        ball.update_right(wall.right)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Breakout")
    glutDisplayFunc(display)
    glutTimerFunc(timeInterval, timer, 1)
    glutKeyboardFunc(keyboard)
    glutPassiveMotionFunc(mouse_motion)
    glutSetCursor(GLUT_CURSOR_NONE)
    init()
    glutMainLoop()


if __name__ == '__main__':
    main()
