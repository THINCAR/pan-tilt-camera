#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# 서보모터 최소각 최대각 설정
ang_min = 25
ang_max = 155

# set_angle function
def set_angle(channel,ang):
	kit.servo[channel].angle = ang



# test code
sweep = range(ang_min,ang_max)
sweep_inv = range(ang_max,ang_min,-1)

while True:
  for degree in sweep:
	  set_angle(0,degree)
	  set_angle(1,degree)
	  time.sleep(0.01)
  for degree in sweep_inv:
    set_angle(0,degree)
    set_angle(1,degree)
    time.sleep(0.01)