import pyglet
from pyglet.window import key
import math

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
        self.gravity = 2.81

        #Is object alive?
        self.dead = False

        #Objects to be added to game
        self.new_objects = []

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
        self.drag = .5
        
        #Ship handling
        self.key_handler = key.KeyStateHandler()

        #Bullet 
        self.bullet_speed = 900.0
        self.fireonce = True

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
            self.velocity_y -= (self.gravity)

        #Fire
        if self.key_handler[key.SPACE]:
            if self.fireonce is True:
                self.fire()
                self.fireonce = False
        if not self.key_handler[key.SPACE]:
            self.fireonce = True

        #Bounds rotation and returns to normal when not accelerating - also features drag to slow the ship down
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

            #Implements drag
            if self.velocity_x > 0:
                self.velocity_x -= self.drag
            elif self.velocity_x < 0:
                self.velocity_x += self.drag        

    def fire(self):
        angle_radians = -math.radians(self.rotation + 270)
        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = Player_Bullet(x=bullet_x,y=bullet_y,batch=self.batch)

        bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
        bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        new_bullet.rotation = self.rotation

        self.new_objects.append(new_bullet)


class Player_Bullet(PhyiscalObject):
    def __init__(self,*args,**kwargs):
        super(Player_Bullet,self).__init__(img=Resources.bullet_image,*args,**kwargs)
        pyglet.clock.schedule_interval(self.check_bounds_bullet,.1)

        self.is_bullet = True

    def die(self):
        self.dead = True

    def check_bounds_bullet(self,dt):
        min_x = 40
        min_y = 40
        max_x = 760
        max_y = 560
        if self.x <= min_x:
            self.die()
        elif self.x >= max_x:
            self.die()
        if self.y <= min_y:
            self.die()
        elif self.y >= max_y:
            self.die()

    

    





