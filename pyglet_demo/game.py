from pyglet import app
from pyglet import resource
from pyglet import sprite
from pyglet import clock
from pyglet.window import key
from pyglet.window import Window

window = Window(500, 500)

@window.event
def on_draw():
    window.clear()
    player_sprite.draw()

@window.event
def on_key_press(symbol, modifiers):
    global plyr_dx, plyr_dy
    if symbol == key.LEFT:
        plyr_dx = -plyr_speed
        plyr_dy = 0
    elif symbol == key.RIGHT:
        plyr_dx = plyr_speed
        plyr_dy = 0
    if symbol == key.UP:
        plyr_dx = 0
        plyr_dy = plyr_speed
    elif symbol == key.DOWN:
        plyr_dx = 0
        plyr_dy = -plyr_speed

@window.event
def on_key_release(symbol, modifiers):
    global plyr_dx, plyr_dy
    if symbol == key.LEFT:
        plyr_dx = 0
    elif symbol == key.RIGHT:
        plyr_dx = 0
    elif symbol == key.UP:
        plyr_dy = 0
    elif symbol == key.DOWN:
        plyr_dy = 0

def update(dt):
    player_sprite.x += plyr_dx * dt
    player_sprite.y += plyr_dy * dt

resource.path = ['resources']
resource.reindex()

player_img = resource.image('player.png')
player_sprite = sprite.Sprite(img=player_img, x=window.width/2, y=window.height/2)

plyr_speed = 100
plyr_dx = 0
plyr_dy = 0

clock.schedule_interval(update, 1/120)

app.run()




