#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from adafruit_servokit import ServoKit

# 서보모터 클래스
class Servo:

    # 서보모터 변수 설정
    ang_ver_min = 25
    ang_ver_max = 155
    ang_hor_min = 0
    ang_hor_max = 180
    ang_ver = 90
    ang_hor = 90
    channel_hor = 0
    channel_ver = 1


    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.set_angle(self.channel_hor,self.ang_hor)
        self.set_angle(self.channel_ver,self.ang_ver)

    # 서보모터 각도 변경 함수 (채널, 각도)
    def set_angle(self,channel,ang):
        self.kit.servo[channel].angle = ang
    
    # 서보모터 좌로 회전 (각도)
    def rotate_left(self,ang):
        self.ang_hor -= ang
        if self.ang_hor < self.ang_hor_min:
            self.ang_hor = self.ang_hor_min
        self.set_angle(self.channel_hor,self.ang_hor)

    # 서보모터 우로 회전 (각도)
    def rotate_right(self,ang):
        self.ang_hor += ang
        if self.ang_hor > self.ang_hor_max:
            self.ang_hor = self.ang_hor_max
        self.set_angle(self.channel_hor,self.ang_hor)

    # 서보모터 위로 회전 (각도)
    def rotate_up(self,ang):
        self.ang_ver += ang
        if self.ang_ver > self.ang_ver_max:
            self.ang_ver = self.ang_ver_max
        self.set_angle(self.channel_ver,self.ang_ver)

    # 서보모터 아래로 회전 (각도)
    def rotate_down(self,ang):
        self.ang_ver -= ang
        if self.ang_ver < self.ang_ver_min:
            self.ang_ver = self.ang_ver_min
        self.set_angle(self.channel_ver,self.ang_ver)
