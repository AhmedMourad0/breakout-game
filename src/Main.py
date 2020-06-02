import time

from src.CollisionDetectors import *
from src.Drawing import *
from src.model.CollisionSide import *
from src.model.Core import *
from src.model.Targets import *

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_INSETS = 20

window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, Wall.bottomless(WINDOW_INSETS))

BAT_WIDTH = 100
BAT_HEIGHT = 10
# this doesn't matter because the mouse motion detector is instantly called when the app is launched
BAT_INITIAL_X = 0
BAT_Y = 40

bat = Bat(BAT_INITIAL_X, BAT_Y, BAT_WIDTH, BAT_HEIGHT)

BALL_LENGTH = 20
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 100

ball = Ball(window, BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)

FLEET_SPACING = 10
FLEET_HORIZONTAL_PADDING = 10
FLEET_INITIALLY_VISIBLE_ROW_COUNT = 5
FLEET_SLIDE_DOWN_TIME_GAP = 10

ROW_VERTICAL_PADDING = 10
ROW_MAX_TARGETS = 13
ROW_SPACING = 10

GROUP_SPACING = 10

TARGET_WIDTH = 50
TARGET_HEIGHT = 20

result = Result()

fleet = Fleet.from_specs(
    window,
    FLEET_SPACING,
    FLEET_HORIZONTAL_PADDING,
    FLEET_INITIALLY_VISIBLE_ROW_COUNT,
    FLEET_SLIDE_DOWN_TIME_GAP,
    TargetsRowSpecs(ROW_SPACING, TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (1, 0, 1)
        ), GROUP_SPACING, 4
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 5
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (1, 0, 1)
        ), GROUP_SPACING, 4
    )
                    ), TargetsRowSpecs(ROW_SPACING, TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 3
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT - 10,
            (1, 0, 1)
        ), GROUP_SPACING, 7
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 3
    )
                                       ), EmptyTargetsRowSpecs(), TargetsRowSpecs(ROW_SPACING, TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (1, 0, 1)
        ), GROUP_SPACING, 4
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 5
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (1, 0, 1)
        ), GROUP_SPACING, 4
    )), TargetsRowSpecs(ROW_SPACING, TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 3
    ), EmptyTargetsGroupSpecs(
        GROUP_SPACING,
        7,
        TARGET_WIDTH
    ), TargetsGroupSpecs(
        TargetSpecs(
            TARGET_WIDTH,
            TARGET_HEIGHT,
            (0, 0, 1)
        ), GROUP_SPACING, 3
    )
                        )
)

collided = []

MOUSE_INITIAL_X = window.inner.horizontal_center()
MOUSE_INITIAL_Y = window.inner.vertical_center()
MOUSE_X_LOWER_LIMIT = window.inner.left + bat.width() / 2
MOUSE_X_UPPER_LIMIT = window.inner.right - bat.width() / 2

mouse = Mouse(
    MOUSE_INITIAL_X,
    MOUSE_INITIAL_Y,
    MOUSE_X_LOWER_LIMIT,
    MOUSE_X_UPPER_LIMIT,
    glutWarpPointer
)

time_since_slide_down = time.time()
timeInterval = 1
is_paused = False

show = True


# noinspection PyUnusedLocal
def mouse_motion(x, y):
    global mouse
    if not is_paused:
        mouse.move(x, y)


# noinspection PyUnusedLocal
def mouse_interaction(button, state, x, y):
    global show
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        ball.is_glued_to_bat = False
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        show = not show


# noinspection PyUnusedLocal
def keyboard(key, x, y):
    global is_paused
    if key.lower() == b"q":
        sys.exit(0)
    elif key == chr(27).encode():  # ESC key
        is_paused = not is_paused


# noinspection PyUnusedLocal
def keyboard_special(key, x, y):
    if key == GLUT_KEY_F11:
        glutFullScreenToggle()


# noinspection PyUnusedLocal
def timer(v):
    if not is_paused:
        display()
    glutTimerFunc(timeInterval, timer, 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    handle_fleet_slide_down()
    ball.move_one_frame(bat)
    handle_ball_wall_collision()
    bat.move_by_horizontal_center(mouse)
    handle_ball_bat_collision()
    handle_ball_fleet_collision()
    draw_results_text(window, result)
    draw_ball(ball)
    draw_bat(bat)
    draw_fleet(window, fleet)

    glColor(0.8, 0.8, 0.8)
    for item in collided:
        draw_rectangle(Rectangle(
            item.left,
            item.bottom,
            item.right,
            item.top
        ))

    if show:
        for row in fleet.rows:
            if type(row) is not EmptyTargetsRow:
                for group in row.target_groups:
                    if type(group) is not EmptyTargetsGroup:
                        glColor(0.1, 0.1, 0.1)
                        draw_rectangle(Rectangle(
                            group.left,
                            group.bottom(row.bottom(fleet, window), fleet.row_height),
                            group.left + group.width,
                            group.bottom(row.bottom(fleet, window), fleet.row_height) + group.target_specs.height
                        ))

    glutSwapBuffers()


def handle_fleet_slide_down():
    global time_since_slide_down
    if time.time() - time_since_slide_down >= fleet.slide_down_time_gap:
        fleet.slide_down_if_needed()
        time_since_slide_down = time.time()


def handle_ball_wall_collision():
    global ball

    if ball.is_glued_to_bat:
        return None

    collision_direction = detect_collision_from_inside(ball, window.inner)

    if collision_direction is None:
        return None

    if collision_direction.primary == CollisionSide.Primary.RIGHT:
        ball.delta_x = -abs(ball.delta_x)
    elif collision_direction.primary == CollisionSide.Primary.LEFT:
        ball.delta_x = abs(ball.delta_x)
    elif collision_direction.primary == CollisionSide.Primary.TOP:
        ball.delta_y = -abs(ball.delta_y)
    elif collision_direction.primary == CollisionSide.Primary.BOTTOM:
        if ball.top < window.inner.bottom:  # game over
            ball = Ball(window, BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)
            ball.move_one_frame(bat)
            result.pc = result.pc + 1

    return collision_direction


def handle_ball_bat_collision():

    if ball.is_glued_to_bat:
        return None

    collision_direction = detect_collision_from_outside(ball, bat)

    if collision_direction is None:
        return None

    if collision_direction.primary == CollisionSide.Primary.RIGHT:
        if collision_direction.secondary == CollisionSide.Secondary.RIGHT_TOP:
            ball.delta_x = abs(ball.delta_x)
            ball.delta_y = abs(ball.delta_y)
            ball.move_by_left(bat.right)
        elif collision_direction.secondary == CollisionSide.Secondary.RIGHT_BOTTOM:
            ball.delta_x = abs(ball.delta_x)
            ball.delta_y = -abs(ball.delta_y)
            ball.move_by_left(bat.right)
    elif collision_direction.primary == CollisionSide.Primary.LEFT:
        if collision_direction.secondary == CollisionSide.Secondary.LEFT_TOP:
            ball.delta_x = -abs(ball.delta_x)
            ball.delta_y = abs(ball.delta_y)
            ball.move_by_right(bat.left)
        elif collision_direction.secondary == CollisionSide.Secondary.LEFT_BOTTOM:
            ball.delta_x = -abs(ball.delta_x)
            ball.delta_y = -abs(ball.delta_y)
            ball.move_by_right(bat.left)
    elif collision_direction.primary == CollisionSide.Primary.TOP:
        ball.delta_y = abs(ball.delta_y)
        ball.move_by_bottom(bat.top)
        result.player = result.player + 1

    return collision_direction


def handle_ball_fleet_collision():
    if ball.is_glued_to_bat:
        return

    interacting_targets = fleet.targets_interacting_with(ball, window)
    colliding_targets = list(filter(
        lambda target: handle_ball_target_collision(target) is not None,
        interacting_targets
    ))

    if len(colliding_targets) > 0:
        fleet.remove_targets(colliding_targets)


def handle_ball_target_collision(target):
    collision_direction = detect_collision_from_outside(ball, target)

    if collision_direction is None:
        return None

    result.player = result.player + 1
    if collision_direction.primary == CollisionSide.Primary.RIGHT:
        ball.delta_x = abs(ball.delta_x)
    elif collision_direction.primary == CollisionSide.Primary.LEFT:
        ball.delta_x = -abs(ball.delta_x)
    elif collision_direction.primary == CollisionSide.Primary.TOP:
        ball.delta_y = abs(ball.delta_y)
    elif collision_direction.primary == CollisionSide.Primary.BOTTOM:
        ball.delta_y = -abs(ball.delta_y)

    return collision_direction


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
    glutMouseFunc(mouse_interaction)
    glutSetCursor(GLUT_CURSOR_NONE)
    glutFullScreen()
    init()
    glutMainLoop()


if __name__ == '__main__':
    main()
