from pico2d import *
import Game_Framework

import random
import time

PIXEL_PER_METER = (10.0 / 0.1)  # 10pixel 10cm
RUN_SPEED_KMPH_CLOUD = 1  # km/hour
RUN_SPEED_MPM_CLOUD = (RUN_SPEED_KMPH_CLOUD * 1000.0 / 60.0)
RUN_SPEED_MPS_CLOUD = (RUN_SPEED_MPM_CLOUD / 60.0)
RUN_SPEED_PPS_CLOUD = (RUN_SPEED_MPS_CLOUD * PIXEL_PER_METER)
class CLOUD:
    def __init__(self):
        self.cloud = load_image('resource/Aft_resource/cloud.png')
        self.x1, self.y1 = -300, 400
        self.x2, self.y2 = -700, 200
        pass

    def update(self):
        self.x1 += RUN_SPEED_PPS_CLOUD * Game_Framework.frame_time
        self.x2 += RUN_SPEED_PPS_CLOUD * Game_Framework.frame_time
        if self.x1 > 1500:
            self.x1 = random.randint(-400, -200)
            self.y1 = random.randint(400, 700)
        if self.x2 > 1500:
            self.x2 = random.randint(-600, -400)
            self.y2 = random.randint(100, 400)
        pass

    def draw(self):
        self.cloud.clip_draw(0, 0, 400, 250, self.x1, self.y1)
        self.cloud.clip_draw(0, 0, 400, 250, self.x2, self.y2)
        pass