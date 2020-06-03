import time

from src.CollisionDetectors import *
from src.Drawing import *
from src.LevelsLoader import *
from src.model.core.Ball import Ball
from src.model.core.Bat import Bat
from src.model.core.Mouse import Mouse
from src.model.core.Player import Player
from src.model.core.Wall import Wall
from src.model.core.Window import Window

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_INSETS = 20


def create_window():
    return Window(WINDOW_WIDTH, WINDOW_HEIGHT, Wall.bottomless(WINDOW_INSETS))


window = create_window()  # TODO: draw wall

BAT_WIDTH = 100
BAT_HEIGHT = 10
# this doesn't matter because the mouse motion detector is instantly called when the app is launched
BAT_INITIAL_X = 0
BAT_Y = 50


def create_bat():
    return Bat(BAT_INITIAL_X, BAT_Y, BAT_WIDTH, BAT_HEIGHT)


bat = create_bat()

BALL_LENGTH = 16
BALL_INITIAL_X = 100
BALL_INITIAL_Y = 100


def create_ball():
    return Ball(window, BALL_INITIAL_X, BALL_INITIAL_Y, BALL_LENGTH)


ball = create_ball()


def create_player():
    return Player.infinite_lives()


player = create_player()

all_levels = load_levels()
current_level = all_levels[1]

fleet = current_level.create_fleet(window)

MOUSE_INITIAL_X = window.inner.horizontal_center()
MOUSE_INITIAL_Y = window.inner.vertical_center()
MOUSE_X_LOWER_LIMIT = window.inner.left + bat.width() / 2
MOUSE_X_UPPER_LIMIT = window.inner.right - bat.width() / 2


def create_mouse():
    return Mouse(
        MOUSE_INITIAL_X,
        MOUSE_INITIAL_Y,
        MOUSE_X_LOWER_LIMIT,
        MOUSE_X_UPPER_LIMIT,
        glutWarpPointer
    )


mouse = create_mouse()

time_since_slide_down = time.time()  # TODO: account for pausing
timeInterval = 1
is_paused = False


# noinspection PyUnusedLocal
def mouse_motion(x, y):
    global mouse
    if not is_paused:
        mouse.move(x, y)


# noinspection PyUnusedLocal
def mouse_interaction(button, state, x, y):
    global player
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if (not player.has_remaining_lives()) or (fleet.is_destroyed() and current_level.is_last_level(all_levels)):
            restart_from_first_level()
        else:
            ball.is_glued_to_bat = False


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

    if fleet.is_destroyed():
        if current_level.is_last_level(all_levels):
            draw_you_won()
        else:
            move_to_next_level()
    else:
        if player.has_remaining_lives():
            continue_playing()
        else:
            draw_you_lost()

    glutSwapBuffers()


def continue_playing():
    handle_fleet_slide_down()
    ball.move_one_frame(bat)
    handle_ball_wall_collision()
    bat.move_by_horizontal_center(mouse)
    handle_ball_bat_collision()
    handle_ball_fleet_collision()
    draw_results_text(window, player)
    draw_level_name(f"{current_level.display_name}")
    draw_ball(ball)
    draw_bat(bat)
    draw_fleet(window, fleet)


def move_to_next_level():
    move_to_level(current_level.index + 1)


def restart_from_first_level():
    global player
    move_to_level(0)
    player = Player()


def move_to_level(level_index):
    global current_level
    global fleet
    global time_since_slide_down
    global ball
    current_level = all_levels[level_index]
    fleet = current_level.create_fleet(window)
    time_since_slide_down = time.time()
    ball = create_ball()


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
            ball = create_ball()
            ball.move_one_frame(bat)
            player.lose_one_life()

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

    player.score = player.score + 1
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
