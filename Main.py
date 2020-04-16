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
window.push_handlers(Objects.global_key_handler)
###

#Labels
Objects.score_label
Objects.level_label


#list of game objects on screen
Objects.game_obj.game_objects = [Objects.player_ship] #+ Sprites.Aliens + Sprites.Barriers 




def update(dt):
    
    if Objects.title_obj.dead == True:

        Objects.game_obj.update(dt)

               
        #Check to send mothership
        Functions.send_mothership(Objects.game_obj.game_objects,batch=Resources.main_batch)


        #Checks for next level
        Functions.next_level()

        Functions.collision_check(Objects.game_obj.game_objects)

        Functions.update_and_add_game_objects(Objects.game_obj.game_objects,dt)
        
        #Score update
        Objects.score_label.text="Score: " + str(Objects.player_ship.points)

        #Level update
        if Objects.game_obj.boss_battle == True:
            Objects.level_label.text='Level Boss Battle'
        else:
            Objects.level_label.text='Level ' + str(Objects.game_obj.level)


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
