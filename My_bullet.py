from pico2d import *
import Game_Framework

import random
import time
import fly_high



PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm


RUN_SPEED_KMPH_MY_BULLET = 40  # km/hour
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

        self.fire_sound = load_wav('resource/Sound/188.WAV')
        self.fire_sound.set_volume(30)
        self.x = fly_high.my_jet.x
        self.y = fly_high.my_jet.y

        self.L_x = fly_high.my_jet.x
        self.L_y = fly_high.my_jet.y
        self.R_x = fly_high.my_jet.x
        self.R_y = fly_high.my_jet.y
        self.sign = 0

        pass

    def shoot(self):
        self.fire_sound.play()

    def update(self):
        if self.sign == 0:
            if self.bullet_dir == 1:
                self.L_x = fly_high.my_jet.x
                self.L_y = fly_high.my_jet.y + 30
                self.x, self.y = -10, -10
            elif self.bullet_dir == 2:
                self.R_x = fly_high.my_jet.x
                self.R_y = fly_high.my_jet.y + 30
                self.x, self.y = -10, -10
            elif self.bullet_dir == 0:
                self.x = fly_high.my_jet.x
                self.y = fly_high.my_jet.y + 35

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
            #draw_rectangle(*self.get_bb())
        elif self.bullet_dir == 2:
            self.image_right.clip_draw(0, 0, 14, 12, self.R_x, self.R_y)
            #draw_rectangle(*self.get_bb())
        else:
            self.image.clip_draw(0, 0, 10, 12, self.x, self.y)
            #draw_rectangle(*self.get_bb())
        pass