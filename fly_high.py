from pico2d import *
import Game_Framework
import Title_state

import random

name = "Main_state"

background = None
my_jet = None
my_bullet = None




class BACKGROUND:
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
    x = 400
    y = 300

    def __init__(self):
        self.image = load_image('resource/Aft_resource/jet21.png')
        self.frame = 0
        pass

    def update(self):
        self.frame = (self.frame + 1) % 6
        self.x += self.move_x
        self.y += self.move_y
        self.x = clamp(25, self.x, 800 - 25)
        self.y = clamp(25, self.y, 600 - 45)
        print(self.x, self.y)
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 80, self.x, self.y)
        pass


class MY_BULLET:

    def __init__(self):
        self.image = load_image('resource/Aft_resource/Fire_Myjet.png')
        self.x = my_jet.x
        self.y = my_jet.y
        self.sign = 0
        pass

    def update(self):
        if self.sign == 0:
            self.x = my_jet.x
            self.y = my_jet.y + 35
            self.sign = 1

        if self.y != 610:
            self.y += 0.5

        pass

    def draw(self):
        self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
        pass

class MY_FRIEND:


    def __init__(self):
        self.image = load_image('resource/Aft_resource/My_Friend.png')
        self.image1 = load_image('resource/Aft_resource/My_Friend.png')
        pass

    def update(self):
        self.x += self.move_x
        self.y += self.move_y
        self.x = clamp(25, self.x, 800 - 25)
        self.y = clamp(25, self.y, 600 - 45)
        print(self.x, self.y)
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 40, 0, 40, 80, self.x, self.y)
        pass

def enter():
    global my_jet, background, my_bullets
    my_jet = MY_JET()
    background = BACKGROUND()
    my_bullets = []


def exit():
    global my_jet, background, my_bullets
    del (my_jet)
    del (background)
    del (my_bullets)


def pause():
    pass


def resume():
    pass


def handle_events():
    global my_jet, my_bullets
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()

        if event.type == SDL_KEYDOWN:
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
            elif event.key == SDLK_z:
                bullet = MY_BULLET()
                my_bullets.append(bullet)
            elif event.key == SDLK_a:
                pass
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                MY_JET.move_y -= 1
            elif event.key == SDLK_DOWN:
                MY_JET.move_y += 1
            elif event.key == SDLK_RIGHT:
                MY_JET.move_x -= 1
            elif event.key == SDLK_LEFT:
                MY_JET.move_x += 1
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_a:
                pass


def update():
    background.update()
    my_jet.update()
    for bullet in my_bullets:
        bullet.update()
    pass


def draw():
    clear_canvas()
    background.draw()
    my_jet.draw()
    for bullet in my_bullets:
        bullet.draw()
    update_canvas()
