from pyglet import app
from pyglet.window import Window
from pyglet import image
from pyglet import clock
from pyglet.window import key
from random import randint

# Create the window.
window = Window(500, 500)

# This is a built-in function that Pyglet calls when the window appears and when it is updated.
@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw the food.
    draw_square(fd_x, fd_y, cell_size, colour = (255, 0, 0, 0))
    # Draw a square for each coordinate in the tail.
    for coords in tail:
        draw_square(coords[0], coords[1], cell_size, colour = (127, 127, 127, 0))
    # Draw the snake's head.
    draw_square(snk_x, snk_y, cell_size)

# This is a function I wrote just to simplify drawing snake segments.
def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    # Create the image of the square.
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    # Draws the image on the canvas. x, y is the top-corner of the image.
    img.blit(x, y)

def place_food():
    global fd_x, fd_y
    # Set random coordinates for the food, ensuring that it doesn't land between cells.
    fd_x = randint(0, (window.width // cell_size) - 1) * cell_size
    fd_y = randint(0, (window.height // cell_size) - 1) * cell_size

@window.event
def on_key_press(symbol, modifiers):
    # Standard up, down, left, right.

    # The global keyword means 'use the variables that are defined at the module
    # level, instead of declaring a new variable local to this function. It is required
    # when you want to assign inside a function to a variable that has been defined
    # outside the function. If you just reference the variable that has been defined outside
    # the function, without assigning to it, then you use the global definition automatically.
    global snk_dx, snk_dy

    # Note how the snake only moves in steps equal to the segment size.
    if symbol == key.LEFT:
        if snk_dx == 0:
            snk_dx = -cell_size      # Left is the negative x direction.
            snk_dy = 0              # Stop moving up/down.
    elif symbol == key.RIGHT:
        if snk_dx == 0:
            snk_dx = cell_size       # Right is the positive x direction.
            snk_dy = 0              # Stop moving up/down.
    elif symbol == key.UP:
        if snk_dy == 0:
            snk_dx = 0              # Up is the positive y direction.
            snk_dy = cell_size       # Stop moving left/right.
    elif symbol == key.DOWN:
        if snk_dy == 0:
            snk_dx = 0              # Down is the negative y direction.
            snk_dy = -cell_size      # Stop moving left/right.

# This function is scheduled to run a certain number of times per second.
def update(dt):
    global snk_x, snk_y, fd_x, fd_y

    # Add a new tail square behind us
    tail.append((snk_x, snk_y))
    # Update the position of the snake's head.
    snk_x += snk_dx
    snk_y += snk_dy

    # Check for collision with food.
    if snk_x == fd_x and snk_y == fd_y:
        place_food()
    else:
        # Remove the new tail square because we didn't eat food.
        tail.pop(0)
    print(tail)

# Not the length of the snake, but the width and height of a single snake segment.
cell_size = 20 

# The amount by which the snake's x and y coordinates change.
snk_dx, snk_dy = 0, 0 
# Start the snake in the middle, ensuring that it doesn't land between cells.
snk_x = window.width // cell_size // 2 * cell_size
snk_y = window.height // cell_size // 2 * cell_size
# Define the coordinates of the food.
fd_x, fd_y = 0, 0
# Immediately place the new food somewhere.
place_food()
# Define the list of coordinates in the snake's tail.
tail = []

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()