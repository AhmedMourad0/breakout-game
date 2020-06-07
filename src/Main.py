from src.CollisionDetectors import *
from src.Drawing import *
from src.Game import Game

game = Game()


# noinspection PyUnusedLocal
def mouse_motion(x, y):
    if not game.is_paused:
        game.mouse.move(x, y)


# noinspection PyUnusedLocal
def mouse_interaction(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if game.has_finished():
            game.restart_from_first_level()
        else:
            game.ball.is_glued_to_bat = False


# noinspection PyUnusedLocal
def keyboard(key, x, y):
    if key.lower() == b"q":
        sys.exit(0)
    elif key == chr(27).encode():  # ESC key
        game.pause_or_resume()


# noinspection PyUnusedLocal
def keyboard_special(key, x, y):
    if key == GLUT_KEY_F11:
        glutFullScreenToggle()
    elif key == GLUT_KEY_F4:
        game.set_in_infinite_lives_mode(not game.is_in_infinite_lives_mode())
    elif key == GLUT_KEY_F5:
        if not game.current_level.is_first_level():
            game.move_to_previous_level()
    elif key == GLUT_KEY_F6:
        if not game.current_level.is_last_level(game.all_levels):
            game.move_to_next_level()


# noinspection PyUnusedLocal
def timer(v):
    if not game.is_paused:
        display()
    glutTimerFunc(game.time_interval, timer, 1)


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    if game.has_lost():
        draw_you_lost()
    elif game.should_move_to_next_level():
        game.move_to_next_level()
    elif game.has_won():
        draw_you_won()
    else:
        continue_playing()

    glutSwapBuffers()


def continue_playing():
    handle_fleet_slide_down()

    game.ball.move_one_frame(game.bat)
    game.bat.follow_mouse(game.mouse)

    handle_ball_wall_collision()
    handle_ball_bat_collision()
    handle_ball_fleet_collision()

    draw_bat_landing_pads(game.window, game.bat)
    draw_results_text(game.window, game.player)
    draw_level_name(f"{game.current_level.display_name}")
    draw_ball(game.ball)
    draw_bat(game.bat)
    draw_fleet(game.window, game.fleet)


def handle_fleet_slide_down():
    game.slide_fleet_down()


def handle_ball_wall_collision():
    if game.ball.is_glued_to_bat:
        return None

    collision_side = detect_collision_from_inside(game.ball, game.window.inner)

    if collision_side is None:
        return None

    if collision_side.primary == CollisionSide.Primary.RIGHT:
        game.ball.delta_x = -abs(game.ball.delta_x)
    elif collision_side.primary == CollisionSide.Primary.LEFT:
        game.ball.delta_x = abs(game.ball.delta_x)
    elif collision_side.primary == CollisionSide.Primary.TOP:
        game.ball.delta_y = -abs(game.ball.delta_y)
    elif collision_side.primary == CollisionSide.Primary.BOTTOM:
        if game.ball.top < game.window.inner.bottom:  # game over
            game.lose_one_life()

    return collision_side


def handle_ball_bat_collision():
    if game.ball.is_glued_to_bat:
        return None

    collision_side = detect_collision_from_outside(game.ball, game.bat)

    if collision_side is None:
        return None

    if collision_side.primary == CollisionSide.Primary.RIGHT:
        if collision_side.secondary == CollisionSide.Secondary.RIGHT_TOP:
            game.ball.delta_x = abs(game.ball.delta_x)
            game.ball.delta_y = abs(game.ball.delta_y)
            game.ball.move_by_left(game.bat.right)
        elif collision_side.secondary == CollisionSide.Secondary.RIGHT_BOTTOM:
            game.ball.delta_x = abs(game.ball.delta_x)
            game.ball.delta_y = -abs(game.ball.delta_y)
            game.ball.move_by_left(game.bat.right)
    elif collision_side.primary == CollisionSide.Primary.LEFT:
        if collision_side.secondary == CollisionSide.Secondary.LEFT_TOP:
            game.ball.delta_x = -abs(game.ball.delta_x)
            game.ball.delta_y = abs(game.ball.delta_y)
            game.ball.move_by_right(game.bat.left)
        elif collision_side.secondary == CollisionSide.Secondary.LEFT_BOTTOM:
            game.ball.delta_x = -abs(game.ball.delta_x)
            game.ball.delta_y = -abs(game.ball.delta_y)
            game.ball.move_by_right(game.bat.left)
    elif collision_side.primary == CollisionSide.Primary.TOP:
        game.ball.delta_y = abs(game.ball.delta_y)
        game.ball.move_by_bottom(game.bat.top)

    return collision_side


def handle_ball_fleet_collision():
    if game.ball.is_glued_to_bat:
        return

    intersecting_targets = game.fleet.targets_intersecting_with(game.ball, game.window)
    colliding_targets = list(filter(
        lambda target: handle_ball_target_collision(target) is not None,
        intersecting_targets
    ))

    if len(colliding_targets) > 0:
        game.fleet.remove_targets(colliding_targets)


def handle_ball_target_collision(target):
    collision_side = detect_collision_from_outside(game.ball, target)

    if collision_side is None:
        return None

    game.player.score = game.player.score + 1
    if collision_side.primary == CollisionSide.Primary.RIGHT:
        game.ball.delta_x = abs(game.ball.delta_x)
    elif collision_side.primary == CollisionSide.Primary.LEFT:
        game.ball.delta_x = -abs(game.ball.delta_x)
    elif collision_side.primary == CollisionSide.Primary.TOP:
        game.ball.delta_y = abs(game.ball.delta_y)
    elif collision_side.primary == CollisionSide.Primary.BOTTOM:
        game.ball.delta_y = -abs(game.ball.delta_y)

    return collision_side


def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, game.window.outer.width(), 0, game.window.outer.height(), 0, 1)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(game.window.outer.width(), game.window.outer.height())
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Breakout")
    glutDisplayFunc(display)
    glutTimerFunc(game.time_interval, timer, 1)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(keyboard_special)
    glutPassiveMotionFunc(mouse_motion)
    glutMouseFunc(mouse_interaction)
    glutSetCursor(GLUT_CURSOR_NONE)
    glutFullScreen()
    init()
    glutMainLoop()


# TODO: sound and textures
if __name__ == '__main__':
    main()
