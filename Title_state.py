import Game_Framework
import Start_state
import fly_high
from pico2d import *
from pygame import mixer


name = "TitleState"
image = None
image1= None
Frame = 4
mixer.init()
mixer.music.load('resource/Sound/TitleSound.mp3')

def enter():
    global image, image1, Frame
    image = load_image('resource/Aft_resource/Title_state.png')
    image1 = load_image('resource/Aft_resource/Titlestate_ani.png')
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
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                mixer.music.stop()
                Game_Framework.change_state(fly_high)



def draw():
    clear_canvas()
    image.draw(400 , 300)
    #image1.clip_draw(0, 600*Frame, 800, 600*(Frame+1), 400, 300)
    image1.clip_draw(0,600*Frame,800,600,400,300)
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






