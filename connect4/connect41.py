import pyglet

from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet import graphics
from pyglet import image
from math import sin, cos, pi

window = Window(700, 600)

def setup():
    print('Setting up...')
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    global last_col_clicked
    if button == mouse.LEFT and last_col_clicked == -1:
        last_col_clicked = column(x) if last_col_clicked == -1 else -1 # The -1 value indicates that the board has been updated.
        print(f'The left mouse button was pressed at {x}, {y}, which is {last_col_clicked}')

def update(dt):
    global last_col_clicked, player
    if last_col_clicked != -1:
        grid[pieces_per_column[last_col_clicked]][last_col_clicked] = player
        pieces_per_column[last_col_clicked] += 1
        last_col_clicked = -1
        player = 2 if player == 1 else 1
        print(grid)
        print(pieces_per_column)

@window.event
def on_draw():
    # Erase everything.
    window.clear()
    draw_grid()
    draw_piece(4, 3)
    
def draw_piece(x, y, color=(255, 0, 0, 0)):
    """Draws a piece on the board with 0, 0 being the bottom-left and 6, 5 being the top-right)"""
    row_height = window.height//6
    col_width  = window.width//7
    draw_reg_polygon(x * col_width + col_width//2, y * row_height + row_height//2, (row_height - 20)//2, 64, color)

def draw_grid():
    row_height = window.height//6
    col_width  = window.width//7
    for i in range(7):
        draw_line(i*row_height, 0, i*row_height, window.height, color=(127, 127, 255, 0))
    for i in range(6):
        draw_line(0, i*col_width, window.width, i*col_width, color=(127, 127, 255, 0))

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    """Draws a line from x1, y1 to x2, y2"""
    # 2 means that 2 vertices will be supplied, the mode is line drawing
    # v2i means (v)ertices, (2) coordinates per vertex ie 2D, each vertex is an (i)nteger
    # c3B means (c)olor, (3) values per vertex ie RGB, unsigned (B)yte representation
    # there has to be one color per vertex, so in this case 2 lots of 3 values
    pyglet.graphics.draw(
        2, pyglet.gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c4B', color  * 2)
    )

def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    """ Draws a circle of radius r centred on x, y"""
    th = 0
    vertices = []
    for i in range(n):
        vertices += [x + r*sin(th), y + r*cos(th)]
        th += 2*pi/n
    # 3 means that 2 vertices will be supplied, the mode is polygon drawing
    # v2i means (v)ertices, (2) coordinates per vertex ie 2D, each vertex is an (i)nteger
    # c3B means (c)olor, (3) values per vertex ie RGB, unsigned (B)yte representation
    # there has to be one color per vertex, so in this case 2 lots of 3 values
    pyglet.graphics.draw(
        n, pyglet.gl.GL_POLYGON,
        ('v2f', vertices),
        ('c4B', color * n)
    )

def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    img.blit(x, y)

def column(x):
    return x // (window.width//7)

def game_over_condition():
    pass 

# The full connect 4 grid. 0 = empty, 1 = P1's piece, 2 = P2's piece.
grid = [[0] * 7 for i in range(6)]
grid[5][6] = 2
# 1d list keeps track of how many pieces are currently in each column.
# Gives the row into which a new piece should be placed.
pieces_per_column = [0] * 7
print(grid)
player = 1
last_col_clicked = -1

setup()

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()