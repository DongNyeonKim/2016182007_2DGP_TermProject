from pico2d import *
import Game_Framework

import random
import time


PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm

RUN_SPEED_KMPH_ENEMY_JET_2 = 3  # km/hour
RUN_SPEED_MPM_ENEMY_JET_2 = (RUN_SPEED_KMPH_ENEMY_JET_2 * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_JET_2 = (RUN_SPEED_MPM_ENEMY_JET_2 / 60.0)
RUN_SPEED_PPS_ENEMY_JET_2 = (RUN_SPEED_MPS_ENEMY_JET_2 * PIXEL_PER_METER)

TIME_PER_ACTION_ENEMY_JET = 0.1
ACTION_PER_TIME_ENEMY_JET_EXPLODE = 0.1 / TIME_PER_ACTION_ENEMY_JET
FRAMES_PER_ACTION_ENEMY_JET = 5

# 적 전투기2(뚱뚱이)
class ENEMY_JET_2:

    def __init__(self):
        self.image1 = load_image('resource/Aft_resource/EnemyJet3.png')

        self.explode_ani1 = load_image('resource/Aft_resource/Explode-enemy.png')
        self.explode_sound = load_wav('resource/Sound/123.wav')
        self.explode_sound.set_volume(30)
        self.explode_frame = 0
        self.explode_check = 0

        self.x1, self.y1 = random.randint(50, 750), random.randint(600, 900)
        pass


    def explode(self):
        self.explode_sound.play()

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
            self.y1 -= RUN_SPEED_PPS_ENEMY_JET_2 * Game_Framework.frame_time

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
            #draw_rectangle(*self.get_bb())

        pass


RUN_SPEED_KMPH_ENEMY_BULLET = 5  # km/hour
RUN_SPEED_MPM_ENEMY_BULLET = (RUN_SPEED_KMPH_ENEMY_BULLET * 1000.0 / 60.0)
RUN_SPEED_MPS_ENEMY_BULLET = (RUN_SPEED_MPM_ENEMY_BULLET / 60.0)
RUN_SPEED_PPS_ENEMY_BULLET = (RUN_SPEED_MPS_ENEMY_BULLET * PIXEL_PER_METER)

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
            #draw_rectangle(*self.get_bb())
        if self.dir == 1:
            self.image_R.clip_draw(0, 0, 12, 12, self.R_x, self.R_y)
            #draw_rectangle(*self.get_bb())
        if self.dir == 2:
            self.image_L.clip_draw(0, 0, 12, 12, self.L_x, self.L_y)
            #draw_rectangle(*self.get_bb())
        pass

    pass