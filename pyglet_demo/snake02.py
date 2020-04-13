from pyglet import app
from pyglet import gl
from pyglet import clock
from pyglet.window import Window
from pyglet.window import key
from pyglet import graphics
from random import randint
import sys

window = Window(500, 500)

@window.event
def on_draw():
    global snk_x, snk_y, snk_size, fd_x, fd_y, tail
    if not game_over:
        # Erase everything.
        window.clear()
        # Draw the snake's head.
        draw_square(snk_x, snk_y, snk_size)
        # Draw the food.
        draw_square(fd_x, fd_y, snk_size, colour = (255, 0, 0, 0))
        # Draw a square for each coordinate in the tail.
        for coords in tail:
            draw_square(coords[0], coords[1], snk_size)
    
def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    # This has confusing syntax. To draw a square we need to give the coordinates
    # of the vertices of a 4 sided polygon, where (x, y) is the top-left corner.
    # The default square colour is white, as given in the parameter list, but
    # this can be overrided, as when we draw food.
    graphics.draw(4, gl.GL_POLYGON, (
        'v2i', (
            x, y,
            x + size, y,
            x + size, y + size,
            x, y + size)
        ),
    ('c4B', colour * 4)              
    )
    

@window.event
def on_key_press(symbol, modifiers):
    # Standard up, down, left, right.
    # The global keyword means 'use the variables that are defined at the module
    # level, instead of declaring a new variable local to this function.
    global snk_dx, snk_dy, app
    if symbol == key.LEFT:
        snk_dx = -snk_size
        snk_dy = 0
    elif symbol == key.RIGHT:
        snk_dx = snk_size
        snk_dy = 0
    elif symbol == key.UP:
        snk_dx = 0
        snk_dy = snk_size
    elif symbol == key.DOWN:
        snk_dx = 0
        snk_dy = -snk_size

def update(dt):
    global snk_x, snk_y, snk_dx, snk_dy, snk_size, new_food, fd_x, fd_y, tail, app, game_over, window

    # Check for collision with edge.
    if snk_x + snk_dx < 0 or snk_x + snk_dx > window.width - snk_size or snk_y + snk_dy < 0 or snk_y + snk_dy > window.height - snk_size:
        game_over = True
        app.exit()
        window.close()
        return

    # Add a new tail square behind us
    tail.append((snk_x, snk_y))
    # Update the position of the snake's head.
    snk_x += snk_dx
    snk_y += snk_dy
    # Check for collision with food.
    if snk_x == fd_x and snk_y == fd_y:
        print('Yum')
        new_food = True
        # Don't remove the new tail square because we ate food.
    else:
        # Remove the new tail square because we didn't eat food.
        tail.pop(0)
    if new_food:
        # Move the food to a new random location.
        print(f'New food at {fd_x} {fd_y}')
        # Create new food in a random place, ensuring that it doesn't land between cells.
        fd_x = randint(0, (window.width // snk_size) - 1) * snk_size
        fd_y = randint(0, (window.height // snk_size) - 1) * snk_size
        new_food = False

fd_x, fd_y = 0, 0 # The location of the food.
tail = [] # A list of coordinates for the snake's tail.
snk_size = 20 # Not the length of the snake, but the width and height of a single snake segment.
snk_dx, snk_dy = 0, 0 # The amount by which the snake's x and y coordinates change.

# Start the snake in the middle, ensuring that it doesn't land between cells.
snk_x = window.width // snk_size // 2 * snk_size
snk_y = window.height // snk_size // 2 * snk_size

new_food = True # Draw a new food the first time round.

if snk_size < 1 or window.width % snk_size != 0 or window.height % snk_size != 0:
    print('Error: Snake size must be greater than 0 and must divide the window width and the window height exactly.')
    exit()
    
game_over = False

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()