from OpenGL.GL import *
from OpenGL.GLUT import *

from src.model.base.Rectangle import Rectangle
from src.model.levels.runtime.TargetsGroup import EmptyTargetsGroup
from src.model.levels.runtime.TargetsRow import EmptyTargetsRow


def _draw_rectangle(rect):
    """
    Draws a rectangle on the screen
    :param rect: the rectangle to draw
    """
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex(rect.left, rect.bottom, 0)
    glVertex(rect.right, rect.bottom, 0)
    glVertex(rect.right, rect.top, 0)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def _draw_text(text, x, y, scale, mono=False, bold=False):
    """
    Draws text on the screen
    :param text: the text to draw
    :param x: the x coordinate of the left of the text
    :param y: the y coordinate of the bottom of the text
    :param scale: the width and height scale to apply to the text
    :param mono: whether to use a monospaced font or not
    :param bold: whether the text should be bold or not
    """
    if bold:
        glLineWidth(5)
    else:
        glLineWidth(2)
    glColor(1, 1, 0)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(scale, scale, 1)
    if mono:
        font = GLUT_STROKE_MONO_ROMAN
    else:
        font = GLUT_STROKE_ROMAN
    for char in text.encode():
        glutStrokeCharacter(font, char)


def draw_results_text(window, player):
    """
    Draws the result of the player
    :param window: the window to draw in
    :param player: the player to draw the results of
    """
    bottom = 20
    left = window.outer.right - 240
    scale = 0.12

    if player.has_infinite_lives():
        text = "Lives: Infinite"
    else:
        text = f"Lives: {str(player.get_lives())}"
    _draw_text(text, left + 120, bottom, scale)

    text = f"Score: {str(player.score)}"
    _draw_text(text, left + 10, bottom, scale)


def draw_you_won():
    """
    Draws the text 'YOU WON!' in the middle of the screen
    """
    _draw_text("YOU WON!", 68, 220, 0.8, mono=True, bold=True)


def draw_you_lost():
    """
    Draws the text 'YOU LOST!' in the middle of the screen
    """
    _draw_text("YOU LOST!", 30, 220, 0.8, mono=True, bold=True)


def draw_level_name(level_name):
    """
    Draws the level name on the screen
    :param level_name: the level name
    """
    level_name = f"Level: {level_name}"
    _draw_text(level_name, 20, 20, 0.12, mono=True)


def draw_ball(ball):
    """
    Draws a ball on the screen
    :param ball: the ball to draw
    """
    glColor(0, 1, 1)
    _draw_rectangle(ball)


def draw_bat(bat):
    """
    Draws a bat on the screen
    :param bat: the bat to draw
    """
    glColor(0.7, 0.7, 0.7)
    _draw_rectangle(bat)


def draw_bat_landing_pads(window, bat):
    """
    Draws the bat's landing pads on the left and right of the screen
    :param window: the window the bat lives in
    :param bat: the bat doing the landing
    """
    glColor(0.7, 0.7, 0.7)
    # left
    _draw_rectangle(Rectangle(
        0,
        bat.bottom,
        window.wall.left_thickness,
        bat.top
    ))
    # right
    _draw_rectangle(Rectangle(
        window.outer.right - window.wall.right_thickness,
        bat.bottom,
        window.outer.right,
        bat.top
    ))


def draw_fleet(window, fleet):
    """
    Draws the entire fleet on the screen
    :param window: the window to draw the fleet in
    :param fleet: the fleet to draw
    """
    for row in fleet.rows:
        if row.position_on_screen >= 0 and type(row) is not EmptyTargetsRow:
            _draw_targets_row(
                row=row,
                row_height=fleet.row_height,
                row_bottom=row.bottom(fleet, window)
            )


def _draw_targets_row(row, row_height, row_bottom):
    """
    Draws a targets rows on the screen
    :param row: the row to draw
    :param row_height: the height of the row
    :param row_bottom: the y coordinate of the bottom of the row
    """
    for group in row.target_groups:
        if type(group) is EmptyTargetsGroup:
            continue
        else:
            _draw_target_group(
                group=group,
                group_bottom=group.bottom(row_bottom, row_height)
            )


def _draw_target_group(group, group_bottom):
    """
    Draws a targets group on the screen
    :param group: the group to draw
    :param group_bottom: the y coordinate of the bottom of the group
    """
    for position in range(group.size):
        _draw_target(
            specs=group.target_specs,
            target_left=group.target_left(position),
            target_bottom=group_bottom
        )


def _draw_target(specs, target_left, target_bottom):
    """
    Draws a target on the screen
    :param specs: the specs of the target to draw
    :param target_left: the x coordinate of the left of the target
    :param target_bottom: the y coordinate of the bottom of the target
    """
    target_rect = Rectangle(
        target_left,
        target_bottom,
        (target_left + specs.width),
        target_bottom + specs.height
    )
    glColor(specs.color[0], specs.color[1], specs.color[2])
    _draw_rectangle(target_rect)
