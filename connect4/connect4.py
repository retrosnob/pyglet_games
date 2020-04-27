from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet.window import key
from pyglet import graphics
from pyglet import gl
from pyglet import text
from math import sin, cos, pi

# TODO: Computer player

COLS = 7 # Don't change.
ROWS = 6 # Don't change.
COL_WIDTH = ROW_HEIGHT = 100 # Change board size by adjusting this. 
PIECE_RADIUS = COL_WIDTH * 0.3 # Change piece size by adjusting multiplier in range: 0 < multiplier = 0.5.
PIECE_SIDES = 64 # Change from 3 (triangle) to largish (~64) for a circle.
P1_COLOR = (255, 0, 0, 0) # Change P1's piece color.
P2_COLOR = (0, 0, 255, 0) # Change P2's piece color.
GRID_COLOR = (63, 63, 63, 0) # Change the color of the grid lines.
TURN_BAR_HEIGHT = 10 # Don't change much.

WIN_WIDTH = COLS * COL_WIDTH
WIN_HEIGHT = ROWS * ROW_HEIGHT

window = Window(WIN_WIDTH, WIN_HEIGHT + TURN_BAR_HEIGHT)

def new_game():
    # Resets the global state variables ready for a new game. These variables are explained at the module level.
    global grid, pieces_per_column, player, last_col_clicked, game_over, winning_line
    grid = [[0] * COLS for i in range(ROWS)]
    pieces_per_column = [0] * COLS
    player = 1
    last_col_clicked = -1
    game_over = False
    winning_line = ()
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    global last_col_clicked
    # The last_col_clicked will be -1 if update has run since the last mouse click so we can use
    # it to determine that the last mouse click has been processed. If this function runs and 
    # last_col_clicked is not -1, then we ignore the click event because the last one hasn't been
    # processed yet.
    if button == mouse.LEFT and last_col_clicked == -1 and not game_over:
        last_col_clicked = column(x) if last_col_clicked == -1 else -1 # Set last_col_clicked to the column the user clicked on.
        # print(f'The left mouse button was pressed at {x}, {y}, which is {last_col_clicked}')

@window.event
def on_key_press(symbol, modifiers):
    # Restart game.
    if game_over and symbol == key.SPACE:
        new_game()

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
                print(f'Player {player} has won.')
            player = 2 if player == 1 else 1
        # Make sure we notify the mouse event code that the current click has been processed.
        last_col_clicked = -1

@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw everything.
    draw_grid()
    draw_turn_bar()
    draw_pieces()
    draw_winning_line()
    if game_over:
        draw_game_over()

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

def draw_pieces():
    """Draw the pieces"""
    # Loop through the grid and draw pieces where 1 or 2 is found.
    for y, row in enumerate(grid):
        for x, player_piece in enumerate(row):
            if player_piece == 1:
                draw_piece(x, y, PIECE_RADIUS, P1_COLOR)
            elif player_piece == 2:
                draw_piece(x, y, PIECE_RADIUS, P2_COLOR)

def draw_piece(x, y, size, color=(255, 0, 0, 0)):
    """Draws a piece on the board with 0, 0 being the bottom-left and 6, 5 being the top-right)"""
    draw_reg_polygon(x * COL_WIDTH +  COL_WIDTH//2, y * ROW_HEIGHT + ROW_HEIGHT//2, PIECE_RADIUS, PIECE_SIDES, color)

def draw_grid():
    """Draw the grid lines"""
    for i in range(COLS):
        draw_line(i*ROW_HEIGHT, 0, i*ROW_HEIGHT, WIN_HEIGHT, color=GRID_COLOR)
    for i in range(ROWS):
        draw_line(0, i*COL_WIDTH, WIN_WIDTH, i*COL_WIDTH, color=GRID_COLOR)

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    """Draws a line from x1, y1 to x2, y2"""
    # 2 means that 2 vertices will be supplied, the mode is line drawing
    # v2i means (v)ertices, (2) coordinates per vertex ie 2D, each vertex is an (i)nteger
    # c3B means (c)olor, (4) values per vertex ie RGBA, unsigned (B)yte representation
    # there has to be one color per vertex, so in this case 2 lots of 4 values
    graphics.draw(
        2, gl.GL_LINES,
        ('v2i', (x1, y1, x2, y2)),
        ('c4B', color  * 2)
    )

def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    """ Draws a regular n-sided polygon of radius r centred on x, y. Make n ~ 64 for a circle."""
    th = 0
    vertices = []
    for _ in range(n):
        vertices += [x + r*sin(th), y + r*cos(th)]
        th += 2*pi/n
    # 3 means that 2 vertices will be supplied, the mode is polygon drawing.
    # v2i means (v)ertices, (2) coordinates per vertex ie 2D, each vertex is an (i)nteger.
    # c3B means (c)olor, (4) values per vertex ie RGBA, unsigned (B)yte representation.
    # There has to be one color per vertex, so in this case n lots of 4 values.
    graphics.draw(
        n, gl.GL_POLYGON,
        ('v2f', vertices),
        ('c4B', color * n)
    )

def draw_winning_line():
    """Highlight the pieces in the winning line"""
    if len(winning_line) == 4:
        # Highlight each piece in the winning line with a small polygon (here a circle).
        for coords in winning_line:
            draw_reg_polygon(coords[0]  * COL_WIDTH + COL_WIDTH//2, coords[1]  * COL_WIDTH + COL_WIDTH//2, PIECE_RADIUS//2, 64, color=(255, 255, 0, 0))

def draw_game_over():
    """Display game over message"""
    game_over_screen = text.Label(f'Press space to restart', font_size=24,
                    x=window.width//2, y=window.height//2, width=window.width, align='center',
                    anchor_x='center', anchor_y='center', multiline=True)
    game_over_screen.draw()

def column(x):
    """Given the x-coord of a mouse click, return the corresonding column number"""
    return x // COL_WIDTH

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

# The full connect 4 grid. 0 = empty, 1 = P1's piece, 2 = P2's piece.
grid = [[0] * COLS for i in range(ROWS)]
# eg 
# [   [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 0, 0, 0, 0], 
#     [0, 0, 0, 2, 1, 0, 0], 
#     [0, 0, 0, 1, 2, 0, 0], 
#     [0, 0, 1, 2, 2, 1, 0]
# }
# Starts off all zeroes.

# pieces_per_column is a 1d list to keep track of how many pieces are currently in each column.
# Used to determine the row into which a new piece should be placed and to determine when
# a column is full.
pieces_per_column = [0] * COLS

player = 1              # The current player
last_col_clicked = -1   # The number of the column just clicked on (-1 means no column yet)
game_over = False       # A flag used by several functions to know when to stop
winning_line = ()       # The coordinates of the winning line, if any, so that it can be highlighted.    

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()