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


def player_lives(num_lives,batch=None):
    
    
    player_lives = []
    
    
    for i in range(num_lives):
        new_sprite = pyglet.sprite.Sprite(img=Resources.player_image,x=750-i*30,y=550,batch=batch)
        new_sprite.scale = 0.5
        player_lives.append(new_sprite)
    return player_lives


def respawn(lives,add_list,player,x_func,batch=None):

    lives -= 1

    if lives > 0:
        player.dead = False
        add_list.append(player)
        x_func(lives,batch=batch)

    else:
        #END GAME
        pass



