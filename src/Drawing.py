from OpenGL.GL import *
from OpenGL.GLUT import *

from src.model.core.Rectangle import Rectangle
from src.model.targets.TargetsGroup import EmptyTargetsGroup
from src.model.targets.TargetsRow import EmptyTargetsRow


def _draw_rectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex(rect.left, rect.bottom, 0)
    glVertex(rect.right, rect.bottom, 0)
    glVertex(rect.right, rect.top, 0)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def _draw_text(text, x, y):
    glLineWidth(2)
    glColor(1, 1, 0)
    glLoadIdentity()
    glTranslate(x, y, 0)
    glScale(0.13, 0.13, 1)
    for char in text.encode():
        glutStrokeCharacter(GLUT_STROKE_ROMAN, char)


def draw_results_text(window, result):
    text = "PC: " + str(result.pc)
    pc_text_y = window.outer.height() - 60
    _draw_text(text, 10, pc_text_y)

    text = "Player: " + str(result.player)
    _draw_text(text, 10, pc_text_y - 40)


def draw_ball(ball):
    glColor(1, 1, 1)
    draw_rectangle(ball)


def draw_bat(bat):
    glColor(1, 1, 1)
    draw_rectangle(bat)


def draw_fleet(window, fleet):
    for row in fleet.rows:
        if row.position_on_screen >= 0 and type(row) is not EmptyTargetsRow:
            _draw_targets_row(
                row=row,
                row_height=fleet.row_height,
                row_bottom=row.bottom(fleet, window)
            )


def _draw_targets_row(row, row_height, row_bottom):
    for group in row.target_groups:
        if type(group) is EmptyTargetsGroup:
            continue
        else:
            _draw_target_group(
                group=group,
                group_bottom=group.bottom(row_bottom, row_height)
            )


def _draw_target_group(group, group_bottom):
    for position in range(group.size):
        _draw_target(
            specs=group.target_specs,
            target_left=group.target_left(position),
            target_bottom=group_bottom
        )


def _draw_target(specs, target_left, target_bottom):
    target_rect = Rectangle(
        target_left,
        target_bottom,
        (target_left + specs.width),
        target_bottom + specs.height
    )
    glColor(specs.color[0], specs.color[1], specs.color[2])
    draw_rectangle(target_rect)
