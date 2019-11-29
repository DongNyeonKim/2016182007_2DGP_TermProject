import Game_Framework
import Start_state
import Title_state
import fly_high
from pico2d import *
from pygame import mixer

name = "GameOverState"
image = None
text = None
ani = None
font = None
Time = None
mixer.init()
mixer.music.load('resource/Sound/TitleSound.mp3')


def enter():
    global image, text, ani, Frame, font, blinkering
    image = load_image('resource/Aft_resource/GameoverState.png')
    text = load_image('resource/Aft_resource/gameover.png')
    ani = load_image('resource/Aft_resource/Gameout_ani.png')
    font = load_font('resource/ENCR10B.TTF', 45)
    Frame = 0
    blinkering = 0
    # mixer.music.play()


def exit():
    global image, text, ani
    del image
    del text
    del ani


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
                Game_Framework.change_state(Title_state)


def draw():
    clear_canvas()
    image.draw(400, 300)
    text.draw(400, 500)
    if Frame != 5:
        ani.clip_draw(0, 600 * Frame, 800, 600, 400, 300)
    if Frame == 5 and 30>= blinkering % 60 >= 1:
        font.draw(225, 400, 'LapTime:%3.2fsec' % Time, (255, 0, 128))
    update_canvas()


def update():
    global Frame, blinkering
    if Frame != 5:
        Frame = Frame + 1
        delay(0.5)
    blinkering += 1
    pass


def pause():
    pass


def resume():
    pass
