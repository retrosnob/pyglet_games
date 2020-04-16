from pyglet import app
from pyglet.window import Window
from pyglet import resource
from pyglet import sprite

window = Window(500, 500)

@window.event
def on_draw():
    window.clear()
    player_sprite.draw()


resource.path = ['resources']
resource.reindex()

player_img = resource.image('player.png')
player_sprite = sprite.Sprite(img=player_img, x=window.width/2, y=window.height/2)
app.run()


window = Window(500, 500)
app.run()



