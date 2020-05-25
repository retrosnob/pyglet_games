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

PIECE_RADIUS = ROW_HEIGHT * 0.4
P1_COLOR = (255, 0, 0, 0)
P2_COLOR = (0, 0, 255, 0)


window = Window(WIN_WIDTH, WIN_HEIGHT)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global last_col_clicked
    if button == mouse.LEFT and last_col_clicked == -1 and not game_over:
        print(f'The mouse was clicked at {x}, {y}, which is column {column(x)}.')
        last_col_clicked = column(x)


def update(dt):
    global last_col_clicked, player, winning_line, game_over, grid
    if game_over == True:
        return
    if last_col_clicked != -1:
        if pieces_per_column[last_col_clicked] < ROWS:
            print(f'Player {player} clicked on column {last_col_clicked}.')
            # Update the game grid
            grid[pieces_per_column[last_col_clicked]][last_col_clicked] = player
            # Update the number of pieces per column
            pieces_per_column[last_col_clicked] += 1

            # Check to see if someone's won
            winning_line = get_winning_line()
            if len(winning_line) == 4:
                # Game is over
                game_over = True
                print(f'Winning line: {winning_line}')
                print(f'Player {player} has won.')

            player = 2 if player == 1 else 1
            print(grid)
            print(pieces_per_column)
        last_col_clicked = -1

@window.event
def on_draw():
    # erase everything
    window.clear()
    # draw everything
    draw_grid()
    draw_pieces()
    draw_winning_line()

def column(x):
    return x // COL_WIDTH

def draw_grid():
    # Draw horizontal lines
    for i in range(ROWS):
        draw_line(0, i * ROW_HEIGHT, WIN_WIDTH, i * ROW_HEIGHT)
    # Draw vertical lines
    for i in range(COLS):
        draw_line(i * COL_WIDTH, 0, i * COL_WIDTH, WIN_HEIGHT)

def draw_line(x1, y1, x2, y2, color=(255, 255, 255, 0)):
    graphics.draw(
        2, gl.GL_LINES, ('v2i', (x1, y1, x2, y2)), ('c4B', (color * 2))
    )

def draw_pieces():
    # loop through the grid and draw each piece
    for y, row in enumerate(grid):
        for x, player_piece in enumerate(row):
            # draw...
            if player_piece == 1:
                draw_piece(x, y, P1_COLOR)
            elif player_piece == 2:
                draw_piece(x, y, P2_COLOR)

def draw_piece(x, y, color=(255, 255, 255, 0)):
    draw_reg_polygon(x * COL_WIDTH + COL_WIDTH // 2, y * ROW_HEIGHT + ROW_HEIGHT // 2, PIECE_RADIUS, 64, color)

def draw_reg_polygon(x, y, r, n, color=(255, 255, 255, 0)):
    vertices = []
    th = 0
    for _ in range(n):
        vertices += [x + r*cos(th), y + r*sin(th)]
        th += 2*pi/n

    graphics.draw(
        n, gl.GL_POLYGON, 
        ('v2f', vertices),
        ('c4B', color * n)
    )

def draw_winning_line():
    if len(winning_line) == 4:
        for coords in winning_line:
            draw_reg_polygon(coords[0] * COL_WIDTH + COL_WIDTH // 2, coords[1] * ROW_HEIGHT + ROW_HEIGHT // 2, PIECE_RADIUS//2, 64, (255, 255, 255, 0))

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

pieces_per_column = [0] * COLS
last_col_clicked = -1
player = 1
game_over = False
winning_line = ()

clock.schedule_interval(update, 1/15)

app.run()