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


#Edits images
def center_image(image):
    #sets an image's anchor point to its center
    
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

center_image(player_image)
center_image(bullet_image)
center_image(alien_image)
center_image(alien_damage_image)
center_image(alien_bullet)
center_image(barrier)
center_image(barrier_damage)

barrier.scale = 3


#Batches
main_batch = pyglet.graphics.Batch()
effects_batch = pyglet.graphics.Batch()
label_batch = pyglet.graphics.Batch()
end_batch = pyglet.graphics.Batch()
