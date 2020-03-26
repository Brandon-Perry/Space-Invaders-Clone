import pyglet

import Objects
import Resources


def aliens_on_screen(num_aliens,batch=None):

    new_aliens = []

    alien_x = 100
    alien_y = 450

    for _i in range(num_aliens):
        
        alien_x += 100*_i

        alien_enemy = Objects.Alien(x=alien_x,y=alien_y,batch=batch)
        new_aliens.append(alien_enemy)

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
    #Updates objects and adds objects to game
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


def update_titles(dt):
    title_obj = [Objects.title_obj,Objects.end_obj]
    for obj in title_obj:
        obj.update(dt)


def start_game(window):
    

    #Alien Sprites
    Aliens = aliens_on_screen(3,batch=Resources.main_batch)

    #Barriers
    Barriers = generate_barriers(4,batch=Resources.main_batch)

    #list of game objects on screen
    game_objects = [Objects.player_ship] + Aliens + Barriers 

    Objects.player_ship.dead = False
    Objects.player_ship.lives = 3

    Objects.end_obj.restart = False
    
    

    return game_objects