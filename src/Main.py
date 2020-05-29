from src.CollisionDetectors import *
from src.Drawing import *
from src.model.CollisionDirection import *
from src.model.Models import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_INSETS = 20

wall = Wall.bottomless(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_INSETS)

BAT_WIDTH = 100
BAT_HEIGHT = 10
# this doesn't matter because the mouse motion detector is instantly called when the app is launched
BAT_INITIAL_X = 0
BAT_Y = 40

bat = Bat(BAT_INITIAL_X, BAT_Y, BAT_WIDTH, BAT_HEIGHT)

BALL_LENGTH = 20
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 100

ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)

ROW_VERTICAL_PADDING = 10
ROW_MAX_TARGETS = 13

TARGET_HORIZONTAL_PADDING = 10
TARGET_WIDTH = wall.width() - (2 * TARGET_HORIZONTAL_PADDING) - TARGET_HORIZONTAL_PADDING * (ROW_MAX_TARGETS - 1)
TARGET_HEIGHT = 40

timeInterval = 1

result = Result()

fleet = Fleet(
    Row(
        TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (1, 0, 1)
            ), ROW_VERTICAL_PADDING, 4
        ), TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (0, 0, 1)
            ), ROW_VERTICAL_PADDING, 5
        ), TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (1, 0, 1)
            ), ROW_VERTICAL_PADDING, 4
        )
    ), Row(
        TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (0, 0, 1)
            ), ROW_VERTICAL_PADDING, 3
        ), TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (1, 0, 1)
            ), ROW_VERTICAL_PADDING, 7
        ), TargetGroupSpecs(
            TargetSpecs(
                TARGET_WIDTH,
                TARGET_HEIGHT,
                TARGET_HORIZONTAL_PADDING,
                (0, 0, 1)
            ), ROW_VERTICAL_PADDING, 3
        )
    )
)

mouse_x = 0


def possible_target_per_row():
    return wall.width() / (TARGET_WIDTH + (TARGET_HORIZONTAL_PADDING * 2))


# noinspection PyUnusedLocal
def mouse_motion(x, y):
    global mouse_x
    mouse_x = x


# noinspection PyUnusedLocal
def keyboard(key, x, y):
    if key == b"q":
        sys.exit(0)
    elif key == chr(27).encode():  # ESC key
        sys.exit(0)


# noinspection PyUnusedLocal
def keyboard_special(key, x, y):
    if key == GLUT_KEY_F11:
        glutFullScreenToggle()


# noinspection PyUnusedLocal
def timer(v):
    display()
    glutTimerFunc(timeInterval, timer, 1)


def display():
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
    text = "PC: " + str(result.pc)
    pc_text_y = WINDOW_HEIGHT - 60
    draw_text(text, 10, pc_text_y)

    text = "Player: " + str(result.player)
    draw_text(text, 10, pc_text_y - 40)


def handle_ball_wall_collision():
    global ball

    ball_wall_collision = detect_ball_wall_collision(ball, wall)

    if ball_wall_collision is None:
        return

    if ball_wall_collision.primary == CollisionDirection.Primary.RIGHT:
        ball.delta_x = -abs(ball.delta_x)
    elif ball_wall_collision.primary == CollisionDirection.Primary.LEFT:
        ball.delta_x = abs(ball.delta_x)
    elif ball_wall_collision.primary == CollisionDirection.Primary.TOP:
        ball.delta_y = -abs(ball.delta_y)
    elif ball_wall_collision.primary == CollisionDirection.Primary.BOTTOM:
        if ball.top < wall.bottom:  # game over
            ball = Ball(BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)
            ball.delta_x = abs(ball.delta_x)
            ball.delta_y = abs(ball.delta_y)
            result.pc = result.pc + 1


def handle_ball_bat_collision():

    ball_bat_collision = detect_ball_bat_collision(ball, bat)

    if ball_bat_collision is None:
        return

    if ball_bat_collision.primary == CollisionDirection.Primary.RIGHT:
        if ball_bat_collision.secondary == CollisionDirection.Secondary.RIGHT_TOP:
            ball.delta_x = abs(ball.delta_x)
            ball.delta_y = abs(ball.delta_y)
            ball.update_left(bat.right)
        elif ball_bat_collision.secondary == CollisionDirection.Secondary.RIGHT_BOTTOM:
            ball.delta_x = abs(ball.delta_x)
            ball.delta_y = -abs(ball.delta_y)
            ball.update_left(bat.right)
    elif ball_bat_collision.primary == CollisionDirection.Primary.LEFT:
        if ball_bat_collision.secondary == CollisionDirection.Secondary.LEFT_TOP:
            ball.delta_x = -abs(ball.delta_x)
            ball.delta_y = abs(ball.delta_y)
            ball.update_right(bat.left)
        elif ball_bat_collision.secondary == CollisionDirection.Secondary.LEFT_BOTTOM:
            ball.delta_x = -abs(ball.delta_x)
            ball.delta_y = -abs(ball.delta_y)
            ball.update_right(bat.left)
    elif ball_bat_collision.primary == CollisionDirection.Primary.TOP:
        ball.delta_y = abs(ball.delta_y)
        ball.update_bottom(bat.top)
        result.player = result.player + 1


def update_ball_position():
    ball.left = ball.left + ball.delta_x
    ball.right = ball.right + ball.delta_x
    ball.top = ball.top + ball.delta_y
    ball.bottom = ball.bottom + ball.delta_y


def update_bat_position():
    bat_half_width = bat.width() / 2
    bat.left = mouse_x - bat_half_width
    bat.right = mouse_x + bat_half_width


def adjust_ball_position():
    if ball.left < wall.left:
        ball.update_left(wall.left)
    elif ball.right > wall.right:
        ball.update_right(wall.right)


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Breakout")
    glutDisplayFunc(display)
    glutTimerFunc(timeInterval, timer, 1)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard_special)
    glutPassiveMotionFunc(mouse_motion)
    glutSetCursor(GLUT_CURSOR_NONE)
    glutFullScreen()
    init()
    glutMainLoop()


if __name__ == '__main__':
    main()
