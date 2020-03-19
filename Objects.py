import pyglet
from pyglet.window import key

#import game files
import Resources


#GENERAL PHYSICAL OBJECTS
class PhyiscalObject(pyglet.sprite.Sprite):
    
    def __init__(self, x=0.0, y=0.0, *args,**kwargs):
        super().__init__(*args,**kwargs)
        
        #Location of object on screen
        self.x = x
        self.y = y

        #Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0

        #Gravity
        self.gravity = -2.81

        #Is object alive?
        self.alive = True

    def update(self,dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        min_x = self.image.width / 2
        min_y = self.image.height / 2
        max_x = 800 - self.image.width / 2
        max_y = 600 - self.image.height / 2
        if self.x <= min_x:
            self.x = min_x
            self.velocity_x = 0
        elif self.x >= max_x:
            self.x = max_x
            self.velocity_x = 0
        if self.y <= min_y:
            self.y = min_y
            self.velocity_y = 0
        elif self.y >= max_y:
            self.y = max_y
            self.velocity_y = 0



class Player(PhyiscalObject):
    def __init__(self,x=400.0,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.player_image,*args,**kwargs)

        #Ship physics
        self.thrust = 100.0
        self.mass = 1.0
        self.rotate_speed = 50.0
        self.rotation = 0
        
        #Ship handling
        self.key_handler = key.KeyStateHandler()

    def update(self,dt):

        super(Player,self).update(dt)

        #Movement left and right - ship must be facing direction of yaw to begin accelerating or deaccelerating 
        if self.key_handler[key.LEFT]:
            if self.rotation < 0:
                self.velocity_x -= self.thrust * dt
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]:
            if self.rotation > 0:
                self.velocity_x += self.thrust * dt
            self.rotation += self.rotate_speed * dt

        #Movement up and down
        if self.key_handler[key.UP]:
            self.velocity_y += self.thrust * dt
        if self.key_handler[key.UP] is False:
            self.velocity_y -= (self.gravity*self.gravity)

        #Bounds rotation and returns to normal when not accelerating 
        normal_rotation = 0
        min_rotation = -30
        max_rotation = 30

        if self.rotation >= max_rotation:
            self.rotation = max_rotation
        if self.rotation <= min_rotation:
            self.rotation = min_rotation

        if not self.key_handler[key.RIGHT] and not self.key_handler[key.LEFT]:
            if self.rotation is not normal_rotation:
                if self.rotation > normal_rotation:
                    self.rotation -= self.rotate_speed * dt
                elif self.rotation < normal_rotation:
                    self.rotation += self.rotate_speed * dt

                





