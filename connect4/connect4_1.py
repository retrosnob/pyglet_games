from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet import graphics
from pyglet import gl

COLS = 7 # Don't change.
ROWS = 6 # Don't change.
COL_WIDTH = ROW_HEIGHT = 100 # Change board size by adjusting this. 

WIN_WIDTH = COLS * COL_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

window = Window(WIN_WIDTH, WIN_HEIGHT)
  
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print(f'The left mouse button was pressed at {x}, {y}, which is column {column(x)}')

def update(dt):
    pass

@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw everything.
    draw_grid()

def draw_grid():
    for i in range(ROWS):
        draw_line(0, i*ROW_HEIGHT, WIN_WIDTH, i*ROW_HEIGHT)
    for i in range(COLS):
        draw_line(i*COL_WIDTH, 0, i*COL_WIDTH, WIN_HEIGHT)

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw (
        2, gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c4B', color * 2)
    )

def column(x):
    return x // COL_WIDTH

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()