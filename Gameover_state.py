import Game_Framework
import Start_state
import fly_high
from pico2d import *
from pygame import mixer


name = "GameOverState"
image = None
Frame = 4

mixer.init()
mixer.music.load('resource/Sound/TitleSound.mp3')

def enter():
    global image
    image = load_image('resource/Aft_resource/GameoverState.png')
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
    update_canvas()







def update():
    global Frame
    if Frame != 0:
        Frame = Frame-1
        delay(0.5)
    pass


def pause():
    pass


def resume():
    pass






