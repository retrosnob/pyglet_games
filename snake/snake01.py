from pyglet import app
from pyglet import image
from pyglet.window import Window

# Create the window.
window = Window(500, 500)

# This is a built-in function that Pyglet calls when the window appears and when it is updated.
@window.event
def on_draw():
    # Erase everything.
    window.clear()
    # Draw the snake's head.
    draw_square(snk_x, snk_y, cell_size, colour = (255, 0, 0, 0))    

# This is a function I wrote just to simplify drawing snake segments.
def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    # Creates the image.
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    # Draws the image on the canvas. x, y is the top-corner of the image.
    img.blit(x, y)

# Not the length of the snake, but the width and height of a single snake segment.
cell_size = 20

# Start the snake in the middle, ensuring that it doesn't land between cells.
snk_x = window.width // cell_size // 2 * cell_size
snk_y = window.height // cell_size // 2 * cell_size

# Start the game.
app.run()