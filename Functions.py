import pyglet

import Objects
import Resources


def aliens_on_screen(num_aliens,batch=None):

    new_aliens = []

    alien_y = 450

        
    spacing = 800 // (num_aliens + 1)
    
    for _i in range(num_aliens):

        alien_x = (spacing * (_i + 1))

        alien = Objects.Alien(x=alien_x,y=alien_y,batch=batch)

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


def restart_game(window,game_objects,level):
    
    

    window.clear()

    for obj in game_objects:
        obj.delete()
        


    #Objects.game_obj.game_objects = []

    print(game_objects)

    #Alien Sprites
    Objects.game_obj.game_objects.extend(aliens_on_screen(2+level,batch=Resources.main_batch))

    #Barriers
    Objects.game_obj.game_objects.extend(generate_barriers(2-level,batch=Resources.main_batch))

    Objects.game_obj.game_objects.append(Objects.player_ship)

    Objects.player_ship.dead = False
    Objects.player_ship.lives = 3
    Objects.player_ship.x = 400
    Objects.player_ship.y = 50
    Objects.player_ship.points = 0

    Objects.end_obj.restart = False
    Objects.end_obj.close = False
    


def next_level():
    if Objects.game_obj.next_level == True:
        
        Objects.game_obj.game_objects.extend(aliens_on_screen(3+Objects.game_obj.level,batch=Resources.main_batch))
        
        Objects.game_obj.next_level = False