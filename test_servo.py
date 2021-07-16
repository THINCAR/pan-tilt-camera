#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from servo import Servo

servo = Servo()
servo.rotate_left(100)
time.sleep(1)
servo.rotate_right(180)
time.sleep(1)
servo.rotate_left(180)
time.sleep(1)
servo.rotate_right(180)
time.sleep(1)
servo.rotate_up(180)
time.sleep(1)
servo.rotate_down(180)
