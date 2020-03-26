import pyglet
import Functions
import Objects
import Resources

#Player sprite located in Objects file due to importing errors

#Alien Sprites
Aliens = Functions.aliens_on_screen(3,batch=Resources.main_batch)

#Barriers
Barriers = Functions.generate_barriers(4,batch=Resources.main_batch)