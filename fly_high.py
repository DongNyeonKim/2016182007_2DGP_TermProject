from pico2d import *
import Game_Framework
import Title_state

import random

name = "Main_state"

my_jet = None
background = None


class BackGround:
    def __init__(self):
        self.image = load_image('resource/Aft_resource/background.png')
        self.image1 = load_image('resource/Aft_resource/background.png')
        self.background_x, self.background_y = 0, 0
        self.move_y, self.move_y1 = 0, 0
        self.a, self.b = 900, 300

    def update(self):
        self.move_y -= 1
        self.move_y1 -= 1

        if self.a + self.move_y == -300:
            self.a = 900
            self.move_y = 0

        if self.b + self.move_y1 == -300:
            self.b = 900
            self.move_y1 = 0
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 800, 600, 800 // 2, self.a + self.move_y)
        self.image1.clip_draw(0, 0, 800, 600, 800 // 2, self.b + self.move_y1)
        pass

class MY_JET:
    move_x = 0
    move_y = 0
    def __init__(self):
        self.image = load_image('resource/Aft_resource/jet21.png')
        self.x, self.y = 400, 300
        self.frame = 0
        pass

    def update(self):
        self.frame = (self.frame + 1) % 6
        self.x += self.move_x
        self.y += self.move_y
        self.x = clamp(25, self.x, 800 - 25)
        self.y = clamp(25, self.y, 600 - 45)
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 80, self.x, self.y)
        pass

def enter():
    global my_jet, background
    my_jet = MY_JET()
    background = BackGround()


def exit():
    global my_jet, background
    del (my_jet)
    del (background)


def pause():
    pass


def resume():
    pass


def handle_events():
    global my_jet
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()

        if event.type ==SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_Framework.change_state(Title_state)
            elif event.key == SDLK_UP:
                MY_JET.move_y += 1
            elif event.key == SDLK_DOWN:
                MY_JET.move_y -= 1
            elif event.key == SDLK_RIGHT:
                MY_JET.move_x += 1
            elif event.key == SDLK_LEFT:
                MY_JET.move_x -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                MY_JET.move_y -= 1
            elif event.key == SDLK_DOWN:
                MY_JET.move_y += 1
            elif event.key == SDLK_RIGHT:
                MY_JET.move_x -= 1
            elif event.key == SDLK_LEFT:
                MY_JET.move_x += 1

def update():
    background.update()
    my_jet.update()
    pass


def draw():
    clear_canvas()
    background.draw()
    my_jet.draw()
    update_canvas()







