import pyglet
from pyglet.window import key
import math
import random

#import game files
import Resources
import Object_Functions

global_key_handler = key.KeyStateHandler()

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
        min_x = self.width / 2
        min_y = self.height / 2
        max_x = 800 - self.width / 2
        max_y = 600 - self.height / 2
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

        if self.__class__ == Boss_Bullet and other_object.__class__ == Boss:
            return False
        if self.__class__ == Boss and other_object.__class__ == Boss_Bullet:
            return False

        #Calculates collision distance 
        collision_distance = self.width/2 + other_object.width/2
        actual_distance = Object_Functions.distance(self.position,other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self,other_object):  #need to make it so player ship and aliens can't pass through barrier
        
        ###
        ###This top part should have collisions that are universal across all objects, like sprites
        ###
        
        #If object is the same type, don't collide
        if other_object.__class__ == self.__class__:
            self.dead = False
        
        #If object is indestructable, don't collide. Powerups and ship with shields should collide
        elif self.destructable == False:
            if (self.__class__ == Player and other_object.__class__ == Powerup)\
                or (self.__class__ == Powerup and other_object.__class__ == Player):
                pass
            else:
                self.dead = False

        #Don't collide with effects
        elif self.__class__ == Effects or other_object.__class__ == Effects:
            self.dead = False
            other_object.dead = False

        ###
        ###This part should have collisions for damage
        ###

        #If object is Alien, then:
        elif self.__class__ == Alien: 
            self.alien_collision(other_object)

        elif self.__class__ == Boss:
            self.boss_collision(other_object)

        ###
        ###Specicial collisions instances
        ###
        
        
        #Aliens and motherships shouldn't collide
        elif self.__class__ == Mothership and other_object.__class__ == Alien:
            self.dead = False
            other_object.dead = False

        #If object is barrier, don't damage Player
        elif self.__class__ == Barrier:
            if other_object.__class__ == Player:
                self.ship_barrier_collision(other_object)
            else:
                self.barrier_collision()

        #Special collision for player_bullets and mothership. Bullet destroys self
        elif self.__class__ == Mothership and other_object.__class__ == Player_Bullet:
            self.mothership_shot()
        

        #Special collision for powerup and barrier (stops movement)
        elif self.__class__ == Powerup and other_object.__class__ == Barrier:
            self.velocity_y = 0
            self.y = other_object.y + other_object.width/2       

        #Handles special collisions for player
        elif self.__class__ == Player:
            if other_object.__class__ == Barrier:
                pass
            if other_object.__class__ == Powerup:
                self.dead = False
                self.determine_powerup(other_object)
            else:
                self.player_dies()

        #Prevents other objects from destroying powerups
        elif (self.__class__ == Powerup and other_object.__class__ != Player)\
            or (self.__class__ != Player and other_object.__class__ == Powerup):
            self.dead = False
            other_object.dead = False



        else:
            self.dead = True
        
    def explosion(self,obj_x = 0.0,obj_y = 0.0):
        explosion_sprite = pyglet.sprite.Sprite(img=Resources.explosion,batch=Resources.effects_batch,x=obj_x,y=obj_y)
        explosion_sprite.scale = .75
        self.dead = True
        
        #Makes sure the explosion only happens once
        duration = pyglet.image.Animation.get_duration(Resources.explosion)
        def remove_explosion(t):
            pyglet.sprite.Sprite.delete(explosion_sprite)
         
        pyglet.clock.schedule_once(remove_explosion,duration)
        
        
class Player(PhyiscalObject):

    def __init__(self,x=400.0,y=100.0,*args,**kwargs):
        super().__init__(img=Resources.player_image,*args,**kwargs)

        #Ship physics
        self.thrust = 200.0
        self.mass = 1.0
        self.rotate_speed = 75.0
        self.rotation = 0
        self.drag = .5
        
        #Ship handling
        self.key_handler = global_key_handler

        #Bullet 
        self.bullet_speed = 1000.0
        self.fireonce = True
        self.reacts_to_bullets = False
        self.reacts_to_alien_bullets = True
        self.killshot_on = False

        #Player's attributes
        self.points = 0
        self.lives = 3

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
        min_rotation = -50
        max_rotation = 50

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
        ship_radius = self.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = Player_Bullet(x=bullet_x,y=bullet_y,batch=self.batch,killshot=self.killshot_on)

        bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
        bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        new_bullet.rotation = self.rotation           

        self.new_objects.append(new_bullet)

    def ship_barrier_collision(self):
        pass

    def hit_alien(self):
        self.points += 100

    def kill_alien(self):
        self.points += 1000

    def player_dies(self):
        self.dead = True
        self.lives -= 1
        print(self.lives)
        self.explosion(obj_x=self.x,obj_y=self.y)

    def determine_powerup(self,other_object):

        if other_object.feature == 'life':
            self.new_life()
            print('got an extra life!')

        if other_object.feature == 'killshot':
            self.killshot()
            print('Got killshot!')

        if other_object.feature == 'shields':
            self.shields()
            print('Got shields!')

    def new_life(self):
        self.lives += 1

        new_effect = Effects(effects_code='life',x=self.x,y=self.y,\
            batch=Resources.effects_batch)

        new_effect.scale = 2

        self.new_objects.append(new_effect)

    def killshot(self):
        #Killshot If statement in the fire function
        self.killshot_on = True

        new_effect = Effects(effects_code='killshot_text',x=self.x,y=self.y,\
            batch=Resources.effects_batch)

        self.new_objects.append(new_effect)

        pyglet.clock.schedule_once(self.killshot_off,5)

    def killshot_off(self,dt):
        self.killshot_on = False

    def shields(self):
        
 
        self.destructable = False
        self.image = Resources.space_ship_shields

        pyglet.clock.schedule_once(self.turn_off_shields,7)

    def turn_off_shields(self,dt):
            self.destructable = True
            self.image = Resources.player_image


class Player_Bullet(PhyiscalObject):
    def __init__(self,killshot=None,*args,**kwargs):
        
        self.killshot = killshot
        
        super(Player_Bullet,self).__init__(img=self.determine_image(),*args,**kwargs)
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

    def determine_image(self):
        if self.killshot == False:
            return Resources.bullet_image

        elif self.killshot == True:
            return Resources.killshot

    def killshot_effects(self):
        
        def killshot_spread():
            return random.randint(-5,5)
        
        if self.killshot == True:

            new_effect = Effects(effects_code='killshot',x=self.x + killshot_spread(),\
                y=self.y + killshot_spread(),batch=Resources.effects_batch)

            self.new_objects.append(new_effect)

    def update(self,dt):
        super(Player_Bullet,self).update(dt)

        self.killshot_effects()

                           
class Effects(PhyiscalObject):

    def __init__(self,effects_code = None, *args,**kwargs):

        self.effects_code = effects_code
        self.duration = self.effect_length()

        super(Effects,self).__init__(img=self.determine_effects(),*args,**kwargs)

        pyglet.clock.schedule_once(self.die,self.duration)

        self.destructable = False
        self.reacts_to_alien_bullets = False
        self.reacts_to_bullets = False

    def determine_effects(self):
        
        if self.effects_code == 'killshot':
            return Resources.killshot_effects
        
        elif self.effects_code == 'killshot_text':
            return Resources.killshot_text

        elif self.effects_code == 'life':
            return Resources.life_text

        elif self.effects_code == 'boss_explosion':
            return Resources.explosion

    def effect_length(self):
        if self.effects_code == 'killshot':
            return pyglet.image.Animation.get_duration(Resources.killshot_effects)
        elif self.effects_code == 'killshot_text':
            return pyglet.image.Animation.get_duration(Resources.killshot_text)
        
        elif self.effects_code == 'life':
            return pyglet.image.Animation.get_duration(Resources.life_text) * 2

        elif self.effects_code == 'boss_explosion':
            return pyglet.image.Animation.get_duration(Resources.explosion)

    def die(self,dt):
        self.dead = True

    def update(self,dt):
        super(Effects,self).update(dt)

        if self.effects_code == 'killshot_text':
            self.velocity_y = 100

        elif self.effects_code == 'life':
            self.velocity_y = 100
        

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
        
        super().__init__(img=Resources.alien_image, *args,**kwargs)


        #If True, Alien is already taking a path in movement
        self.movement = False
        self.health = 3
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
    
    def alien_collision(self,other_object):  
        
        #Prevents collision between mothership and aliens
        if other_object.__class__ == Mothership:
            self.dead = False
            other_object.dead = False
        else:
        
            self.health -= 1
            player_ship.hit_alien()

            #Instakill with killshot
            if other_object.__class__ == Player_Bullet and other_object.killshot == True:
                self.health = 0

            #Alien ship falls
            if self.health == 1:
                self.fall()
            
            #Alien ship dies
            elif self.health == 0:
                self.explosion(self.x,self.y)
                pyglet.clock.unschedule(self.damage_picture)
                player_ship.kill_alien()
                

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

        #self.velocity_y -= self.gravity

        self.rotation = -45

        #Unschedule changing the damage picture
        pyglet.clock.unschedule(self.damage_picture)

    def fire(self,dt): ####Needs to be fixed with player ship
        
        #Fire so the bullet goes the direction the ship is facing and take into account ship velocities
        if self.dead is False:
            angle_to_player = math.degrees(Object_Functions.angle(self.position,player_ship.position))
            variance_in_shot = random.randint(-30,30)

            angle_radians = -math.radians(self.rotation - angle_to_player + variance_in_shot)
            ship_radius = self.width/2
            bullet_x = self.x + math.cos(angle_radians) * ship_radius
            bullet_y = self.y + math.sin(angle_radians) * ship_radius
            new_bullet = Alien_Bullet(x=bullet_x,y=bullet_y,batch=self.batch)

            bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
            bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
            new_bullet.velocity_x = bullet_vx
            new_bullet.velocity_y = bullet_vy

            #Sets rotation of the bullet
            
            #bullet_angle = math.degrees(math.cos(self.velocity_y/Object_Functions.distance(new_bullet.position,player_ship.position)))
            #new_bullet.rotation = bullet_angle

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
    def __init__(self,*args,**kwargs):

        super(Barrier,self).__init__(img=Resources.barrier,*args,**kwargs)

        self.health = 5
        self.destructable = True
        self.is_bullet = False
        self.is_alien_bullet = False
        self.reacts_to_alien_bullets = True
        self.reacts_to_bullets = True

    def barrier_collision(self):
        self.health -= 1
        
        self.destructable = False
        self.image = Resources.barrier_damage
        
        def temp(dt):
            self.image = Resources.barrier
            self.destructable = True
            if self.health <= 0:
                self.dead = True

        pyglet.clock.schedule_once(temp,.25)

    def update(self,dt):
        super(Barrier,self).update(dt)

        if self.velocity_y > 0:
            self.velocity_y -= 5
        else:
            self.velocity_y = 0

    def ship_barrier_collision(self,other_object):
        self.velocity_y += other_object.velocity_y * .1

     
class Mothership(PhyiscalObject):
    
    def __init__(self,start=None,x=0,y=0,*args,**kwargs):
        super(Mothership,self).__init__(img=Resources.mothership,*args,**kwargs)

        self.powerup = random.randint(1,3)
        self.health = 1
        self.reacts_to_alien_bullets = False
        self.reacts_to_bullets = True
        self.start = start
        self.velocity_x = 100
        self.x = x
        self.y = y

    def spawn_powerup(self):

        if self.powerup == 1:
            new_powerup = Powerup(x=self.x,y=self.y,feature='life',batch=Resources.main_batch)
            self.new_objects.append(new_powerup)

        elif self.powerup == 2:
            new_powerup = Powerup(x=self.x,y=self.y,feature='killshot',batch=Resources.main_batch)
            self.new_objects.append(new_powerup)

        elif self.powerup == 3:
            new_powerup = Powerup(x=self.x,y=self.y,feature='shields',batch=Resources.main_batch)
            self.new_objects.append(new_powerup)

    def update(self,dt):

        #Depending on which side of the screen mothership starts, mothership moves left or right. If reaches edge, dead.
        if self.start == 'Left':
            self.x += self.velocity_x * dt
            #if self.x == 800:
                #self.dead = True

        elif self.start == 'Right':
            self.x -= self.velocity_x * dt
            #if self.x == 0:
                #self.dead = True

    def mothership_shot(self):
        self.spawn_powerup()
        self.dead = True
        
        
class Powerup(PhyiscalObject):
    
    def __init__(self,x=0,y=0,feature=None,*args,**kwargs):
        super(Powerup,self).__init__(img=Resources.powerup,*args,**kwargs)

        self.feature = feature
        self.health = 1
        self.reacts_to_bullets = False
        self.reacts_to_alien_bullets = False
        self.x = x
        self.y = y
        self.upgrade = None

    def update(self,dt):
        self.y -= self.gravity
        
        #Prevents from falling through floor
        if self.y <= 5:
            self.y = 5
 

class Boss(PhyiscalObject):

    def __init__(self,*args,**kwargs):

        super().__init__(img=Resources.putin,*args,**kwargs)

        #Handles life and damage
        self.health = 10
        self.isdying = False
        self.reacts_to_alien_bullets = False
        self.reacts_to_bullets = True
        self.explosion_count = 0

        #Handles movement
        self.movement = False
        self.navigating = False
        self.nav_x = None
        self.nav_y = None

        #Handles attacks
        #Attack status is True when it is in the middle of attacking or in the cool off
        self.attack_status = False
        self.lazer_status = False
        self.beam_status = False
        self.beam_loc = None
        self.lazer_count = 0
        self.bullet_speed = 300


    def update(self,dt):

        super(Boss,self).update(dt)

        #Handles attacks
        if self.attack_status == False and self.isdying == False:

            self.choose_attack()

        if self.beam_status == True and self.navigating == False:

                self.fire_beam()

        #Handles movement      
        if self.movement == False and self.navigating == False:
            time = random.uniform(0.01,1.5)
            self.choose_direction()
            self.change_movement_status(dt)
            pyglet.clock.schedule_once(self.change_movement_status,time)

        elif self.navigating == True:
            self.navigation_check()


    def choose_attack(self):

        attack_type = random.randint(1,2)

        if attack_type == 1:

            pyglet.clock.schedule_interval(self.lazer_attack,.1)
            self.attack_status = True

        elif attack_type == 2:

            self.beam_attack()
            self.attack_status = True
            

    def choose_direction(self):
        
        if self.isdying == False:

            new_x_velocity = random.randint(-100,100)
            new_y_velocity = random.randint(-75,75)

            if self.x <= 75:
                new_x_velocity += 200
            elif self.x >= 750:
                new_x_velocity -= 200
            if self.y >= 650:
                new_y_velocity -= 100
            if self.y <= 200:
                new_y_velocity += 150

            self.velocity_x = new_x_velocity
            self.velocity_y = new_y_velocity

            self.movement = False
        
        else:
            self.velocity_x = 0
            self.velocity_y = 0


    def change_movement_status(self,dt):
        if self.movement is True:
            self.movement = False
        elif self.movement is False:
            self.movement = True


    def lazer_attack(self,dt):
        
        #Fire so the bullet goes the direction the ship is facing and take into account ship velocities
        angle_to_player = math.degrees(Object_Functions.angle(self.position,player_ship.position))
        variance_in_shot = random.randint(0,0)

        angle_radians = -math.radians(self.rotation - angle_to_player + variance_in_shot)
        self_radius = self.width/2
        bullet_x = self.x + math.cos(angle_radians) * self_radius
        bullet_y = self.y + math.sin(angle_radians) * self_radius
        new_bullet = Boss_Bullet(x=bullet_x,y=bullet_y,batch=self.batch)

        bullet_vx = (self.velocity_x + math.cos(angle_radians) * self.bullet_speed)
        bullet_vy = (self.velocity_y + math.sin(angle_radians) * self.bullet_speed)
        new_bullet.velocity_x = bullet_vx
        new_bullet.velocity_y = bullet_vy

        new_bullet.scale = 3

        #Sets rotation of the bullet
        
        #bullet_angle = math.degrees(math.cos(self.velocity_y/Object_Functions.distance(new_bullet.position,player_ship.position)))
        #new_bullet.rotation = bullet_angle

        self.new_objects.append(new_bullet)

        #Adds count to lazer_count to ensure burst of certain number
        self.lazer_count += 1

        #Ensure only a certain number of lazers fire at once, then resets firestatus and lazerstatus after some period
        if self.lazer_count >= 10:
            self.reset_attack_status(func=self.lazer_attack)
            self.lazer_count = 0


    def beam_attack(self):

        self.navigating = True
        self.beam_status = True
        self.movement = True

        self.beam_loc = random.randint(1,4)

        if self.beam_loc == 1:
            self.nativgate_to(600,700)
        elif self.beam_loc == 2 or self.beam_loc == 3:
            self.nativgate_to(400,700)
        elif self.beam_loc == 4:
            self.nativgate_to(200,700)


    def fire_beam(self):
        new_beam = Boss_Beam(x=self.x, y=self.y//4, batch=Resources.main_batch)
        new_beam.image.height = self.y
        
        self.new_objects.append(new_beam)

        #Handles movement while beam is firing
        if self.beam_loc == 1:
            self.velocity_x = -100
        elif self.beam_loc == 2:
            self.velocity_x = -100
        elif self.beam_loc == 3:
            self.velocity_x = 100
        elif self.beam_loc == 4:
            self.velocity_x = 100

        #Once boss has reached end of listed trajectory, end beam attack
        if (self.beam_loc == 1 and self.x <= 400) or ((self.beam_loc == 2 or self.beam_loc == 3) and (self.x <= 200 or self.x >=600)) or \
            (self.beam_loc == 4 and self.x >= 400):
            self.beam_status = False
            self.movement = False
            self.reset_attack_status(func=self.fire_beam)


    def nativgate_to(self,location_x,location_y):

        self.navigating = True

        self.velocity_y =  location_y - self.y
        self.velocity_x = location_x - self.x

        self.nav_x = location_x
        self.nav_y = location_y


    def navigation_check(self):


        if self.velocity_x > 0:
            if self.x > self.nav_x:
                self.velocity_x = 0
        elif self.velocity_x < 0:
            if self.x < self.nav_x:
                self.velocity_x = 0

        if self.velocity_y > 0:
            if self.y > self.nav_y:
                self.velocity_y = 0
        elif self.velocity_y < 0:
            if self.y < self.nav_y:
                self.velocity_y = 0

        if self.velocity_x == 0 and self.velocity_y == 0:
            self.navigating = False


        #self.velocity_y =  self.nav_y - self.y
        #self.velocity_x = self.nav_x - self.x


    def boss_collision(self,other_object):
        
        #Prevents collision between mothership and boss
        if other_object.__class__ == Mothership:
            self.dead = False
            other_object.dead = False

        elif other_object.__class__ == Alien:
            self.dead = False
            other_object.dead = False
        else:
        
            self.health -= 1
            print(self.health)

            #Extra damage for killshot
            if other_object.__class__ == Player_Bullet and other_object.killshot == True:
                self.health -= 1

            #Boss goes into dying effects if at one health
            if self.health == 1:
                self.dying_sequence()
                          

            else: #If boss isn't dead or dying, then make them indestructable for a second and replace with boss damage picture
                self.destructable = False
                self.image = Resources.putin_damage
                pyglet.clock.schedule_once(self.damage_picture,.1)

    
    def dying_sequence(self):
        
        self.destructable = False
        self.isdying = True
        
        def explosions(dt):
            rand_x = random.randint(-100,100)
            rand_y = random.randint(-100,100)
            new_effect = Effects(effects_code='boss_explosion',x=self.x+rand_x,y=self.y+rand_y,batch=Resources.effects_batch)

            self.new_objects.append(new_effect)

            self.explosion_count += 1

            if self.explosion_count >= 10:
                pyglet.clock.unschedule(explosions)
                self.explosion(obj_x=self.x,obj_y=self.y)

        pyglet.clock.schedule_interval(explosions,.5)


    def damage_picture(self,dt):
        self.destructable = True
        self.image = Resources.putin


    def reset_attack_status(self,func=None):

        pyglet.clock.unschedule(func)
        print('unscheduled')

        time = random.randint(3,5)

        def reset(dt):
            self.attack_status = False
            print('reset')

        pyglet.clock.schedule_once(reset,time)
        

class Boss_Bullet(PhyiscalObject):

    def __init__(self,*args,**kwargs):

        super().__init__(img=Resources.boss_lazer,*args,**kwargs)

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


class Boss_Beam(PhyiscalObject):

    def __init__(self, *args, **kwargs):

        super().__init__(img=Resources.boss_beam,*args,**kwargs)

        pyglet.clock.schedule_once(self.die,.05)

        self.is_alien_bullet = True
        

    def die(self,dt):
        self.dead = True


class Background(pyglet.sprite.Sprite):

    def __init__(self, x=0, y=0, *args,**kwargs):
        super().__init__(img=Resources.background, *args, **kwargs)

        self.x = x
        self.y = y


class EndGame(pyglet.sprite.Sprite):
    
    def __init__(self, x=0,y=0, *args,**kwargs):
        self.key_handler = global_key_handler
        self.dead = False
        self.restart = False
        self.close = False
        #self.x = x
        #self.game_window = game_window

    def update(self,dt):
        if self.key_handler[key.Y]:
            self.restart = True
        elif self.key_handler[key.N]:
            self.close = True


class Title(pyglet.sprite.Sprite):
    
    def __init__(self, x=0,y=0, *args,**kwargs):
        self.key_handler = global_key_handler
        self.dead = False
        #self.x = x
        #self.game_window = game_window

    def update(self,dt):
        if self.key_handler[key.ENTER]:
            self.dead = True


class GamePlay(pyglet.sprite.Sprite):

    def __init__(self, x=0, y=0, *args, **kwargs):
        self.game_objects = []
        self.enemy_count = 0
        self.level = 0
        self.boss_level_num = 10
        self.boss_battle = False
        self.end_game = False

        #On initiation, load first level

    def level_load(self):
        
        if self.level == 1:

            self.clear_barriers()
            barriers = self.generate_barriers(3,batch=Resources.main_batch)
            
            aliens = self.aliens_on_screen(2,batch=Resources.main_batch)
            self.game_objects.extend(aliens)
            self.game_objects.extend(barriers)

        if self.level == 2:

            self.clear_barriers()
            aliens = self.aliens_on_screen(3,batch=Resources.main_batch)
            self.game_objects.extend(aliens)

        if self.level == 3:

            aliens = self.aliens_on_screen(4,batch=Resources.main_batch)

        

    def update(self,dt):
        
        #If this is a boss battle, then killing the boss should end the game
        if self.level is self.boss_level_num:

            self.load_boss()

            for obj in self.game_objects:
                if obj.__class__ == Boss:
                    self.end_game = True
                    break

        #Otherwise, count aliens and if aliens are killed, go to next level
        else:
        
            self.enemy_count = 0
            for obj in self.game_objects:
                if obj.__class__ == Alien:
                    self.enemy_count += 1

            if self.enemy_count == 0:
                self.level += 1
                self.level_load()

    def load_boss(self):

        if self.boss_battle == False:
            
            self.boss_battle = True

            putin_boss = Boss(x=400,y=400,batch=Resources.main_batch)

            putin_boss.scale = .75

            self.game_objects.append(putin_boss)


    def restart_game(self,window):
    

        window.clear()

        del self.game_objects[0:]
        self.game_objects = []
        
        
        Resources.main_batch = pyglet.graphics.Batch()
        Resources.effects_batch = pyglet.graphics.Batch()
        Resources.label_batch = pyglet.graphics.Batch()
        Resources.end_batch = pyglet.graphics.Batch()
        Resources.title_batch = pyglet.graphics.Batch()


        player_ship = Player(x=400,y=500, batch=Resources.main_batch)
        self.game_objects.append(player_ship)

        player_ship.dead = False
        player_ship.lives = 3
        player_ship.x = 400
        player_ship.y = 50
        player_ship.points = 0

        end_obj.restart = False
        end_obj.close = False

        self.level = 0
        
        #score_label = pyglet.text.Label(text="Score: " + str(player_ship.points),x=25,y=550,batch=Resources.label_batch)
        #level_label = pyglet.text.Label(text='Level: ' + str(self.level),x=400,y=550,batch=Resources.label_batch)


    def update_and_add_game_objects(self,dt):
        #Updates objects and adds objects to game, game decides whether to respawn player here
        to_add = []

        for obj in self.game_objects:
            obj.update(dt)
            self.game_objects.extend(obj.new_objects)
            obj.new_objects = []

        for to_remove in [obj for obj in self.game_objects if obj.dead]:
            if not to_remove == player_ship:
                to_remove.delete() 
                
            if to_remove == player_ship:
                self.respawn(player_ship,self.game_objects)
            self.game_objects.remove(to_remove)

        self.game_objects.extend(to_add)


    def aliens_on_screen(self,num_aliens,batch=None):

        new_aliens = []

        alien_y = 450

            
        spacing = 800 // (num_aliens + 1)
        
        for _i in range(num_aliens):

            alien_x = (spacing * (_i + 1))

            alien = Alien(x=alien_x,y=alien_y,batch=batch)

            #Changes the size
            alien.scale = 1.4

            new_aliens.append(alien)

        return new_aliens


    def generate_barriers(self,num_barriers,batch=None):

        new_barriers = []

        spacing = 800 // (num_barriers + 1)
        
        for _i in range(num_barriers):

            barrier_x = (spacing * (_i + 1))

            barrier = Barrier(x=barrier_x,y=200,batch=batch)

            new_barriers.append(barrier)

        return new_barriers


    def respawn(self,player,add_list):

        if player.lives > 0:
        
            player.dead = False
            add_list.append(player)
            player.x = 400
            player.y = 100
        else:
            pass

        def destructable_reset(dt):
            player.destructable = True

        player.destructable = False

        pyglet.clock.schedule_once(destructable_reset,2)

        player.velocity_x = 0
        player.velocity_y = 0
    

    def clear_barriers(self):

        delete_list = []

        for barrier in self.game_objects:
            if barrier.__class__ is Barrier:
                delete_list.append(self.game_objects.pop(self.game_objects.index(barrier)))
                
        del delete_list



#Player Sprite
player_ship = Player(x=100,y=100, batch=Resources.main_batch)
player_ship.x = 400
player_ship.y = 50

end_obj = EndGame(x=400,y=400,batch=Resources.end_batch)

title_obj = Title(x=0,y=0,batch=Resources.title_batch)

game_obj = GamePlay(x=0,y=0,batch=Resources.main_batch)

#Labels
score_label = pyglet.text.Label(text="Score: " + str(player_ship.points),x=25,y=550,batch=Resources.label_batch)
level_label = pyglet.text.Label(text='Level: ' + str(game_obj.level),x=400,y=550,batch=Resources.label_batch)