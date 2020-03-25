#Import modules
import pyglet 
import math
import random

#Game files 
import Objects
import Functions
import Resources
import Sprites
import Screens

###
#Game Window
window = pyglet.window.Window(800,600)
###


#Labels
score_label = pyglet.text.Label(text="Score: " + str(Objects.player_ship.points),x=25,y=550,batch=Resources.label_batch)


#list of game objects on screen
game_objects = [Objects.player_ship] + Sprites.Aliens + Sprites.Barriers 




def update(dt):
    
    Functions.collision_check(game_objects)

    Functions.update_and_add_game_objects(game_objects,dt)

    Functions.update_titles(dt)

    #Score update
    score_label.text="Score: " + str(Objects.player_ship.points)
      



@window.event
def on_draw():
    end_game = Functions.check_endgame(Objects.player_ship)
    
    if Objects.title_obj.dead == False:
        Screens.title_screen(window,game_objects)
    else:
        if end_game == False:
            Screens.game_screen(window)
            
        elif end_game == True:
            Screens.end_screen(window,game_objects)
        
        
            

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()