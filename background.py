from pico2d import *
import Game_Framework

from pygame import mixer
import random
import time


PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm
RUN_SPEED_KMPH_BACKGROUND = 30  # km/hour
RUN_SPEED_MPM_BACKGROUND = (RUN_SPEED_KMPH_BACKGROUND * 1000.0 / 60.0)
RUN_SPEED_MPS_BACKGROUND = (RUN_SPEED_MPM_BACKGROUND / 60.0)
RUN_SPEED_PPS_BACKGROUND = (RUN_SPEED_MPS_BACKGROUND * PIXEL_PER_METER)

# 배경화면 8m x 6m
# background1, background2 가 y축으로 움직이면서 배경을 이어 보이게 만듦
class BACKGROUND:
    def __init__(self):
        self.bgm = load_music('resource/Sound/aaa.mp3')
        self.bgm.set_volume(100)
        self.bgm.repeat_play()
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