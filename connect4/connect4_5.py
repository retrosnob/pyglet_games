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
P1_COLOR = (255, 0, 0, 0)
P2_COLOR = (0, 0, 255, 0)
TURN_BAR_HEIGHT = 10 # Don't change much.

WIN_WIDTH = COLS * COL_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

window = Window(WIN_WIDTH, WIN_HEIGHT + TURN_BAR_HEIGHT)
  
@window.event
def on_mouse_press(x, y, button, modifiers):
    global last_col_clicked
    # The last_col_clicked will be -1 if update has run since the last mouse click so we can use
    # it to determine that the last mouse click has been processed. If this function runs and 
    # last_col_clicked is not -1, then we ignore the click event because the last one hasn't been
    # processed yet.
    if button == mouse.LEFT and last_col_clicked == -1 and not game_over:
        last_col_clicked = column(x) # Set last_col_clicked to the column the user clicked on.
        # print(f'The left mouse button was pressed at {x}, {y}, which is {last_col_clicked}')

def update(dt):
    global last_col_clicked, player, game_over, winning_line
    if game_over:
        return    
    # The last_col_clicked is -1 if nothing has been clicked since the last update.
    if last_col_clicked != -1:
        # If pieces_per_column >= ROWS then the column is full, so check for that first.
        if pieces_per_column[last_col_clicked] < ROWS:
            print(f'Player {player} placed a piece in column {last_col_clicked}.')
            # Put the current player (1 or 2) at the correct point in the grid.
            grid[pieces_per_column[last_col_clicked]][last_col_clicked] = player
            # Update the number of pieces in the selected column.
            pieces_per_column[last_col_clicked] += 1
            # Check to see if a winning line exists. If not winning_line will be of length 0.
            winning_line = get_winning_line()
            if len(winning_line) == 4:
                game_over = True
                print(f'Winning line: {winning_line}')
                print(f'Player {player} has won.')        # Make sure we notify the mouse event code that the current click has been processed.
            # Toggle player
            player = 2 if player == 1 else 1
        last_col_clicked = -1

@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw everything.
    draw_grid()
    draw_pieces()
    draw_turn_bar()
    draw_winning_line()

def draw_pieces():
    """Draw the pieces"""
    # Loop through the grid and draw pieces where 1 or 2 is found.
    for y, row in enumerate(grid):
        for x, player_piece in enumerate(row):
            if player_piece == 1:
                draw_piece(x, y, P1_COLOR)
            elif player_piece == 2:
                draw_piece(x, y, P2_COLOR)

def draw_grid():
    for i in range(ROWS):
        draw_line(0, i*ROW_HEIGHT, WIN_WIDTH, i*ROW_HEIGHT)
    for i in range(COLS):
        draw_line(i*COL_WIDTH, 0, i*COL_WIDTH, WIN_HEIGHT)

def draw_turn_bar():
    # This just draws a thin bar at the top of the grid to show whose turn it is.
    if player == 1:
        color = P1_COLOR
    elif player == 2:
        color = P2_COLOR
    graphics.draw(
        4, gl.GL_POLYGON,
        ('v2i', (0, WIN_HEIGHT + TURN_BAR_HEIGHT, WIN_WIDTH, WIN_HEIGHT + TURN_BAR_HEIGHT, WIN_WIDTH, WIN_HEIGHT, 0, WIN_HEIGHT)),
        ('c4B', color  * 4)
    )

def draw_winning_line():
    """Highlight the pieces in the winning line"""
    if len(winning_line) == 4:
        # Highlight each piece in the winning line with a small polygon (here a circle).
        for coords in winning_line:
            draw_reg_polygon(coords[0]  * COL_WIDTH + COL_WIDTH//2, coords[1]  * COL_WIDTH + COL_WIDTH//2, PIECE_RADIUS//2, 64, color=(255, 255, 0, 0))

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

def get_winning_line():
    """Return the coords of the winning line, if any"""
    # Test the left four columns only, for horizontals going right.
    for row in range(0, ROWS):
        for col in range(0, 4):
            if all([grid[row][col] == value and value != 0 for value in grid[row][col:col+4]]):
                return (col, row), (col+1, row), (col+2, row), (col+3, row)
    # Test the top three rows only, for verticals going downwards.
    transpose = list(zip(*grid))
    for col in range(0, ROWS):
        for row in range(0, 4):
            if all([transpose[col][row] == value and value != 0 for value in transpose[col][row:row+4]]):
                return (col, row), (col, row+1), (col, row+2), (col, row+3)
    # Test the top-left 3r x 4c only, for diagonals going down-right.
    for row in range(3, ROWS):
        for col in range(0, 4):
            # Break a long condition into several lines by enclosing in parentheses.
            if (grid[row][col] != 0
            and grid[row][col] == grid[row-1][col+1]
            and grid[row][col] == grid[row-2][col+2] 
            and grid[row][col] == grid[row-3][col+3]):
                return (col+3, row-3), (col+2, row-2), (col+1, row-1), (col, row)
    # Test the top-right 3r x 4c only, for diagonals going down-left.
    for row in range(3, ROWS):
        for col in range(3, COLS):
            # Break a long condition into several lines by enclosing in parentheses.
            if (grid[row][col] != 0
            and grid[row][col] == grid[row-1][col-1]
            and grid[row][col] == grid[row-2][col-2]
            and grid[row][col] == grid[row-3][col-3]):
                return (col-3, row-3), (col-2, row-2), (col-1, row-1), (col, row)
    # If we get here then no winning line was found so return an empty tuple.
    return ()

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
game_over = False
winning_line = ()

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()