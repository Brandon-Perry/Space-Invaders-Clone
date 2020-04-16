import pyglet
import Resources
import Objects

def game_screen(window):
    window.clear()
    Resources.background_batch.draw()
    Resources.main_batch.draw()
    Resources.effects_batch.draw()  
    Resources.label_batch.draw()

def end_screen(window,game_objects):
    window.clear()
    end_text = pyglet.text.Label("Oh dear! You've lost the game ;)",x=window.height/2,y=window.width/2)
    end_text.draw()

    start_again_text = pyglet.text.Label("Press Y to start again. Press N to quit",x=end_text.x,y=end_text.y-100)
    start_again_text.draw()

    Resources.end_batch.draw()

def title_screen(window,game_objects):
    window.clear()
    title_text = pyglet.text.Label("Oh dear! You've stumbled into a poor Space Invaders Parody",x=window.height/2,y=window.width/2)
    title_text.draw()

    title_again_text = pyglet.text.Label("Press ENTER for some fffuuunnn",x=title_text.x,y=title_text.y-100)
    title_again_text.draw()

    Resources.title_batch.draw()
