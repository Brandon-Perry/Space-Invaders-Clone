import pyglet

import Objects


def aliens_on_screen(num_aliens,batch=None):

    new_aliens = []

    alien_x = 100
    alien_y = 450

    for _i in range(num_aliens):
        
        alien_x += 100*_i

        alien_enemy = Objects.Alien(x=alien_x,y=alien_y,batch=batch)
        new_aliens.append(alien_enemy)

    return new_aliens




