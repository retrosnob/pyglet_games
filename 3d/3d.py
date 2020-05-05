import pyglet
from pyglet.gl import *

pos = [0, 0, -20]
rot_y = 0

config = Config(sample_buffers=1, samples=8)
tela = pyglet.window.Window(height=500, width=500, config=config)

@tela.event
def on_draw():

    global pos_z, rot_y

    tela.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)
    glRotatef(rot_y, 0, 1, 0)

    glBegin(GL_POLYGON)
    glVertex3f(-5,-5,0)
    glVertex3f(5,-5,0)
    glVertex3f(0,5,0)
    glEnd()

    glFlush()

@tela.event
def on_key_press(s,m):

    global pos_z, rot_y

    if s == pyglet.window.key.W:
        pos[2] -= 1
    if s == pyglet.window.key.S:
        pos[2] += 1
    if s == pyglet.window.key.A:
        rot_y += 5
    if s == pyglet.window.key.D:
        rot_y -= 5

pyglet.app.run()