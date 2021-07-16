import sys
import cv2
import time
import face_recog

secs = time.time()
tm = time.localtime(secs)
start_time = str(tm.tm_year) + '-' + str(tm.tm_mon) + '-' + str(tm.tm_mday) + '-' + str(tm.tm_hour) + ':' + str(
    tm.tm_min) + ':' + str(tm.tm_sec)

dispW = 960
dispH = 540
frame_rate = 10
flip = 0

camSet = ' nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=' + str(
    frame_rate) + '/1 ! nvvidconv flip-method=' + str(flip) + ' ! video/x-raw, width=' + str(dispW) + ', height=' + str(
    dispH) + ', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

camera = cv2.VideoCapture(camSet)

if not camera.isOpened():
    print("Camera open failed!")
    sys.exit()

w = round(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
h = round(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
delay = round(1000 / fps)

out = cv2.VideoWriter('record/' + start_time + '.avi', fourcc, fps, (w, h))

if not out.isOpened():
    print('File open failed!')
    camera.release()
    sys.exit()

img_itr = 0

face_recog = face_recog.FaceRecog()
while True:
    frame = face_recog.get_frame()

    cv2.imshow('cam', frame)
    # cv2.imwrite('imgs/'+str(img_itr)+'.png', frame)

    # 반지름 150인 원이 오차허용프레임일 경우의 움직여야하는 x, y 좌표값
    f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
    print("x좌표 : ", f1_move_x, ", ", "y좌표 : ", f1_move_y)

    out.write(frame)

    if cv2.waitKey(1) == ord('q'):
        break

    img_itr += 1

camera.release()
out.release()
cv2.destroyAllWindows()