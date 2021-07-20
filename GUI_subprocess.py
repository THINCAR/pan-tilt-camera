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
    
def vertical_value(val):
    f = open("./vertical_value.txt",'w')
    f.write(val)
    f.close()
    

def horizontal_value(val):
    f = open("./horizontal_value.txt",'w')
    f.write(val)
    f.close()
    
root = tk.Tk()

root.title("Auto Tracking Video")
root.geometry("1024x600+0+0")  #너비X높이+X좌표+Y좌표
root.resizable(True, True)        #사이즈 변경 가능

scale1=tk.Scale(root, command=vertical_value, orient="vertical",showvalue=True, tickinterval=30,from_=0, to=432, length=432)
scale1.set(216)
scale1.grid(column=0, row=0)

button1 = tk.Button(root, text="record_start",width=20,height=3 ,command=record_start)
button1.grid(column=0, row=1)

button2 = tk.Button(root, text="record_stop",width=20,height=3 ,command=record_stop)
button2.grid(column=0, row=2)

scale2=tk.Scale(root, command=horizontal_value, orient="horizontal",showvalue=True, tickinterval=30,from_=0, to=768, length=768)
scale2.set(384)
scale2.grid(column=1, row=2)




root.mainloop()
