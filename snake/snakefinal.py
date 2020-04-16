from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import key
from pyglet import graphics
from pyglet import image
from pyglet import text
from random import randint

window = Window(500, 500)

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
    # Draw the game over message if the game is over.
    if game_over:
        draw_game_over()
    

def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    img.blit(x, y)
    
def draw_game_over():
    game_over_screen = text.Label(f'Score: {len(tail)}', font_size=24,
                    x=window.width//2, y=window.height//2,
                    anchor_x='center', anchor_y='center')
    game_over_screen.draw()

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
    if not game_over:
        if symbol == key.LEFT:
            if snk_dx == 0:
                snk_dx = -cell_size
                snk_dy = 0
        elif symbol == key.RIGHT:
            if snk_dx == 0:
                snk_dx = cell_size
                snk_dy = 0
        elif symbol == key.UP:
            if snk_dy == 0:
                snk_dx = 0
                snk_dy = cell_size
        elif symbol == key.DOWN:
            if snk_dy == 0:
                snk_dx = 0
                snk_dy = -cell_size

def game_over_condition():
    # Collision with edge.
    condition1 = snk_x + snk_dx < 0 or snk_x + snk_dx > window.width - cell_size or snk_y + snk_dy < 0 or snk_y + snk_dy > window.height - cell_size
    # Collision with self.
    condition2 = (snk_x, snk_y) in tail
    return condition1 or condition2

def update(dt):
    global snk_x, snk_y, new_food, fd_x, fd_y, game_over

    # Check for game over conditions
    if game_over_condition():
        game_over = True

    if game_over:
        return

    # Add a new tail square behind us
    tail.append((snk_x, snk_y))
    # Update the position of the snake's head.
    snk_x += snk_dx
    snk_y += snk_dy

    # Check for collision with food.
    if snk_x == fd_x and snk_y == fd_y:
        place_food()
        # Don't remove the new tail square because we ate food.
    else:
        # Remove the new tail square because we didn't eat food.
        tail.pop(0)

fd_x, fd_y = 0, 0 # The location of the food.
tail = [] # A list of coordinates for the snake's tail.
cell_size = 20 # Not the length of the snake, but the width and height of a single snake segment.
snk_dx, snk_dy = 0, 0 # The amount by which the snake's x and y coordinates change.

# Start the snake in the middle, ensuring that it doesn't land between cells.
snk_x = window.width // cell_size // 2 * cell_size
snk_y = window.height // cell_size // 2 * cell_size

# Immediately place the new food somewhere.
place_food()


if cell_size < 1 or window.width % cell_size != 0 or window.height % cell_size != 0:
    print('Error: Snake size must be greater than 0 and must divide the window width and the window height exactly.')
    exit()
    
game_over = False

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()