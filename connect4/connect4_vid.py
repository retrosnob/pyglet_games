from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet import graphics
from pyglet import gl
from math import sin, cos, pi

COLS = 7
ROWS = 6

COL_WIDTH = ROW_HEIGHT = 100

WIN_WIDTH = COLS * COL_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

window = Window(WIN_WIDTH, WIN_HEIGHT)

@window.event
def on_mouse_press(x, y, symbol, modifiers):
    if symbol == mouse.LEFT:
        print(f'The left mouse button was clicked at {x}, {y}, which is column {column(x)}.')

def update(dt):
    pass

@window.event
def on_draw():
    window.clear()
    draw_grid()
    draw_piece(0, 0, ROW_HEIGHT * 0.4, color=(255, 0, 0, 0))

def draw_grid():
    for i in range(ROWS):
        draw_line(0, i*ROW_HEIGHT, WIN_WIDTH, i*ROW_HEIGHT)
    for i in range(COLS):
        draw_line(i*COL_WIDTH, 0, i*COL_WIDTH, WIN_HEIGHT)

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw(
        2, gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c4B', color * 2)
    )

def draw_piece(x, y, size, color=(255, 255, 255, 0)):
    draw_reg_polygon(x * COL_WIDTH + COL_WIDTH // 2, y * ROW_HEIGHT + ROW_HEIGHT // 2, size, 64, color)

def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    vertices = []
    th = 0
    for _ in range(n):
        vertices += [x + r*sin(th), y + r*cos(th)]
        th += 2*pi/n
    graphics.draw(
        n, gl.GL_POLYGON,
        ('v2f', vertices),
        ('c4B', color * n)
    )


def column(x):
    return x // COL_WIDTH

clock.schedule_interval(update, 1/15)

app.run()