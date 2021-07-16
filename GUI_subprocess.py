#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import tkinter as tk
import subprocess as sp

def record_start():
    global procA
    procA = sp.Popen(['python3', 'record_video.py'])
    
def record_stop():
    global procA
    procA.terminate()
    procA = None
    
def scale_val(val):
    f = open("./val.txt",'w')
    f.write(val)
    f.close()
    
procA = None

root = tk.Tk()

root.geometry("640x640+100+100")  #너비X높이+X좌표+Y좌표
root.resizable(True, True)        #사이즈 변경 가능

label1 = tk.Label(root, text="Auto Tracking Video",width=50,height=3)
label1.pack(anchor=tk.CENTER, expand=True)

button1 = tk.Button(root, text="record_start",width=50,height=5 ,command=record_start)
button1.pack(anchor=tk.CENTER, expand=True)

button2 = tk.Button(root, text="record_stop",width=50,height=5 ,command=record_stop)
button2.pack(anchor=tk.CENTER, expand=True)

scale=tk.Scale(root, command=scale_val, orient="horizontal",showvalue=True, tickinterval=30,from_=60, to=360, length=360)
scale.set(180)
scale.pack()

root.mainloop()
