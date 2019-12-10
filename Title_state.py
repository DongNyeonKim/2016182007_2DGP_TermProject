import Game_Framework
import Start_state
import fly_high
from pico2d import *


name = "TitleState"
image = None
frame = 4
#Start_state에서 시작한 bgm이 Title_state 까지 이어짐

def enter():
    global image, frame, font
    frame =4

    image = load_image('resource/Aft_resource/Titlestate_ani.png')
    font = load_font('resource/ENCR10B.TTF', 23)


def exit():
    global image
    del image
    del Start_state.bgm

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()
        else:
            if(event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Game_Framework.change_state(Start_state)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
                Start_state.bgm.stop()
                fly_high.Enemy1_quantity = 7
                fly_high.Enemy2_quantity = 7
                fly_high.Enemy3_quantity = 5
                Game_Framework.change_state(fly_high)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
                Start_state.bgm.stop()
                fly_high.Enemy1_quantity = 8
                fly_high.Enemy2_quantity = 8
                fly_high.Enemy3_quantity = 7
                Game_Framework.change_state(fly_high)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
                Start_state.bgm.stop()
                fly_high.Enemy1_quantity = 12
                fly_high.Enemy2_quantity = 12
                fly_high.Enemy3_quantity = 10
                Game_Framework.change_state(fly_high)



def draw():
    clear_canvas()
    image.clip_draw(0, 600 * frame, 800, 600, 400, 300)
    if frame ==0:
        font.draw(500, 500, '(Press 1: EASY MODE)', (255, 255, 0))
        font.draw(500, 450, '(Press 2: NORMAL MODE)', (255, 255, 0))
        font.draw(500, 400, '(Press 3: HARD MODE)', (255, 255, 0))
    update_canvas()




def update():
    global frame
    if frame != 0:
        frame = frame - 1
        delay(0.5)
    pass


def pause():
    pass


def resume():
    pass






