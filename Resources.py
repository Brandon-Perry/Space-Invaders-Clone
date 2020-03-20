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


#Batches
main_batch = pyglet.graphics.Batch()