#Import modules
import pyglet 
import math
import random

#Game files 
import Objects
import Functions
import Resources
import Sprites

###
#Game Window
window = pyglet.window.Window(800,600)
###



#Labels
score_label = pyglet.text.Label(text="Score: " + str(Objects.player_ship.points),x=25,y=550,batch=Resources.label_batch)
lives_label = Functions.player_lives(Objects.player_ship.lives,batch=Resources.label_batch)


#list of game objects on screen
game_objects = [Objects.player_ship] + Sprites.Aliens + Sprites.Barriers 
 

def update(dt):
    
    #Checks each object active to see if collision kills
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

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

    #Score update
    score_label.text="Score: " + str(Objects.player_ship.points)
    


@window.event
def on_draw():
    window.clear()
    Resources.main_batch.draw()
    Resources.effects_batch.draw()  
    Resources.label_batch.draw()
    window.push_handlers(Objects.player_ship.key_handler)


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()