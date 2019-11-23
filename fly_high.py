from pico2d import *
import Game_Framework
import Title_state
import Gameover_state
from pygame import mixer
import random
import time

name = "Main_state"

Timer = 0
#적들 숫자 설정(난이도 설정)
Enemy1_quantity = 0
Enemy2_quantity = 0
Enemy3_quantity = 0

PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm
RUN_SPEED_KMPH_BACKGROUND = 30  # km/hour
RUN_SPEED_MPM_BACKGROUND = (RUN_SPEED_KMPH_BACKGROUND * 1000.0 / 60.0)
RUN_SPEED_MPS_BACKGROUND = (RUN_SPEED_MPM_BACKGROUND / 60.0)
RUN_SPEED_PPS_BACKGROUND = (RUN_SPEED_MPS_BACKGROUND * PIXEL_PER_METER)


# 배경화면
# background1, background2 가 y축으로 움직이면서 배경을 이어 보이게 만듦
class BACKGROUND:
    def __init__(self):
        self.background1 = load_image('resource/Aft_resource/background.png')
        self.background2 = load_image('resource/Aft_resource/background.png')
        self.background_x, self.background_y = 0, 0
        self.background1_move_y, self.background2_move_y = 0, 0
        self.a, self.b = 900, 300
        self.velocity = 0

    def update(self):
        self.velocity = int(RUN_SPEED_PPS_BACKGROUND * Game_Framework.frame_time)
        self.background1_move_y -= 2
        self.background2_move_y -= 2

        if self.a + self.background1_move_y <= -300:
            self.a = 900
            self.background1_move_y = 0

        if self.b + self.background2_move_y <= -300:
            self.b = 900
            self.background2_move_y = 0
        pass

    def draw(self):
        self.background1.clip_draw(0, 0, 800, 600, 800 // 2, self.a + self.background1_move_y)
        self.background2.clip_draw(0, 0, 800, 600, 800 // 2, self.b + self.background2_move_y)
        pass

class Cloud:
    def __init__(self):
        self.cloud = load_image('resource/Aft_resource/cloud.png')
        self.x, self.y = 200,200

        pass
    def update(self):
        self.x += 0.3
        if self.x > 700:
            self.x =0
            self.y=300
        pass
    def draw(self):
        self.cloud.clip_draw(0,0,400,250, self.x,self.y)
        pass

# JET Speed
RUN_SPEED_KMPH_JET = 10  # km/hour
RUN_SPEED_MPM_JET = (RUN_SPEED_KMPH_JET * 1000.0 / 60.0)
RUN_SPEED_MPS_JET = (RUN_SPEED_MPM_JET / 60.0)
RUN_SPEED_PPS_JET = (RUN_SPEED_MPS_JET * PIXEL_PER_METER)
# JET Action Speed
TIME_PER_ACTION_JET = 0.5
ACTION_PER_TIME_JET = 1.0 / TIME_PER_ACTION_JET
# 폭발시 애니메이션 속도
ACTION_PER_TIME_JET_EXPLODE = 0.1 / TIME_PER_ACTION_JET
FRAMES_PER_ACTION_JET = 6


# 내 전투기(케릭터)
class MY_JET:

    def __init__(self):
        self.image = load_image('resource/Aft_resource/jet21.png')
        self.explode_ani = load_image('resource/Aft_resource/MyJet_Explode.png')
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.frame = 0
        self.x, self.y = 400, 300
        self.move_x, self.move_y = 0, 0
        self.NowTime = 0

        self.explode_frame = 0
        self.explode_check = 0
        self.game_over_sign = 0
        pass

    def update(self):
        if self.explode_check == 1:
            # if Timer % 100 == 0:
            self.explode_frame = (
                                         self.explode_frame + FRAMES_PER_ACTION_JET * ACTION_PER_TIME_JET_EXPLODE * Game_Framework.frame_time) % 6
            if int(self.explode_frame) == 5:
                # 폭발 프레임이 끝나면 게임 오버스테이트로 이동
                self.game_over_sign = 1

        else:
            self.frame = (self.frame + FRAMES_PER_ACTION_JET * ACTION_PER_TIME_JET * Game_Framework.frame_time) % 6
            # 이동
            self.x += self.move_x * Game_Framework.frame_time
            self.y += self.move_y * Game_Framework.frame_time
            # 화면 충돌처리
            self.x = clamp(25, self.x, 800 - 25)
            self.y = clamp(25, self.y, 600 - 45)
            # print(self.x, self.y)
        pass

    def get_bb(self):
        return self.x - 17, self.y, self.x + 17, self.y + 40

    def draw(self):
        self.NowTime = time.time() - First_Time
        # print(self.NowTime)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % self.NowTime, (255, 255, 0))

        if self.explode_check == 1:
            self.explode_ani.clip_draw(int(self.explode_frame) * 40, 0, 40, 80, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 40, 0, 40, 80, self.x, self.y)
            draw_rectangle(*self.get_bb())
        pass


RUN_SPEED_KMPH_MY_BULLET = 100  # km/hour
RUN_SPEED_MPM_MY_BULLET = (RUN_SPEED_KMPH_MY_BULLET * 1000.0 / 60.0)
RUN_SPEED_MPS_MY_BULLET = (RUN_SPEED_MPM_MY_BULLET / 60.0)
RUN_SPEED_PPS_MY_BULLET = (RUN_SPEED_MPS_MY_BULLET * PIXEL_PER_METER)


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
                self.L_x -= RUN_SPEED_PPS_MY_BULLET * Game_Framework.frame_time
                self.L_y += RUN_SPEED_PPS_MY_BULLET * Game_Framework.frame_time
        elif self.bullet_dir == 2:
            if self.R_y != 610:
                self.R_x += RUN_SPEED_PPS_MY_BULLET * Game_Framework.frame_time
                self.R_y += RUN_SPEED_PPS_MY_BULLET * Game_Framework.frame_time
        elif self.bullet_dir == 0 and self.y != 610:
            self.y += RUN_SPEED_PPS_MY_BULLET * Game_Framework.frame_time

        pass

    def get_bb(self):
        if self.bullet_dir == 1:
            return self.L_x - 7, self.L_y - 6, self.L_x + 7, self.L_y + 6
        elif self.bullet_dir == 2:
            return self.R_x - 7, self.R_y - 6, self.R_x + 7, self.R_y + 6
        else:
            return self.x - 7, self.y - 6, self.x + 7, self.y + 6

    def draw(self):
        if self.bullet_dir == 1:
            self.image_left.clip_draw(0, 0, 14, 12, self.L_x, self.L_y)
            draw_rectangle(*self.get_bb())
        elif self.bullet_dir == 2:
            self.image_right.clip_draw(0, 0, 14, 12, self.R_x, self.R_y)
            draw_rectangle(*self.get_bb())
        else:
            self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
            draw_rectangle(*self.get_bb())
        pass


RUN_SPEED_KMPH_MY_FRIEND = 6  # km/hour
RUN_SPEED_MPM_MY_FRIEND = (RUN_SPEED_KMPH_MY_FRIEND * 1000.0 / 60.0)
RUN_SPEED_MPS_MY_FRIEND = (RUN_SPEED_MPM_MY_FRIEND / 60.0)
RUN_SPEED_PPS_MY_FRIEND = (RUN_SPEED_MPS_MY_FRIEND * PIXEL_PER_METER)


# 내 아군 전투기 A(왼쪽) B(오른쪽)
class MY_FRIEND:
    def __init__(self):
        self.image = load_image('resource/Aft_resource/My_Friend.png')
        self.image1 = load_image('resource/Aft_resource/My_Friend.png')
        self.A_x = -100
        self.A_y = -100
        self.B_x = 900
        self.B_y = -100
        self.ax = 0
        self.ay = 0
        self.bx = 0
        self.by = 0

        self.sign = 0
        pass

    def update(self):
        # sign은 아군 호출 여부
        if self.sign % 2 == 1:
            if self.A_x >= my_jet.x - 80:
                self.A_x -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.A_x < my_jet.x - 80:
                self.A_x += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.A_y >= my_jet.y + 70:
                self.A_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.A_y < my_jet.y + 70:
                self.A_y += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_x >= my_jet.x + 80:
                self.B_x -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.B_x < my_jet.x + 80:
                self.B_x += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_y >= my_jet.y + 70:
                self.B_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.B_y < my_jet.y + 70:
                self.B_y += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            pass

        elif self.sign % 2 == 0:
            if self.A_x != -100:
                self.A_x -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.A_y != -100:
                self.A_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_x != +900:
                self.B_x += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_y != -100:
                self.B_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            pass

    def draw(self):
        self.image.clip_draw(0, 0, 140, 120, self.A_x, self.A_y)
        self.image1.clip_draw(0, 0, 140, 120, self.B_x, self.B_y)
        pass


RUN_SPEED_KMPH_MY_FRIEND_BULLET = 30  # km/hour
RUN_SPEED_MPM_MY_FRIEND_BULLET = (RUN_SPEED_KMPH_MY_FRIEND_BULLET * 1000.0 / 60.0)
RUN_SPEED_MPS_MY_FRIEND_BULLET = (RUN_SPEED_MPM_MY_FRIEND_BULLET / 60.0)
RUN_SPEED_PPS_MY_FRIEND_BULLET = (RUN_SPEED_MPS_MY_FRIEND_BULLET * PIXEL_PER_METER)


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
            self.a_y += RUN_SPEED_PPS_MY_FRIEND_BULLET * Game_Framework.frame_time

        if self.bullet_dir == 2 and self.b_y != 650:
            self.b_y += RUN_SPEED_PPS_MY_FRIEND_BULLET * Game_Framework.frame_time

        pass

    def get_bb(self):
        if self.bullet_dir == 1:
            return self.a_x - 10, self.a_y - 15, self.a_x + 10, self.a_y + 15
        elif self.bullet_dir == 2:
            return self.b_x - 10, self.b_y - 15, self.b_x + 10, self.b_y + 15

    def draw(self):
        if self.bullet_dir == 1:
            self.image.clip_draw(0, 0, 20, 30, self.a_x, self.a_y)
            draw_rectangle(*self.get_bb())
        if self.bullet_dir == 2:
            self.image.clip_draw(0, 0, 20, 30, self.b_x, self.b_y)
            draw_rectangle(*self.get_bb())
        pass


RUN_SPEED_KMPH_ENEMY_JET = 3  # km/hour
RUN_SPEED_MPM_ENEMY_JET = (RUN_SPEED_KMPH_ENEMY_JET * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_JET = (RUN_SPEED_MPM_ENEMY_JET / 60.0)
RUN_SPEED_PPS_ENEMY_JET = (RUN_SPEED_MPS_ENEMY_JET * PIXEL_PER_METER)

TIME_PER_ACTION_ENEMY_JET = 0.1
ACTION_PER_TIME_ENEMY_JET_EXPLODE = 0.1 / TIME_PER_ACTION_ENEMY_JET
FRAMES_PER_ACTION_ENEMY_JET = 5


# 적 전투기 1 (레드)
class ENEMY_JET:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet1.png')

        self.explode_ani1 = load_image('resource/Aft_resource/Explode-enemy.png')

        self.explode_frame = 0
        self.explode_check = 0

        self.x1, self.y1 = random.randint(100, 700), random.randint(600, 800)
        pass

    def update(self):
        # 적이 죽으면 explode_check=1 이 되고 폭발 애니메이션 실행 후 초기화 한 뒤 다시 생성
        if self.explode_check == 1:
            self.explode_frame = (
                                         self.explode_frame + FRAMES_PER_ACTION_ENEMY_JET * ACTION_PER_TIME_ENEMY_JET_EXPLODE * Game_Framework.frame_time) % 5
            if int(self.explode_frame) == 4:
                self.explode_check = 0
                self.explode_frame = 0
                self.x1, self.y1 = random.randint(100, 700), random.randint(600, 800)
        # 살아 있는 경우 계속 앞으로 전진
        else:
            self.y1 -= RUN_SPEED_PPS_ENEMY_JET * Game_Framework.frame_time

        # 맵 끝까지 오면 다시 위로 초기화
        if self.y1 <= -100:
            self.x1, self.y1 = random.randint(100, 700), random.randint(600, 700)

        pass

    def get_bb(self):
        return self.x1 - 15, self.y1 - 35, self.x1 + 15, self.y1 + 35

    def draw(self):
        if self.explode_check == 1:
            self.explode_ani1.clip_draw(int(self.explode_frame) * 40, 0, 40, 80, self.x1, self.y1)
        else:
            self.image1.clip_draw(0, 0, 40, 80, self.x1, self.y1)
            draw_rectangle(*self.get_bb())

        pass


RUN_SPEED_KMPH_ENEMY_BULLET = 5  # km/hour
RUN_SPEED_MPM_ENEMY_BULLET = (RUN_SPEED_KMPH_ENEMY_BULLET * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_BULLET = (RUN_SPEED_MPM_ENEMY_BULLET / 60.0)
RUN_SPEED_PPS_ENEMY_BULLET = (RUN_SPEED_MPS_ENEMY_BULLET * PIXEL_PER_METER)


# 적 전투기 1 (레드) 총알
class ENEMY_BULLET():
    image = None

    def __init__(self):
        if ENEMY_BULLET.image is None:
            ENEMY_BULLET.image = load_image('resource/Aft_resource/Fire_Enemy.png')

        self.x = 0
        self.y = 0
        pass

    def update(self):
        self.y -= RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
        pass

    def get_bb(self):
        return self.x - 5, self.y - 6, self.x + 5, self.y + 6

    def draw(self):
        self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
        draw_rectangle(*self.get_bb())
        pass

    pass


RUN_SPEED_KMPH_ENEMY_JET_2 = 3  # km/hour
RUN_SPEED_MPM_ENEMY_JET_2 = (RUN_SPEED_KMPH_ENEMY_JET_2 * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_JET_2 = (RUN_SPEED_MPM_ENEMY_JET_2 / 60.0)
RUN_SPEED_PPS_ENEMY_JET_2 = (RUN_SPEED_MPS_ENEMY_JET_2 * PIXEL_PER_METER)


# 적 전투기2(뚱뚱이)
class ENEMY_JET_2:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet3.png')

        self.explode_ani1 = load_image('resource/Aft_resource/Explode-enemy.png')

        self.explode_frame = 0
        self.explode_check = 0

        self.x1, self.y1 = random.randint(50, 750), random.randint(600, 900)
        pass

    def update(self):
        # 적이 죽으면 explode_check=1 이 되고 폭발 애니메이션 실행 후 초기화 한 뒤 다시 생성
        if self.explode_check == 1:
            self.explode_frame = (
                                         self.explode_frame + FRAMES_PER_ACTION_ENEMY_JET * ACTION_PER_TIME_ENEMY_JET_EXPLODE * Game_Framework.frame_time) % 5
            if int(self.explode_frame) == 4:
                self.explode_check = 0
                self.explode_frame = 0
                self.x1, self.y1 = random.randint(50, 750), random.randint(600, 900)
        # 살아 있는 경우 계속 앞으로 전진
        else:
            self.y1 -= RUN_SPEED_PPS_ENEMY_JET * Game_Framework.frame_time

        # 맵 끝까지 오면 다시 위로 초기화
        if self.y1 <= -100:
            self.x1, self.y1 = random.randint(50, 750), random.randint(600, 900)

        pass

    def get_bb(self):
        return self.x1 - 25, self.y1 - 25, self.x1 + 25, self.y1 + 25

    def draw(self):
        if self.explode_check == 1:
            self.explode_ani1.clip_draw(int(self.explode_frame) * 40, 0, 40, 80, self.x1, self.y1)
        else:
            self.image1.clip_draw(0, 0, 50, 50, self.x1, self.y1)
            draw_rectangle(*self.get_bb())

        pass


# 적 전투기 2 (뚱뚱이) 총알
class ENEMY_BULLET_2:
    image = None
    image_R = None
    image_L = None

    def __init__(self):
        if ENEMY_BULLET_2.image is None:
            ENEMY_BULLET_2.image = load_image('resource/Aft_resource/Fire_Enemy_1.png')
        if ENEMY_BULLET_2.image_R is None:
            ENEMY_BULLET_2.image_R = load_image('resource/Aft_resource/Fire_Enemy_1_R.png')
        if ENEMY_BULLET_2.image_L is None:
            ENEMY_BULLET_2.image_L = load_image('resource/Aft_resource/Fire_Enemy_1_L.png')

        self.dir = 0

        self.x = 0
        self.y = 0
        self.R_x = 0
        self.R_y = 0
        self.L_x = 0
        self.L_y = 0
        pass

    def update(self):
        if self.dir == 0:
            self.y -= RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
        if self.dir == 1:
            self.R_y -= RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
            self.R_x += RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
        if self.dir == 2:
            self.L_y -= RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
            self.L_x -= RUN_SPEED_PPS_ENEMY_BULLET * Game_Framework.frame_time
        pass

    def get_bb(self):
        if self.dir == 0:
            return self.x - 5, self.y - 6, self.x + 5, self.y + 6
        elif self.dir == 1:
            return self.R_x - 6, self.R_y - 6, self.R_x + 6, self.R_y + 6
        elif self.dir == 2:
            return self.L_x - 6, self.L_y - 6, self.L_x + 6, self.L_y + 6

    def draw(self):
        if self.dir == 0:
            self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
            draw_rectangle(*self.get_bb())
        if self.dir == 1:
            self.image_R.clip_draw(0, 0, 12, 12, self.R_x, self.R_y)
            draw_rectangle(*self.get_bb())
        if self.dir == 2:
            self.image_L.clip_draw(0, 0, 12, 12, self.L_x, self.L_y)
            draw_rectangle(*self.get_bb())
        pass

    pass


RUN_SPEED_KMPH_ENEMY_JET_2 = 3  # km/hour
RUN_SPEED_MPM_ENEMY_JET_2 = (RUN_SPEED_KMPH_ENEMY_JET_2 * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_JET_2 = (RUN_SPEED_MPM_ENEMY_JET_2 / 60.0)
RUN_SPEED_PPS_ENEMY_JET_2 = (RUN_SPEED_MPS_ENEMY_JET_2 * PIXEL_PER_METER)


# 적 전투기3(라이트형제)
class ENEMY_JET_3:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet4.png')

        self.explode_ani1 = load_image('resource/Aft_resource/Explode-enemy.png')

        self.explode_frame = 0
        self.explode_check = 0

        self.x1, self.y1 = random.randint(-100, 0), random.randint(50, 550)
        pass

    def update(self):
        # 적이 죽으면 explode_check=1 이 되고 폭발 애니메이션 실행 후 초기화 한 뒤 다시 생성
        if self.explode_check == 1:
            self.explode_frame = (
                                             self.explode_frame + FRAMES_PER_ACTION_ENEMY_JET * ACTION_PER_TIME_ENEMY_JET_EXPLODE * Game_Framework.frame_time) % 5
            if int(self.explode_frame) == 4:
                self.explode_check = 0
                self.explode_frame = 0
                self.x1, self.y1 = random.randint(-100, 0), random.randint(300, 550)
        # 살아 있는 경우 계속 앞으로 전진
        else:
            self.x1 += RUN_SPEED_PPS_ENEMY_JET * Game_Framework.frame_time

        # 맵 끝까지 오면 다시 위로 초기화
        if self.x1 >= 900:
            self.x1, self.y1 = random.randint(-100, 0), random.randint(300, 550)

        pass

    def get_bb(self):
        return self.x1 - 20, self.y1 - 15, self.x1 + 20, self.y1 + 15

    def draw(self):
        if self.explode_check == 1:
            self.explode_ani1.clip_draw(int(self.explode_frame) * 40, 0, 40, 80, self.x1, self.y1)
        else:
            self.image1.clip_draw(0, 0, 40, 30, self.x1, self.y1)
            draw_rectangle(*self.get_bb())

        pass


# 충돌처리
def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global background, my_jet, my_bullets, my_friend, my_friend_bullets, enemy_jets, enemy_bullets, enemy_jets_2, enemy_jets_3, First_Time, Timer, cloud
    background = BACKGROUND()

    my_jet = MY_JET()
    my_bullets = []

    my_friend = MY_FRIEND()
    my_friend_bullets = []

    enemy_jets = [ENEMY_JET() for i in range(Enemy1_quantity)]
    enemy_jets_2 = [ENEMY_JET_2() for i in range(Enemy2_quantity)]
    enemy_jets_3 = [ENEMY_JET_3() for i in range(Enemy3_quantity)]

    enemy_bullets = []

    First_Time = 0.0
    cloud = Cloud()

def exit():
    global my_jet, background, my_bullets, my_friend, my_friend_bullets, enemy_jets, enemy_jets_2, enemy_jets_3
    del my_jet
    del background
    del my_bullets
    del my_friend
    del enemy_jets
    del enemy_jets_2
    del enemy_jets_3
    del my_friend_bullets


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Game_Framework.quit()

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                Game_Framework.change_state(Title_state)
            elif event.key == SDLK_UP:
                my_jet.move_y += RUN_SPEED_PPS_JET
            elif event.key == SDLK_DOWN:
                my_jet.move_y -= RUN_SPEED_PPS_JET
            elif event.key == SDLK_RIGHT:
                my_jet.move_x += RUN_SPEED_PPS_JET
            elif event.key == SDLK_LEFT:
                my_jet.move_x -= RUN_SPEED_PPS_JET
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

            elif event.key == SDLK_a:
                my_friend.sign += 1
            elif event.key == SDLK_s:
                Gameover_state.Time = my_jet.NowTime
                Game_Framework.change_state(Gameover_state)

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP:
                my_jet.move_y -= RUN_SPEED_PPS_JET
            elif event.key == SDLK_DOWN:
                my_jet.move_y += RUN_SPEED_PPS_JET
            elif event.key == SDLK_RIGHT:
                my_jet.move_x -= RUN_SPEED_PPS_JET
            elif event.key == SDLK_LEFT:
                my_jet.move_x += RUN_SPEED_PPS_JET
            elif event.key == SDLK_z:
                pass
            elif event.key == SDLK_x:
                pass
            elif event.key == SDLK_a:
                pass
            elif event.key == SDLK_s:
                pass


def update():
    global Timer, enemy_bullet, First_Time
    background.update()
    cloud.update()
    my_jet.update()
    if First_Time == 0:
        First_Time = time.time()
    # 내 총알의 충돌처리
    for bullet in my_bullets:
        bullet.update()
        # print(bullet.x, bullet.y)
        # 적군과 충돌처리
        for enemy in enemy_jets:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        for enemy in enemy_jets_2:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        for enemy in enemy_jets_3:
            if collide(enemy, bullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if bullet in my_bullets:
                    my_bullets.remove(bullet)
        # 화면을 넘어갈 경우 삭제
        if bullet.y > 700 or bullet.L_y > 700 or bullet.R_y > 700:
            if bullet in my_bullets:
                my_bullets.remove(bullet)

    my_friend.update()

    # 일정 시간마다 아군 총알 발사
    Timer += 1
    if Timer % 50 == 0:
        sbullet = MY_FRIEND_BULLET()
        sbullet.bullet_dir = 1
        my_friend_bullets.append(sbullet)
        sbullet = MY_FRIEND_BULLET()
        sbullet.bullet_dir = 2
        my_friend_bullets.append(sbullet)

    # 아군 총알의 충돌처리
    for sbullet in my_friend_bullets:
        sbullet.update()
        if sbullet.a_y > 700 or sbullet.b_y > 700:
            if sbullet in my_friend_bullets:
                my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)
        for enemy in enemy_jets_2:
            if collide(enemy, sbullet) and enemy.explode_check == 0:
                enemy.explode_check = 1
                if sbullet in my_friend_bullets:
                    my_friend_bullets.remove(sbullet)

    # 적군 업데이트
    for enemy in enemy_jets:
        enemy.update()
        if Timer % random.randint(50, 100) == 0 and enemy.explode_check == 0:
            enemy_bullet = ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    for enemy in enemy_jets_2:
        enemy.update()
        if Timer % random.randint(100, 200) == 0 and enemy.explode_check == 0:
            enemy_bullet = ENEMY_BULLET_2()
            enemy_bullet.dir = random.randint(0, 2)
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullet.R_x = enemy.x1
            enemy_bullet.R_y = enemy.y1 - 25
            enemy_bullet.L_x = enemy.x1
            enemy_bullet.L_y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    for enemy in enemy_jets_3:
        enemy.update()
        if Timer % random.randint(50, 100) == 0 and enemy.explode_check == 0:
            enemy_bullet = ENEMY_BULLET()
            enemy_bullet.x = enemy.x1
            enemy_bullet.y = enemy.y1 - 25
            enemy_bullets.append(enemy_bullet)
        if collide(my_jet, enemy) and my_jet.explode_check == 0:
            my_jet.explode_check = 1
            enemy.explode_check = 1
    # 적군 총알 충돌처리
    for enemy_bullet in enemy_bullets:
        enemy_bullet.update()
        if collide(my_jet, enemy_bullet) and my_jet.explode_check == 0:
            my_jet.explode_check = 1
            if enemy_bullet in enemy_bullets:
                enemy_bullets.remove(enemy_bullet)
        if enemy_bullet.y < -100:
            if enemy_bullet in enemy_bullets:
                enemy_bullets.remove(enemy_bullet)

    # 내 전투기기가 폭발하면 게임 종료
    if my_jet.game_over_sign == 1:
        Gameover_state.Time = my_jet.NowTime
        Game_Framework.change_state(Gameover_state)
    pass


def draw():
    clear_canvas()
    background.draw()

    my_jet.draw()
    for bullet in my_bullets:
        bullet.draw()
    my_friend.draw()

    for bullet in my_friend_bullets:
        bullet.draw()

    for enemy in enemy_jets:
        enemy.draw()

    for bullet in enemy_bullets:
        bullet.draw()

    for enemy in enemy_jets_2:
        enemy.draw()

    for enemy in enemy_jets_3:
        enemy.draw()
    cloud.draw()
    update_canvas()
