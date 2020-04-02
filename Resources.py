import pyglet

#sets pyglet resource path
pyglet.resource.path = ['resources']
pyglet.resource.reindex()

#creates images for player
player_image = pyglet.resource.image('space_ship.png')
bullet_image = pyglet.resource.image('lazer.png')
alien_image = pyglet.resource.image('alien.png')
alien_damage_image = pyglet.resource.image('alien_damage.png')
alien_bullet = pyglet.resource.image('alien_lazer.png')
explosion = pyglet.resource.animation('explosion.gif')
barrier = pyglet.resource.image('barrier.png')
barrier_damage = pyglet.resource.image('barrier_damage.png')
mothership = pyglet.resource.animation('mothership.gif')
space_ship_shields = pyglet.resource.animation('space_ship_shields.gif')
powerup = pyglet.resource.animation('powerup.gif')
killshot = pyglet.resource.animation('killshot.gif')
killshot_effects = pyglet.resource.animation('killshot_effects.gif')



#Edits images
def center_image(image):
    #sets an image's anchor point to its center
    
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

def animation_center(anim):
    for f in anim.frames:
        f.image.anchor_x = f.image.width // 2
        f.image.anchor_y = f.image.height // 2

center_image(player_image)
center_image(bullet_image)
center_image(alien_image)
center_image(alien_damage_image)
center_image(alien_bullet)
center_image(barrier)
center_image(barrier_damage)

animation_center(explosion)
animation_center(space_ship_shields)
animation_center(powerup)
animation_center(killshot)
animation_center(killshot_effects)


barrier.scale = 3
mothership.scale = .1

#Batches
main_batch = pyglet.graphics.Batch()
effects_batch = pyglet.graphics.Batch()
label_batch = pyglet.graphics.Batch()
end_batch = pyglet.graphics.Batch()
title_batch = pyglet.graphics.Batch()
