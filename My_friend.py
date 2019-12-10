from pico2d import *
import Game_Framework

import random
import time
import fly_high


PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm


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
            if self.A_x >= fly_high.my_jet.x - 80:
                self.A_x -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.A_x < fly_high.my_jet.x - 80:
                self.A_x += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.A_y >= fly_high.my_jet.y + 70:
                self.A_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.A_y < fly_high.my_jet.y + 70:
                self.A_y += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_x >= fly_high.my_jet.x + 80:
                self.B_x -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.B_x < fly_high.my_jet.x + 80:
                self.B_x += RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            if self.B_y >= fly_high.my_jet.y + 70:
                self.B_y -= RUN_SPEED_PPS_MY_FRIEND * Game_Framework.frame_time
            elif self.B_y < fly_high.my_jet.y + 70:
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
        self.fire_sound = load_wav('resource/Sound/192.WAV')
        self.fire_sound.set_volume(30)
        self.a_x = fly_high.my_friend.A_x
        self.a_y = fly_high.my_friend.A_y
        self.b_x = fly_high.my_friend.B_x
        self.b_y = fly_high.my_friend.B_y
        self.bullet_dir = 0
        self.sign = 0
        pass


    def shoot(self):
        self.fire_sound.play()


    def update(self):
        if self.sign == 0:
            if self.bullet_dir == 1:
                self.a_x = fly_high.my_friend.A_x
                self.a_y = fly_high.my_friend.A_y + 60
            if self.bullet_dir == 2:
                self.b_x = fly_high.my_friend.B_x
                self.b_y = fly_high.my_friend.B_y + 60
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
            #draw_rectangle(*self.get_bb())
        if self.bullet_dir == 2:
            self.image.clip_draw(0, 0, 20, 30, self.b_x, self.b_y)
            #draw_rectangle(*self.get_bb())
        pass