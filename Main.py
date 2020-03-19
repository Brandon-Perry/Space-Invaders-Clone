#Import modules
import pyglet 
import math
import random

#Game files
import Objects
import Functions
import Resources

###
#Game Window
window = pyglet.window.Window(800,600)
###

#Loads Sprites
player_ship = Objects.Player(x=100,y=100, batch=Resources.main_batch)
player_ship.x = 400
player_ship.y = 50





#list of game objects on screen
game_objects = [player_ship]


def update(dt):
    
    #Updates objects and adds objects to game
    to_add = []

    for obj in game_objects:
        obj.update(dt)
        game_objects.extend(obj.new_objects)
        obj.new_objects = []

    for to_remove in [obj for obj in game_objects if obj.dead]:
        to_remove.delete()
        game_objects.remove(to_remove)

    game_objects.extend(to_add)


@window.event
def on_draw():
    window.clear()
    Resources.main_batch.draw()
    window.push_handlers(player_ship.key_handler)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()