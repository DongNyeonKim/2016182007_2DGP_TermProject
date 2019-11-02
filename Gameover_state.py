import Game_Framework
import Start_state
import fly_high
from pico2d import *
from pygame import mixer


name = "GameOverState"
image = None
text = None
Frame = 4

mixer.init()
mixer.music.load('resource/Sound/TitleSound.mp3')

def enter():
    global image, text
    image = load_image('resource/Aft_resource/GameoverState.png')
    text = load_image('resource/Aft_resource/gameover.png')
    mixer.music.play()

def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
                Game_Framework.change_state(Start_state)



def draw():
    clear_canvas()
    image.draw(400,300)
    text.draw(400,500)
    update_canvas()







def update():
    pass


def pause():
    pass


def resume():
    pass






