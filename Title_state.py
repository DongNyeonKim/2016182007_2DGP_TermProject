import Game_Framework
import Start_state
import fly_high
from pico2d import *
from pygame import mixer


name = "TitleState"
image = None
Frame = 4

mixer.init()
mixer.music.load('resource/Sound/TitleSound.mp3')

def enter():
    global image, Frame
    Frame =4

    image = load_image('resource/Aft_resource/Titlestate_ani.png')
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
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                mixer.music.stop()
                Game_Framework.change_state(Start_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
                mixer.music.stop()
                fly_high.Enemy1_quantity = 5
                fly_high.Enemy2_quantity = 5
                fly_high.Enemy3_quantity = 3
                Game_Framework.change_state(fly_high)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
                mixer.music.stop()
                fly_high.Enemy1_quantity = 7
                fly_high.Enemy2_quantity = 7
                fly_high.Enemy3_quantity = 5
                Game_Framework.change_state(fly_high)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
                mixer.music.stop()
                fly_high.Enemy1_quantity = 12
                fly_high.Enemy2_quantity = 12
                fly_high.Enemy3_quantity = 9
                Game_Framework.change_state(fly_high)



def draw():
    clear_canvas()
    image.clip_draw(0,600*Frame,800,600,400,300)
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






