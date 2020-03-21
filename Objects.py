import pyglet
from pyglet.window import key
import math
import random

#import game files
import Resources
import Object_Functions

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
        self.gravity = 5

        #Is object alive?
        self.dead = False
        self.destructable = True

        #Objects to be added to game, used for player and alien bullets
        self.new_objects = []

        #How the object react to bullets
        self.reacts_to_bullets = True
        self.reacts_to_alien_bullets = True
        self.is_bullet = False
        self.is_alien_bullet = False

        #Heath of Object
        self.health = 0

    def update(self,dt):
        #Velocity and how it affects movement (dt is frame)
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        #if item reaches the edges of the map, then it stops them from going any further
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

    def collides_with(self,other_object):
        
        #If object reacts to bullets and other object is a bullet, then calculate the distance between the two and return if within collision distance

        if not self.reacts_to_bullets and other_object.is_bullet:
            return False
        if self.is_bullet and not other_object.reacts_to_bullets:
            return False

        if not self.reacts_to_alien_bullets and other_object.is_alien_bullet:
            return False
        if self.is_alien_bullet and not other_object.reacts_to_alien_bullets:
            return False

        #Calculates collision distance 
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = Object_Functions.distance(self.position,other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self,other_object):
        
        #If object is the same type, don't collide
        if other_object.__class__ == self.__class__:
            self.dead = False
        
        #If object is indestructable, don't collide
        elif self.destructable == False:
            self.dead = False

        #If object is Alien, then:
        elif self.__class__ == Alien: 
            self.alien_collision()

        else:
            self.dead = True

    def explosion(self,obj_x = 0.0,obj_y = 0.0):
        explosion_sprite = pyglet.sprite.Sprite(img=Resources.explosion,batch=Resources.effects_batch,x=obj_x,y=obj_y)
        explosion_sprite.scale = .75
        Resources.effects_list.append(explosion_sprite)
        self.dead = True
        
        #Makes sure the explosion only happens once
        duration = pyglet.image.Animation.get_duration(Resources.explosion)
        remove_explosion = pyglet.sprite.Sprite.delete(explosion_sprite)
        pyglet.clock.schedule_once(remove_explosion,duration)
        
class Player(PhyiscalObject):
    def __init__(self,x=400.0,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.player_image,*args,**kwargs)

        #Ship physics
        self.thrust = 100.0
        self.mass = 1.0
        self.rotate_speed = 75.0
        self.rotation = 0
        self.drag = .5
        
        #Ship handling
        self.key_handler = key.KeyStateHandler()

        #Bullet 
        self.bullet_speed = 1000.0
        self.fireonce = True
        self.reacts_to_bullets = False

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
        #Fire so the bullet goes the direction the ship is facing and take into account ship velocities
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
        pyglet.clock.schedule_interval(self.check_bounds_bullet,.05)

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


class Alien_Bullet(PhyiscalObject):
    def __init__(self,*args,**kwargs):
        super(Alien_Bullet,self).__init__(img=Resources.alien_bullet,*args,**kwargs)
        pyglet.clock.schedule_interval(self.check_bounds_bullet,.05)

        self.is_alien_bullet = True

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


class Alien(PhyiscalObject):
    def __init__(self,*args,**kwargs):
        
        super(Alien,self).__init__(img=Resources.alien_image, *args,**kwargs)


        #If True, Alien is already taking a path in movement
        self.movement = False
        self.health = 2
        self.is_falling = False

        #Alien bullet object
        self.bullet_speed = 500
        self.reacts_to_bullets = True
        self.reacts_to_alien_bullets = False
        self.firestatus = False
        
    def update(self, dt):

        super(Alien,self).update(dt)

        #Handles falling
        if self.is_falling is True:
            self.velocity_y -= self.gravity
            if self.y <= 50:
                self.explosion(self.x,self.y)
        
        #Handles movement updates       
        elif self.movement == False:
            time = random.uniform(0.01,1.5)
            self.choose_direction(dt)
            self.change_movement_status(dt)
            pyglet.clock.schedule_once(self.change_movement_status,time)

        
        #Handles Firing
        if self.firestatus is False:
            firetime = random.uniform(.75,1.5)
            pyglet.clock.schedule_once(self.fire,firetime)
            self.firestatus = True
    
    def choose_direction(self,dt):
        
        if self.is_falling is False:

            new_x_velocity = random.randint(-100,100)
            new_y_velocity = random.randint(-100,100)

            if self.x <= 75:
                new_x_velocity += 100
            elif self.x >= 750:
                new_x_velocity -= 100
            if self.y >= 550:
                new_y_velocity -= 100
            if self.y <= 100:
                new_y_velocity += 100

            self.velocity_x = new_x_velocity
            self.velocity_y = new_y_velocity

            self.movement = False
        
        else:
            pass
    
    def alien_collision(self):
        self.health -= 1
            
        #Alien ship falls
        if self.health == 1:
            self.fall()
        
        #Alien ship dies
        elif self.health == 0:
            self.explosion(self.x,self.y)
            

        else: #If Alien isn't dead or falling, then make them indestructable for a second and replace with alien damage picture
            self.destructable = False
            self.image = Resources.alien_damage_image
            pyglet.clock.schedule_once(self.damage_picture,1)

    def damage_picture(self,dt):
        
        self.image = Resources.alien_image
        self.destructable = True

    def fall(self):
        
        #Sets image to alien_damage
        self.image = Resources.alien_damage_image
        self.is_falling = True

        self.velocity_y -= self.gravity

        self.rotation = -45

    def fire(self,dt):
        
        #Fire so the bullet goes the direction the ship is facing and take into account ship velocities
        if self.dead is False:
            angle_to_player = math.degrees(Object_Functions.angle(self.position,player_ship.position))
            variance_in_shot = random.randint(-30,30)

            angle_radians = -math.radians(self.rotation - angle_to_player + variance_in_shot)
            ship_radius = self.image.width/2
            bullet_x = self.x + math.cos(angle_radians) * ship_radius
            bullet_y = self.y + math.sin(angle_radians) * ship_radius
            new_bullet = Alien_Bullet(x=bullet_x,y=bullet_y,batch=self.batch)

            bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
            bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
            new_bullet.velocity_x = bullet_vx
            new_bullet.velocity_y = bullet_vy

            new_bullet.rotation = self.rotation

            self.new_objects.append(new_bullet)

            self.firestatus = False

        else:
            pass

    def change_movement_status(self,dt):
        if self.movement is True:
            self.movement = False
        elif self.movement is False:
            self.movement = True

class Barrier(PhyiscalObject):
    pass



#Loads Sprites
player_ship = Player(x=100,y=100, batch=Resources.main_batch)
player_ship.x = 400
player_ship.y = 50