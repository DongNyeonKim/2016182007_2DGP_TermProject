from pico2d import *
import Game_Framework
import Title_state

import random

name = "Main_state"

background = None
my_jet = None
my_bullet = None
my_friend = None
enemy_jet = None

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
    image = None
    def __init__(self):
        if MY_BULLET.image == None:
            MY_BULLET.image = load_image('resource/Aft_resource/Fire_Myjet.png')
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
    sign = 0

    def __init__(self):
        self.image = load_image('resource/Aft_resource/My_Friend.png')
        self.image1 = load_image('resource/Aft_resource/My_Friend.png')
        self.A_x = -100
        self.A_y = -100
        self.B_x = +900
        self.B_y = -100
        pass

    def update(self):
        if self.sign % 2 == 1:
            if self.A_x >= my_jet.x-80:
                self.A_x -= 0.5
            elif self.A_x < my_jet.x-80:
                self.A_x += 0.5
            if self.A_y >= my_jet.y+70:
                self.A_y -= 0.5
            elif self.A_y < my_jet.y+70:
                self.A_y += 0.5
            if self.B_x >= my_jet.x+80:
                self.B_x -= 0.5
            elif self.B_x < my_jet.x+80:
                self.B_x += 0.5
            if self.B_y >= my_jet.y+70:
                self.B_y -= 0.5
            elif self.B_y < my_jet.y+70:
                self.B_y += 0.5
            pass
        elif self.sign % 2 == 0:
            if self.A_x != -100:
                self.A_x -= 1
            if self.A_y != -100:
                self.A_y -= 1
            if self.B_x != +900:
                self.B_x += 1
            if self.B_y != -100:
                self.B_y -= 1
            pass

    def draw(self):
        self.image.clip_draw(0, 0, 140, 120, self.A_x, self.A_y)
        self.image1.clip_draw(0, 0, 140, 120, self.B_x, self.B_y)
        pass

class ENEMY_JET:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet1.png')
        self.image2 = load_image('resource/Aft_resource/EnemyJet2.png')
        self.image3 = load_image('resource/Aft_resource/EnemyJet3.png')

        self.image4 = load_image('resource/Aft_resource/EnemyJet1.png')
        self.image5 = load_image('resource/Aft_resource/EnemyJet2.png')
        self.image6 = load_image('resource/Aft_resource/EnemyJet3.png')

        self.x1, self.y1 = random.randint(100, 700), random.randint(600, 800)
        self.x2, self.y2 = random.randint(100, 700), random.randint(600, 800)
        self.x3, self.y3 = random.randint(100, 700), random.randint(600, 800)

        self.x4, self.y4 = random.randint(100, 700), random.randint(900, 1000)
        self.x5, self.y5 = random.randint(100, 700), random.randint(900, 1000)
        self.x6, self.y6 = random.randint(100, 700), random.randint(900, 1000)
        pass

    def update(self):
        self.y1 -= 0.5
        self.y2 -= 0.5
        self.y3 -= 0.5
        self.y4 -= 0.5
        self.y5 -= 0.5
        self.y6 -= 0.5

        if self.y1 ==-100:
            self.x1, self.y1 = random.randint(100, 700), random.randint(600, 700)
        if self.y2 ==-100:
            self.x2, self.y2 = random.randint(100, 700), random.randint(600, 700)
        if self.y3 == -100:
            self.x3, self.y3 = random.randint(100, 700), random.randint(600, 700)
        if self.y4 == -100:
            self.x4, self.y4 = random.randint(100, 700), random.randint(900, 1000)
        if self.y5 == -100:
            self.x5, self.y5 = random.randint(100, 700), random.randint(900, 1000)
        if self.y6 == -100:
            self.x6, self.y6 = random.randint(100, 700), random.randint(900, 1000)
        pass

    def draw(self):
        self.image1.clip_draw(0, 0, 40, 80, self.x1, self.y1)
        self.image2.clip_draw(0, 0, 40, 50, self.x2, self.y2)
        self.image3.clip_draw(0, 0, 50, 50, self.x3, self.y3)
        self.image4.clip_draw(0, 0, 40, 80, self.x4, self.y4)
        self.image5.clip_draw(0, 0, 40, 50, self.x5, self.y5)
        self.image6.clip_draw(0, 0, 50, 50, self.x6, self.y6)
        pass

def enter():
    global my_jet, background, my_bullets, my_friend, enemy_jet
    my_jet = MY_JET()
    background = BACKGROUND()
    my_bullets = []
    my_friend = MY_FRIEND()
    enemy_jet = ENEMY_JET()

def exit():
    global my_jet, background, my_bullets, my_friend, enemy_jet
    del (my_jet)
    del (background)
    del (my_bullets)
    del (my_friend)
    del (enemy_jet)


def pause():
    pass


def resume():
    pass


def handle_events():
    global my_jet, my_bullets, my_friend
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
                MY_FRIEND.sign += 1

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
    my_friend.update()
    enemy_jet.update()
    pass


def draw():
    clear_canvas()
    background.draw()
    my_jet.draw()
    for bullet in my_bullets:
        bullet.draw()
    my_friend.draw()
    enemy_jet.draw()
    update_canvas()
