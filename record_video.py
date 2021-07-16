import cv2
import time

secs = time.time()
tm = time.localtime(secs)
start_time = str(tm.tm_year)+'-'+str(tm.tm_mon)+'-'+str(tm.tm_mday)+'-'+str(tm.tm_hour)+':'+str(tm.tm_min)+':'+str(tm.tm_sec)

dispW = 960
dispH = 540
frame_rate = 10
flip = 0

camSet =' nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate='+str(frame_rate)+'/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

camera = cv2.VideoCapture(camSet)

if not camera.isOpened():
  print("Camera open failed!")
  sys.exit()

w = round(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
delay = round(1000/fps)

out = cv2.VideoWriter('record/'+start_time+'.avi', fourcc, fps, (w, h))

if not out.isOpened():
  print('File open failed!')
  camera.release()
  sys.exit()

img_itr = 0
while True:
  ret, frame =  camera.read()

  cv2.imshow('cam', frame)
  #cv2.imwrite('imgs/'+str(img_itr)+'.png', frame)
  out.write(frame)
  
  if cv2.waitKey(1) == ord('q'):
    break

  img_itr += 1

camera.release()
out.release()
cv2.destroyAllWindows()

