from pico2d import *
import Game_Framework

from pygame import mixer
import random
import time

PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm



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
class ENEMY_BULLET:
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