import pyglet

from pyglet import app
from pyglet import clock
from pyglet.window import Window
from pyglet.window import mouse
from pyglet import image
from pyglet import text
from pyglet import sprite

window = Window(700, 600)

def setup():
    print('Setting up...')
    
@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print(f'The left mouse button was pressed at {x}, {y}')

def update(dt):
    pass

@window.event
def on_draw():
    # Erase everything.
    window.clear()
    draw_grid()
    
def draw_grid():
    draw_square(0, 0, 100)
    pass

def draw_square(x, y, size, colour = (255, 255, 255, 0)):
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    img.blit(x, y)

def game_over_condition():
    pass 


grid = []

setup()

# Set how often the update function is called.
clock.schedule_interval(update, 1/15)

# Start the game.
app.run()