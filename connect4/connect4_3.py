from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet import graphics
from pyglet import gl
from math import sin, cos, pi

COLS = 7 # Don't change.
ROWS = 6 # Don't change.
COL_WIDTH = ROW_HEIGHT = 100 # Change board size by adjusting this. 
PIECE_RADIUS = ROW_HEIGHT * 0.4 # Change the multiplier between 0.1 and 0.5 to adjust piece size.

WIN_WIDTH = COLS * COL_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

window = Window(WIN_WIDTH, WIN_HEIGHT)
  
@window.event
def on_mouse_press(x, y, button, modifiers):
    global last_col_clicked
    # The last_col_clicked will be -1 if update has run since the last mouse click so we can use
    # it to determine that the last mouse click has been processed. If this function runs and 
    # last_col_clicked is not -1, then we ignore the click event because the last one hasn't been
    # processed yet.
    if button == mouse.LEFT and last_col_clicked == -1:
        last_col_clicked = column(x) if last_col_clicked == -1 else -1 # Set last_col_clicked to the column the user clicked on.
        # print(f'The left mouse button was pressed at {x}, {y}, which is {last_col_clicked}')

def update(dt):
    global last_col_clicked, player
    # The last_col_clicked is -1 if nothing has been clicked since the last update.
    if last_col_clicked != -1:
        # If pieces_per_column >= ROWS then the column is full, so check for that first.
        if pieces_per_column[last_col_clicked] < ROWS:
            print(f'Player {player} placed a piece in column {last_col_clicked}.')
            # Put the current player (1 or 2) at the correct point in the grid.
            grid[pieces_per_column[last_col_clicked]][last_col_clicked] = player
            # Update the number of pieces in the selected column.
            pieces_per_column[last_col_clicked] += 1
            # TO DO: Check to see if a line of 4 exists
            player = 2 if player == 1 else 1
            print(grid)
            print(pieces_per_column)
        # Make sure we notify the mouse event code that the current click has been processed.
        last_col_clicked = -1

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

def draw_piece(x, y, color=(255, 255, 255, 0)):
    draw_reg_polygon(x * COL_WIDTH + COL_WIDTH // 2, y * ROW_HEIGHT + ROW_HEIGHT // 2, PIECE_RADIUS, 64, color)

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

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw (
        2, gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c4B', color * 2)
    )

def column(x):
    return x // COL_WIDTH

# The full connect 4 grid. 0 = empty, 1 = P1's piece, 2 = P2's piece.
grid = [[0] * COLS for i in range(ROWS)]
# eg 
# [   [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 2, 1, 0, 0], 
#     [0, 0, 0, 1, 2, 0, 0], 
#     [0, 0, 1, 2, 2, 1, 0]
# ]
# Starts off all zeroes.

# pieces_per_column is a 1d list to keep track of how many pieces are currently in each column.
# Used to determine the row into which a new piece should be placed and to determine when
# a column is full.
pieces_per_column = [0] * COLS
# eg  [0, 0, 1, 3, 3, 1, 0] corresponding to the example grid above.

last_col_clicked = -1   # The number of the column just clicked on (-1 means no column yet)
player = 1 # Toggles between 1 and 2

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()