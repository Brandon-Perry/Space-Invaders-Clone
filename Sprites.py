import pyglet
import Functions
import Objects
import Resources

#Player sprite located in Objects file due to importing errors


#Barriers
#Barriers = Functions.generate_barriers(4,batch=Resources.main_batch)

Background = Objects.Background(x=400,y=400,batch=Resources.background_batch)
Background.scale = 2
Background.rotation = 270