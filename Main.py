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
game_level = 1

#global game_objects
game_objects = Functions.start_game(window)



#Labels
score_label = pyglet.text.Label(text="Score: " + str(Objects.player_ship.points),x=25,y=550,batch=Resources.label_batch)
level_label = pyglet.text.Label(text="Level " + str(game_level),x=window.height/2,y=550,batch=Resources.label_batch) 


def update(dt):
    
    if Objects.title_obj.dead == True:
        game_objects = Functions.start_game(window)

        Functions.collision_check(game_objects)

        Functions.update_and_add_game_objects(game_objects,dt)
        #Score update
        score_label.text="Score: " + str(Objects.player_ship.points)

    
    elif Functions.check_endgame(Objects.player_ship) == True:
        Objects.end_obj.update(dt)
    
    else:

        Objects.title_obj.update(dt)

    if Objects.end_obj.restart == True:
        game_objects = Functions.start_game(window)
        Objects.end_obj.restart = None
        
    elif Objects.end_obj.restart == False:
        window.close()

    
    

@window.event
def on_draw():
    end_game = Functions.check_endgame(Objects.player_ship)
    
    if Objects.title_obj.dead == False:
        Screens.title_screen(window,game_objects)
    else:
        if end_game == False:
            #Screens.game_screen(window)
            pass
            
        elif end_game == True:
            #Screens.end_screen(window,game_objects)
            pass
            
        
        
            

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()