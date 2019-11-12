from pico2d import *
import Game_Framework
import Title_state
import Gameover_state
from pygame import mixer
import random

name = "Main_state"

# 없어도 되나? ㅅㅂ
# background = None
# my_jet = None
# my_bullets = None
# my_friend = None
# my_friend_bullets = None
# enemy_jet = None
# enemy_jets = None
Timer = 0



# 배경화면
# background1, background2 가 y축으로 움직이면서 배경을 이어 보이게 만듦
class BACKGROUND:
    def __init__(self):
        self.background1 = load_image('resource/Aft_resource/background.png')
        self.background2 = load_image('resource/Aft_resource/background.png')
        self.background_x, self.background_y = 0, 0
        self.background1_move_y, self.background2_move_y = 0, 0
        self.a, self.b = 900, 300

    def update(self):
        self.background1_move_y -= 2
        self.background2_move_y -= 2

        if self.a + self.background1_move_y == -300:
            self.a = 900
            self.background1_move_y = 0

        if self.b + self.background2_move_y == -300:
            self.b = 900
            self.background2_move_y = 0
        pass

    def draw(self):
        self.background1.clip_draw(0, 0, 800, 600, 800 // 2, self.a + self.background1_move_y)
        self.background2.clip_draw(0, 0, 800, 600, 800 // 2, self.b + self.background2_move_y)
        pass

#JET Speed
PIXEL_PER_METER = (10.0/0.1)    # 10pixel 10cm
RUN_SPEED_KMPH = 10.0  # km/hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0/60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
#JET Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0/ TIME_PER_ACTION
FRAMES_PER_ACTION = 6

# 내 전투기(케릭터)
class MY_JET:
    def __init__(self):
        self.image = load_image('resource/Aft_resource/jet21.png')
        self.frame = 0
        self.x, self.y = 400, 300
        self.move_x, self.move_y = 0, 0
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * Game_Framework.frame_time) % 6
        # 이동
        self.x += self.move_x * Game_Framework.frame_time
        self.y += self.move_y * Game_Framework.frame_time
        # 화면 충돌처리
        self.x = clamp(25, self.x, 800 - 25)
        self.y = clamp(25, self.y, 600 - 45)
        # print(self.x, self.y)
        pass

    def draw(self):
        self.image.clip_draw(int(self.frame) * 40, 0, 40, 80, self.x, self.y)
        pass


# 내 전투기 총알
class MY_BULLET:
    image = None
    image_left = None
    image_right = None

    def __init__(self):
        if MY_BULLET.image is None:
            MY_BULLET.image = load_image('resource/Aft_resource/Fire_Myjet.png')
        if MY_BULLET.image_left is None:
            MY_BULLET.image_left = load_image('resource/Aft_resource/my_bullet_left.png')
        if MY_BULLET.image_right is None:
            MY_BULLET.image_right = load_image('resource/Aft_resource/my_bullet_right.png')
        self.bullet_dir = 0

        self.x = my_jet.x
        self.y = my_jet.y

        self.L_x = my_jet.x
        self.L_y = my_jet.y
        self.R_x = my_jet.x
        self.R_y = my_jet.y
        self.sign = 0

        pass

    def update(self):
        if self.sign == 0:
            if self.bullet_dir == 1:
                self.L_x = my_jet.x
                self.L_y = my_jet.y + 30
                self.x, self.y = -10, -10
            elif self.bullet_dir == 2:
                self.R_x = my_jet.x
                self.R_y = my_jet.y + 30
                self.x, self.y = -10, -10
            elif self.bullet_dir == 0:
                self.x = my_jet.x
                self.y = my_jet.y + 35

            self.sign = 1

        if self.bullet_dir == 1:
            if self.L_y != 610:
                self.L_x -= 1
                self.L_y += 1
        elif self.bullet_dir == 2:
            if self.R_y != 610:
                self.R_x += 1
                self.R_y += 1
        elif self.bullet_dir == 0 and self.y != 610:
            self.y += 1

        pass

    def draw(self):
        if self.bullet_dir == 1:
            self.image_left.clip_draw(0, 0, 14, 12, self.L_x, self.L_y)
        elif self.bullet_dir == 2:
            self.image_right.clip_draw(0, 0, 14, 12, self.R_x, self.R_y)
        else:
            self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
        pass


# 내 아군 전투기 A(왼쪽) B(오른쪽)
class MY_FRIEND:
    def __init__(self):
        self.image = load_image('resource/Aft_resource/My_Friend.png')
        self.image1 = load_image('resource/Aft_resource/My_Friend.png')
        self.A_x = -100
        self.A_y = -100
        self.B_x = +900
        self.B_y = -100
        self.sign = 0
        pass

    def update(self):
        # sign은 아군 호출 여부
        if self.sign % 2 == 1:
            if self.A_x >= my_jet.x - 80:
                self.A_x -= 0.5
            elif self.A_x < my_jet.x - 80:
                self.A_x += 0.5
            if self.A_y >= my_jet.y + 70:
                self.A_y -= 0.5
            elif self.A_y < my_jet.y + 70:
                self.A_y += 0.5
            if self.B_x >= my_jet.x + 80:
                self.B_x -= 0.5
            elif self.B_x < my_jet.x + 80:
                self.B_x += 0.5
            if self.B_y >= my_jet.y + 70:
                self.B_y -= 0.5
            elif self.B_y < my_jet.y + 70:
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


# 아군 전투기 총알
class MY_FRIEND_BULLET:
    image = None

    def __init__(self):
        if MY_FRIEND_BULLET.image is None:
            MY_FRIEND_BULLET.image = load_image('resource/Aft_resource/Fire_MyFriend.png')
        self.a_x = my_friend.A_x
        self.a_y = my_friend.A_y
        self.b_x = my_friend.B_x
        self.b_y = my_friend.B_y
        self.bullet_dir = 0
        self.sign = 0
        pass

    def update(self):
        if self.sign == 0:
            if self.bullet_dir == 1:
                self.a_x = my_friend.A_x
                self.a_y = my_friend.A_y + 60
            if self.bullet_dir == 2:
                self.b_x = my_friend.B_x
                self.b_y = my_friend.B_y + 60
            self.sign = 1

        if self.bullet_dir == 1 and self.a_y != 650:
            self.a_y += 1

        if self.bullet_dir == 2 and self.b_y != 650:
            self.b_y += 1

        pass

    def draw(self):
        if self.bullet_dir == 1:
            self.image.clip_draw(0, 0, 20, 30, self.a_x, self.a_y)
        if self.bullet_dir == 2:
            self.image.clip_draw(0, 0, 20, 30, self.b_x, self.b_y)
        pass


class ENEMY_JET:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet1.png')

        self.explode_ani1 = load_image('resource/Aft_resource/Explode-enemy.png')

        self.explode_frame = 0
        self.explode_check = 0
        # self.image2 = load_image('resource/Aft_resource/EnemyJet2.png')
        # self.image3 = load_image('resource/Aft_resource/EnemyJet3.png')
        #
        # self.image4 = load_image('resource/Aft_resource/EnemyJet1.png')
        # self.image5 = load_image('resource/Aft_resource/EnemyJet2.png')
        # self.image6 = load_image('resource/Aft_resource/EnemyJet3.png')
        #
        # self.image7 = load_image('resource/Aft_resource/EnemyJet4.png')
        # self.image8 = load_image('resource/Aft_resource/EnemyJet4.png')

        self.x1, self.y1 = random.randint(100, 700), random.randint(600, 800)
        # self.x2, self.y2 = random.randint(100, 700), random.randint(600, 800)
        # self.x3, self.y3 = random.randint(100, 700), random.randint(600, 800)
        #
        # self.x4, self.y4 = random.randint(100, 700), random.randint(900, 1000)
        # self.x5, self.y5 = random.randint(100, 700), random.randint(900, 1000)
        # self.x6, self.y6 = random.randint(100, 700), random.randint(900, 1000)
        # self.x7, self.y7 = random.randint(-100,0), random.randint(300,600)
        # self.x8, self.y8 = random.randint(800, 900), random.randint(300, 600)
        pass

    def update(self):
        # 적이 죽으면 explode_check=1 이 되고 폭발 애니메이션 실행 후 초기화 한 뒤 다시 생성
        if self.explode_check == 1:
            if Timer % 100 == 0:
                self.explode_frame += 1
            if self.explode_frame == 5:
                self.explode_check = 0
                self.explode_frame = 0
                self.x1, self.y1 = random.randint(100, 700), random.randint(600, 800)
        # 살아 있는 경우 계속 앞으로 전진
        else:
            self.y1 -= 0.5
        # self.y2 -= 0.5
        # self.y3 -= 0.5
        # self.y4 -= 0.5
        # self.y5 -= 0.5
        # self.y6 -= 0.5
        #
        # self.x7 += 0.5
        # self.x8 -= 0.5

        # 맵 끝까지 오면 다시 위로 초기화
        if self.y1 == -100:
            self.x1, self.y1 = random.randint(100, 700), random.randint(600, 700)
        # if self.y2 ==-100:
        #     self.x2, self.y2 = random.randint(100, 700), random.randint(600, 700)
        # if self.y3 == -100:
        #     self.x3, self.y3 = random.randint(100, 700), random.randint(600, 700)
        # if self.y4 == -100:
        #     self.x4, self.y4 = random.randint(100, 700), random.randint(900, 1000)
        # if self.y5 == -100:
        #     self.x5, self.y5 = random.randint(100, 700), random.randint(900, 1000)
        # if self.y6 == -100:
        #     self.x6, self.y6 = random.randint(100, 700), random.randint(900, 1000)
        # if self.x7 == 900:
        #     self.x7, self.y7 = random.randint(-100, 0), random.randint(300, 600)
        # if self.x8 == -100:
        #     self.x8, self.y8 = random.randint(800, 900), random.randint(300, 600)
        pass

    def draw(self):
        if self.explode_check == 1:
            self.explode_ani1.clip_draw(self.explode_frame * 40, 0, 40, 80, self.x1, self.y1)
        else:
            self.image1.clip_draw(0, 0, 40, 80, self.x1, self.y1)

        # self.image2.clip_draw(0, 0, 40, 50, self.x2, self.y2)
        # self.image3.clip_draw(0, 0, 50, 50, self.x3, self.y3)
        # self.image4.clip_draw(0, 0, 40, 80, self.x4, self.y4)
        # self.image5.clip_draw(0, 0, 40, 50, self.x5, self.y5)
        # self.image6.clip_draw(0, 0, 50, 50, self.x6, self.y6)
        # self.image7.clip_draw(0, 0, 40, 30, self.x7, self.y7)
        # self.image8.clip_draw(0, 0, 40, 30, self.x8, self.y8)
        pass


class ENEMY_BULLET():
    image = None
    def __init__(self):
        if ENEMY_BULLET.image is None:
            ENEMY_BULLET.image = load_image('resource/Aft_resource/Fire_Enemy.png')

        self.x = 0
        self.y = 0
        pass
    def update(self):
        self.y -= 1
        pass
    def draw(self):
        self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
        pass

    pass


def enter():
    global background, my_jet, my_bullets, my_friend, my_friend_bullets, enemy_jets, Timer, enemy_bullets
    background = BACKGROUND()

    my_jet = MY_JET()
    my_bullets = []

    my_friend = MY_FRIEND()
    my_friend_bullets = []

    enemy_jets = [ENEMY_JET() for i in range(10)]
    enemy_bullets = []


def exit():
    global my_jet, background, my_bullets, my_friend, my_friend_bullets, enemy_jets
    del my_jet
    del background
    del my_bullets
    del my_friend
    del enemy_jets
    del my_friend_bullets


def pause():
    pass


def resume():
    pass


def handle_events():
    # global my_jet, my_bullets, my_friend
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_Framework.change_state(Title_state)
            elif event.key == SDLK_UP:
                my_jet.move_y += RUN_SPEED_PPS
            elif event.key == SDLK_DOWN:
                my_jet.move_y -= RUN_SPEED_PPS
            elif event.key == SDLK_RIGHT:
                my_jet.move_x += RUN_SPEED_PPS
            elif event.key == SDLK_LEFT:
                my_jet.move_x -= RUN_SPEED_PPS
            elif event.key == SDLK_z:
                bullet = MY_BULLET()
                my_bullets.append(bullet)
            elif event.key == SDLK_x:
                bullet = MY_BULLET()
                bullet.bullet_dir = 1
                my_bullets.append(bullet)
                bullet = MY_BULLET()
                bullet.bullet_dir = 2
                my_bullets.append(bullet)
                pass

                # mixer.music.play()
            elif event.key == SDLK_a:
                my_friend.sign += 1
            elif event.key == SDLK_s:
                Game_Framework.change_state(Gameover_state)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                my_jet.move_y -= RUN_SPEED_PPS
            elif event.key == SDLK_DOWN:
                my_jet.move_y += RUN_SPEED_PPS
            elif event.key == SDLK_RIGHT:
                my_jet.move_x -= RUN_SPEED_PPS
            elif event.key == SDLK_LEFT:
                my_jet.move_x += RUN_SPEED_PPS
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_x:
                pass
            elif event.key == SDLK_a:
                pass
            elif event.key == SDLK_s:
                pass


def update():
    # global Timer, enemy_jet
    global Timer, enemy_bullet
    background.update()
    my_jet.update()

    # 내 총알의 충돌처리
    for bullet in my_bullets:
        bullet.update()
        print(bullet.x, bullet.y)
        # 적군과 충돌처리
        for enemy in enemy_jets:
            if enemy.y1 + 10 >= bullet.y >= enemy.y1 - 10 and enemy.x1 + 10 >= bullet.x >= enemy.x1 - 10 or enemy.y1 + 10 >= bullet.L_y >= enemy.y1 - 10 and enemy.x1 + 10 >= bullet.L_x >= enemy.x1 - 10 or enemy.y1 + 10 >= bullet.R_y >= enemy.y1 - 10 and enemy.x1 + 10 >= bullet.R_x >= enemy.x1 - 10:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        # 화면을 넘어갈 경우 삭제
        if bullet.y > 500 or bullet.L_y > 500 or bullet.R_y > 500:
            if bullet in my_bullets:
                my_bullets.remove(bullet)

    my_friend.update()

    # 일정 시간마다 아군 총알 발사
    Timer += 1
    if Timer % 100 == 0:
        sbullet = MY_FRIEND_BULLET()
        sbullet.bullet_dir = 1
        my_friend_bullets.append(sbullet)
        sbullet = MY_FRIEND_BULLET()
        sbullet.bullet_dir = 2
        my_friend_bullets.append(sbullet)

    # 아군 총알의 충돌처리
    for sbullet in my_friend_bullets:
        sbullet.update()
        if sbullet.a_y > 500 or sbullet.b_y > 500:
            if sbullet in my_friend_bullets:
                my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets:
            if enemy.y1 + 10 >= sbullet.a_y >= enemy.y1 - 10 and enemy.x1 + 10 >= sbullet.a_x >= enemy.x1 - 10 or enemy.y1 + 10 >= sbullet.b_y >= enemy.y1 - 10 and enemy.x1 + 10 >= sbullet.b_x >= enemy.x1 - 10:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)

    # 적군 업데이트
    for enemy in enemy_jets:
        enemy.update()
        if Timer % random.randint(100, 200) == 0:
            enemy_bullet = ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1
            enemy_bullets.append(enemy_bullet)


    for enemy_bullet in enemy_bullets:
        enemy_bullet.update()
        if enemy_bullet.y < 100:
            enemy_bullets.remove(enemy_bullet)


    pass


def draw():
    clear_canvas()
    background.draw()
    my_jet.draw()
    for bullet in my_bullets:
        bullet.draw()
    my_friend.draw()
    for sbullet in my_friend_bullets:
        sbullet.draw()

    for enemy in enemy_jets:
        enemy.draw()

    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw()

    update_canvas()
