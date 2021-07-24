# -*- coding:utf-8 -*-

import servo
from threading import Timer

class Controler():
    def __init__(self, width=480, height=320, fps=6):
        self.servo = servo.Servo()
        self.width = width
        self.height = height
        self.fps = fps

    def control(self,x1,y1,x2,y2):
        x_mid = self.width/2
        y_mid = self.height/2
        x_cor = (x1+x2)/2
        y_cor = (y1+y2)/2
        x_thr = self.width/15
        y_thr = self.height/15
        res = (x_thr + y_thr)/2

        # 중앙과 얼굴 위치의 차이값
        x_diff = x_mid - x_cor
        y_diff = y_mid - y_cor

        x_ang = abs(int(x_diff/res))
        x_delay = 1.0/self.fps/x_ang

        y_ang = abs(int(y_diff/res))
        y_delay = 1.0/self.fps/y_ang

        if x_diff >= x_thr:
            for i in range(x_ang):
                t = Timer(x_delay*i,servo.rotate_right,args=[1])
                t.start()
        if x_diff <= -x_thr:
            for i in range(x_ang):
                t = Timer(x_delay*i,servo.rotate_left,args=[1])
                t.start()
        if y_diff >= y_thr:
            for i in range(y_ang):
                t = Timer(y_delay*i,servo.rotate_up,args=[1])
                t.start()
        if y_diff <= -y_thr:
            for i in range(y_ang):
                t = Timer(y_delay*i,servo.rotate_down,args=[1])
                t.start()