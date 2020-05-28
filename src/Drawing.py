from OpenGL.GL import *
from OpenGL.GLUT import *


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
