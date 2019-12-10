from pico2d import *
import Game_Framework

import random
import time
import fly_high

class PLAYTIME:
    def __init__(self):
        self.font = load_font('resource/ENCR10B.TTF', 20)
        self.NowTime = 0
        pass

    def update(self):
        pass

    def draw(self):
        self.NowTime = time.time() - fly_high.First_Time
        self.font.draw(650, 580, '(Time: %3.2f)' % self.NowTime, (255, 0, 128))
        pass