import pyglet

import Objects
import Resources
import random

'''
def aliens_on_screen(num_aliens,batch=None):

    new_aliens = []

    alien_y = 450

        
    spacing = 800 // (num_aliens + 1)
    
    for _i in range(num_aliens):

        alien_x = (spacing * (_i + 1))

        alien = Objects.Alien(x=alien_x,y=alien_y,batch=batch)

        #Changes the size
        alien.scale = 1.4

        new_aliens.append(alien)

    return new_aliens


def generate_barriers(num_barriers,batch=None):

    new_barriers = []

    spacing = 800 // (num_barriers + 1)
    
    for _i in range(num_barriers):

        barrier_x = (spacing * (_i + 1))

        barrier = Objects.Barrier(x=barrier_x,y=200,batch=batch)

        new_barriers.append(barrier)

    return new_barriers
'''

def player_lives(num_lives=0,batch=None):
    
    
    player_lives = []
    
    
    for i in range(num_lives):
        new_sprite = pyglet.sprite.Sprite(img=Resources.player_image,x=750-i*30,y=550,batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives
  
'''
def respawn(player,add_list):

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
'''

def check_endgame(player):
    if player.lives <= 0:
        return True
    else:
        return False


def collision_check(game_objects):
    #Checks each object active to see if collision kills
    for i in range(len(game_objects)):
        for j in range(i+1, len(game_objects)):
            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)


def send_mothership(game_objects,batch=None):

    x = random.randint(1,250)

    if x == 5:

        new_mothership = Objects.Mothership(start='Left',x=100,y=400,batch=batch)

        new_mothership.scale = 1.3

        game_objects.append(new_mothership)

