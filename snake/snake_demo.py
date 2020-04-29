from pyglet import window
from pyglet import app
from pyglet import image
from pyglet.window import key
from pyglet import clock
from pyglet import text
from pyglet import media
from pyglet import resource
from itertools import cycle
from random import randint

window = window.Window(500, 500)

@window.event
def on_key_press(symbol, modifiers):
    global snk_dx, snk_dy
    if not game_over:
        if symbol == key.LEFT and snk_dx == 0:
            snk_dx = -cell_size
            snk_dy = 0
        if symbol == key.RIGHT and snk_dx == 0:
            snk_dx = cell_size
            snk_dy = 0
        if symbol == key.UP and snk_dy == 0:
            snk_dy = cell_size
            snk_dx = 0
        if symbol == key.DOWN and snk_dy == 0:
            snk_dy = -cell_size
            snk_dx = 0
    else:
        if symbol == key.SPACE:
            new_game()


def update(dt):
    global snk_x, snk_y, game_over

    if game_over:
        return

    if game_over_condition():
        game_over = True
        crash.play()
        return

    tail.append( (snk_x, snk_y) )

    snk_x += snk_dx
    snk_y += snk_dy

    if snk_x == fd_x and snk_y == fd_y:
        eat.play()
        place_food()
        # Don't remove the last coordinate from the tail
    else:
        tail.pop(0)
    # print(tail)


@window.event
def on_draw():
    window.clear()
    # Draw the food
    draw_square(fd_x, fd_y, cell_size, colour=(255, 0, 0, 0))
    # Draw the tail
    for coords in tail:
        draw_square(coords[0], coords[1], cell_size, colour=(127, 127, 127, 0))

    # Draw the snake's head
    draw_square(snk_x, snk_y, cell_size)

    if game_over:
        draw_game_over()

def draw_square(x, y, size, colour=(255, 255, 255, 0)):
    img = image.create(size, size, image.SolidColorImagePattern(colour))
    img.blit(x, y)

def place_food():
    global fd_x, fd_y
    fd_x = randint(0, (window.width // cell_size) - 1) * cell_size
    fd_y = randint(0, (window.height // cell_size) - 1) * cell_size

def game_over_condition():
    condition1 = snk_x + snk_dx < 0 or snk_x + snk_dx > window.width - cell_size or snk_y + snk_dy < 0 or snk_y + snk_dy > window.height - cell_size 
    condition2 = (snk_x, snk_y) in tail
    return condition1 or condition2

def draw_game_over():
    game_over_screen = text.Label(f'Score: {len(tail)}\n(Press space to restart)', font_size=24, x=window.width//2, y=window.height//2,
        multiline=True, width=window.width, align='center', anchor_x='center', anchor_y='center')
    game_over_screen.draw()

def new_game():
    global snk_x, snk_y, snk_dx, snk_dy, tail, game_over
    snk_x, snk_y = window.width // cell_size // 2 * cell_size, window.height // cell_size // 2 * cell_size
    snk_dx, snk_dy = 0, 0
    tail = []
    game_over = False
    place_food()
    
# Global stuff
eat = resource.media('resources/eat_eff.wav', streaming=False)
crash = resource.media('resources/crash_eff.wav', streaming=False)
bgm1 = resource.media('resources/bgm1.wav')
bgm2 = resource.media('resources/bgm2.wav')
bgm3 = resource.media('resources/bgm3.wav')
bgm4 = resource.media('resources/bgm4.wav')
bgm5 = resource.media('resources/bgm5.wav')
playlist = cycle([bgm1, bgm2, bgm3, bgm4, bgm5])

player = media.Player()
player.queue(playlist)
player.play()

cell_size = 20
snk_x, snk_y = window.width // cell_size // 2 * cell_size, window.height // cell_size // 2 * cell_size
snk_dx, snk_dy = 0, 0
fd_x, fd_y = 0, 0
game_over = False
place_food()
tail = []

clock.schedule_interval(update, 1/15)

app.run()