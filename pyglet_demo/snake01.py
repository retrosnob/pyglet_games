from pyglet import app
from pyglet import gl
from pyglet import clock
from pyglet.window import Window
from pyglet.window import key
from pyglet import graphics
import sys

window = Window(500, 500)

@window.event
def on_draw():
    global snk_x, snk_y, snk_size
    window.clear()
    graphics.draw(4, gl.GL_POLYGON, (
        'v2i', (
            snk_x, snk_y,
            snk_x + snk_size, snk_y,
            snk_x + snk_size, snk_y + snk_size,
            snk_x, snk_y + snk_size)
        ))

@window.event
def on_key_press(symbol, modifiers):
    global snk_dx, snk_dy
    if symbol == key.LEFT:
        snk_dx = -snk_speed
        snk_dy = 0
    elif symbol == key.RIGHT:
        snk_dx = snk_speed
        snk_dy = 0
    elif symbol == key.UP:
        snk_dx = 0
        snk_dy = snk_speed
    elif symbol == key.DOWN:
        snk_dx = 0
        snk_dy = -snk_speed

def update(dt):
    global snk_x, snk_y, snk_dx, snk_dy
    snk_x += snk_dx
    snk_y += snk_dy

snk_speed = 10
snk_dx, snk_dy = 0, 0
snk_x = window.width//2
snk_y = window.height//2
snk_size = 10
clock.schedule_interval(update, 1/15)

app.run()