import Game_Framework
import Title_state
from pico2d import *
from pygame import mixer

name = "StartState"
image = None
Name = None
logo_time = 0.0


def enter():
    global image, Name
    image = load_image('resource/Aft_resource/Title_state.png')
    Name = load_image('resource/Aft_resource/TitleName1.png')
    # mixer.music.play()

def exit():
    global image
    del(image)


def update():
    global logo_time

    if(logo_time>1.0):
        logo_time = 0
        Game_Framework.change_state(Title_state)
    delay(0.03)
    logo_time += 0.01


def draw():
    global image
    clear_canvas()
    image.draw(400,300)
    Name.draw(660,100)
    update_canvas()




def handle_events():
    pass




def pause(): pass


def resume(): pass




