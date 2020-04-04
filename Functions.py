import pyglet

import Objects
import Resources
import random


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


def player_lives(num_lives=0,batch=None):
    
    
    player_lives = []
    
    
    for i in range(num_lives):
        new_sprite = pyglet.sprite.Sprite(img=Resources.player_image,x=750-i*30,y=550,batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives
  

def respawn(player,add_list):

    if player.lives > 0:
    
        player.dead = False
        add_list.append(player)
        player.x = 400
        player.y = 100
    else:
        pass


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


def update_and_add_game_objects(game_objects,dt):
    #Updates objects and adds objects to game, game decides whether to respawn player here
    to_add = []

    for obj in game_objects:
        obj.update(dt)
        game_objects.extend(obj.new_objects)
        obj.new_objects = []

    for to_remove in [obj for obj in game_objects if obj.dead]:
        if not to_remove == Objects.player_ship:
            to_remove.delete() 
            
        if to_remove == Objects.player_ship:
            respawn(Objects.player_ship,game_objects)
        game_objects.remove(to_remove)

    game_objects.extend(to_add)


def restart_game(window,game_objects,level):
    
    

    window.clear()

    del Objects.game_obj.game_objects[0:]
    Objects.game_obj.game_objects = []
    
    
    Resources.main_batch = pyglet.graphics.Batch()
    Resources.effects_batch = pyglet.graphics.Batch()
    Resources.label_batch = pyglet.graphics.Batch()
    Resources.end_batch = pyglet.graphics.Batch()
    Resources.title_batch = pyglet.graphics.Batch()

    print(game_objects)

    #Alien Sprites
    Objects.game_obj.game_objects.extend(aliens_on_screen(3,batch=Resources.main_batch))

    #Barriers
    Objects.game_obj.game_objects.extend(generate_barriers(4,batch=Resources.main_batch))

    Objects.player_ship = Objects.Player(x=400,y=500, batch=Resources.main_batch)
    Objects.game_obj.game_objects.append(Objects.player_ship)

    Objects.player_ship.dead = False
    Objects.player_ship.lives = 3
    Objects.player_ship.x = 400
    Objects.player_ship.y = 50
    Objects.player_ship.points = 0

    Objects.end_obj.restart = False
    Objects.end_obj.close = False

    Objects.game_obj.next_level = False
    Objects.game_obj.level = 1
    
    Objects.score_label = pyglet.text.Label(text="Score: " + str(Objects.player_ship.points),x=25,y=550,batch=Resources.label_batch)
    Objects.level_label = pyglet.text.Label(text='Level: ' + str(Objects.game_obj.level),x=400,y=550,batch=Resources.label_batch)

    print(game_objects)


def next_level():
    if Objects.game_obj.next_level == True:
        
        Objects.game_obj.game_objects.extend(aliens_on_screen(3+Objects.game_obj.level,batch=Resources.main_batch))
        
        Objects.game_obj.next_level = False


def send_mothership(game_objects,batch=None):

    x = random.randint(1,250)

    if x == 5:

        new_mothership = Objects.Mothership(start='Left',x=100,y=400,batch=batch)

        new_mothership.scale = 1.3

        game_objects.append(new_mothership)

