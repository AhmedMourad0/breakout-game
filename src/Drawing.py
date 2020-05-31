from OpenGL.GL import *
from OpenGL.GLUT import *

from src.model.Rectangle import *
from src.model.Targets import *


def draw_rectangle(rect):
    glLoadIdentity()
    glBegin(GL_QUADS)
    glVertex(rect.left, rect.bottom, 0)
    glVertex(rect.right, rect.bottom, 0)
    glVertex(rect.right, rect.top, 0)
    glVertex(rect.left, rect.top, 0)
    glEnd()


def draw_text(text, x, y):
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
    draw_text(text, 10, pc_text_y)

    text = "Player: " + str(result.player)
    draw_text(text, 10, pc_text_y - 40)


def draw_ball(ball):
    glColor(1, 1, 1)
    draw_rectangle(ball)


def draw_bat(bat):
    glColor(1, 1, 1)
    draw_rectangle(bat)


def draw_fleet(window, fleet):
    width_scale = fleet.width_scale_for(window)
    for row in fleet.rows:
        if row.position_on_screen >= 0:
            _draw_targets_row(
                row=row,
                row_height=fleet.row_height,
                row_bottom=window.inner.top - row.position_on_screen * (
                            fleet.row_height + fleet.spacing) - fleet.row_height,
                width_scale=width_scale
            )


def _draw_targets_row(row, row_height, row_bottom, width_scale):
    for group in row.target_groups:
        if type(group) is EmptyTargetsGroup:
            continue
        else:
            _draw_target_group(
                group=group,
                group_bottom=int(row_bottom + (row_height - group.target_specs.height) / 2),
                width_scale=width_scale
            )


def _draw_target_group(group, group_bottom, width_scale):
    for position in range(group.size):
        _draw_target(
            specs=group.target_specs,
            target_left=group.left + position * (group.target_specs.width + group.spacing),
            target_bottom=group_bottom,
            width_scale=width_scale
        )


def _draw_target(specs, target_left, target_bottom, width_scale):
    target_rect = Rectangle(
        target_left * width_scale,
        target_bottom,
        (target_left + specs.width) * width_scale,
        target_bottom + specs.height
    )
    glColor(specs.color[0], specs.color[1], specs.color[2])
    draw_rectangle(target_rect)
