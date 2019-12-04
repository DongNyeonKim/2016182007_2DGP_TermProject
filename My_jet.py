from pico2d import *
import Game_Framework

from pygame import mixer
import random
import time

PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm


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
        self.explode_sound = load_wav('resource/Sound/Self.wav')
        self.explode_sound.set_volume(70)
        self.font = load_font('resource/ENCR10B.TTF', 16)
        self.frame = 0
        self.x, self.y = 400, 300
        self.move_x, self.move_y = 0, 0

        self.explode_frame = 0
        self.explode_check = 0
        self.game_over_sign = 0
        self.no_die = 1
        pass

    def explode(self):
        self.explode_sound.play()

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
        if self.explode_check == 1:
            self.explode_ani.clip_draw(int(self.explode_frame) * 40, 0, 40, 80, self.x, self.y)
        else:
            self.image.clip_draw(int(self.frame) * 40, 0, 40, 80, self.x, self.y)
            draw_rectangle(*self.get_bb())
        pass



