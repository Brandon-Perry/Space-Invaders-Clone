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
level_label = pyglet.text.Label(text='Level: ' + str(Objects.game_obj.level),x=window.width/2,y=550,batch=Resources.label_batch)


#list of game objects on screen
Objects.game_obj.game_objects = [Objects.player_ship] + Sprites.Aliens + Sprites.Barriers 




def update(dt):
    
    if Objects.title_obj.dead == True:

        #Checks for next level
        Functions.next_level()

        Functions.collision_check(Objects.game_obj.game_objects)

        Functions.update_and_add_game_objects(Objects.game_obj.game_objects,dt)
        
        #Score update
        score_label.text="Score: " + str(Objects.player_ship.points)

        #Level update
        level_label.text='Level ' + str(Objects.game_obj.level)

        Objects.game_obj.update(dt)

        if Functions.check_endgame(Objects.player_ship) == True:
            Objects.end_obj.update(dt)
            if Objects.end_obj.close == True:
                window.close()
                
            if Objects.end_obj.restart == True:
                Functions.restart_game(window,Objects.game_obj.game_objects,Objects.game_obj.level)
        
        
        
    if Objects.title_obj.dead == False:

        Objects.title_obj.update(dt)

    



@window.event
def on_draw():
    end_game = Functions.check_endgame(Objects.player_ship)
    
    if Objects.title_obj.dead == False:
        Screens.title_screen(window,Objects.game_obj.game_objects)
    else:
        if end_game == False:
            Screens.game_screen(window)
            
        elif end_game == True:
            Screens.end_screen(window,Objects.game_obj.game_objects)
            
        
        
            

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()
