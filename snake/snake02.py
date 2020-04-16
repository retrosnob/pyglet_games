from pyglet import app
from pyglet.window import Window
from pyglet import image
from pyglet import clock
from pyglet.window import key

# Create the window.
window = Window(500, 500)

# This is a built-in function that Pyglet calls when the window appears and when it is updated.
@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw the snake's head.
    draw_square(snk_x, snk_y, cell_size)

# This is a function I wrote just to simplify drawing snake segments.
def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    # Creates the image.
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    # Draws the image on the canvas. x, y is the top-corner of the image.
    img.blit(x, y)

@window.event
def on_key_press(symbol, modifiers):
    # Standard up, down, left, right.

    # The global keyword means 'use the variables that are defined at the module level
    # level, instead of declaring a new variable local to this function'. If we didn't
    # use this then we would create new, local versions of the variables.
    global snk_dx, snk_dy

    # Note how the snake only moves in steps equal to the segment size.
    if symbol == key.LEFT:
        snk_dx = -cell_size      # Left is the negative x direction.
        snk_dy = 0              # Stop moving up/down.
    elif symbol == key.RIGHT:
        snk_dx = cell_size       # Right is the positive x direction.
        snk_dy = 0              # Stop moving up/down.
    elif symbol == key.UP:
        snk_dx = 0              # Up is the positive y direction.
        snk_dy = cell_size       # Stop moving left/right.
    elif symbol == key.DOWN:
        snk_dx = 0              # Down is the negative y direction.
        snk_dy = -cell_size      # Stop moving left/right.

# This function is scheduled to run a certain number of times per second.
def update(dt):
    global snk_x, snk_y
    # Update the position of the snake's head.
    snk_x += snk_dx
    snk_y += snk_dy

# Not the length of the snake, but the width and height of a single snake segment.
cell_size = 20 

# The amount by which the snake's x and y coordinates change.
snk_dx, snk_dy = 0, 0 

# Start the snake in the middle, ensuring that it doesn't land between cells.
snk_x = window.width // cell_size // 2 * cell_size
snk_y = window.height // cell_size // 2 * cell_size

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()