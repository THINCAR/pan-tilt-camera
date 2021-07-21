# face_recog.py

import face_recognition
import cv2
import imutils

import camera
import os
import numpy as np
import servo

class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.camera = camera.VideoCamera()

        self.known_face_encodings = []
        self.known_face_names = []

        # Load sample pictures and learn how to recognize it.
        dirname = 'knowns'
        files = os.listdir(dirname)
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext == '.jpg':
                self.known_face_names.append(name)
                pathname = os.path.join(dirname, filename)
                img = face_recognition.load_image_file(pathname)
                face_encoding = face_recognition.face_encodings(img)[0]
                self.known_face_encodings.append(face_encoding)

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        self.error_tolerance_frame1 = 30

    def __del__(self):
        del self.camera

    def get_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()

        # Resize frame of video to 1/4 size for faster face recognition processing
        # small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # 얼굴 인식 모델 로드
        face_detector = "./face_detector/"
        prototxt = face_detector + "deploy.prototxt"  # prototxt 파일 : 모델의 레이어 구성 및 속성 정의
        weights = face_detector + "res10_300x300_ssd_iter_140000.caffemodel"  # caffemodel 파일 : 얼굴 인식을 위해 ResNet 기본 네트워크를 사용하는 SSD(Single Shot Detector) 프레임워크를 통해 사전 훈련된 모델 가중치 사용
        net = cv2.dnn.readNet(prototxt, weights)  # cv2.dnn.readNet() : 네트워크를 메모리에 로드
        # 인식할 최소 확률
        minimum_confidence = 0.5
        # 얼굴 검출 프레임 resize
        detection_frame = imutils.resize(frame, width=400)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = detection_frame[:, :, ::-1]
        # 이미지 크기
        (H, W) = detection_frame.shape[:2]
        # blob 이미지 생성
        blob = cv2.dnn.blobFromImage(detection_frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        # 얼굴 인식
        net.setInput(blob)  # setInput() : blob 이미지를 네트워크의 입력으로 설정
        detections = net.forward()  # forward() : 네트워크 실행(얼굴 인식)
        # 얼굴 번호
        number = 0

        # Only process every other frame of video to save time
        # if self.process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            min_value = min(distances)

            # tolerance: How much distance between faces to consider it a match. Lower is more strict.
            # 0.6 is typical best performance.
            name = "Unknown"
            if min_value < 0.6:
                index = np.argmin(distances)
                name = self.known_face_names[index]

            self.face_names.append(name)

        # 얼굴 인식을 위한 반복
        for i in range(0, detections.shape[2]):
            # 얼굴 인식 확률 추출
            confidence = detections[0, 0, i, 2]

            # 얼굴 인식 확률이 최소 확률보다 큰 경우
            if confidence > minimum_confidence:
                # bounding box 위치 계산
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")

                # bounding box 가 전체 좌표 내에 있는지 확인
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(W - 1, endX), min(H - 1, endY))

                cv2.putText(detection_frame, "Face[{}]".format(number + 1), (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)  # 얼굴 번호 출력
                cv2.rectangle(detection_frame, (startX, startY), (endX, endY), (255, 0, 0), 2)  # bounding box 출력

                # 사용자 얼굴 중심점 찾아서 표시하기.
                my_face_center_x = (endX + startX) // 2
                my_face_center_y = (endY + startY) // 2
                cv2.line(detection_frame, (my_face_center_x, my_face_center_y), (my_face_center_x, my_face_center_y), (255, 0, 0),
                         3)

                number = number + 1  # 얼굴 번호 증가

        # 얼굴인식된 모습 표시하기
        # for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
        #     cv2.rectangle(detection_frame, (left, top), (right, bottom), (0, 0, 255), 2)
        #     cv2.putText(detection_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # 영상에 초록색 원과 점 찍기위한 용도임.
        width, height = 400, 225  # 225 = 720(카메라 입력 높이값)/1280(카메라 입력 너비값)*400(얼굴 검출하기 쉽도록 너비를 400으로 리사이즈시킴)
        # horizontal_value
        f = open("horizontal_value.txt", 'r')
        data2 = f.read()
        horizontal_value = int(data2)
        f.close()
        # vertical_value
        f = open("vertical_value.txt", 'r')
        data1 = f.read()
        vertical_value = int(data1)
        f.close()

        width = int(width * (horizontal_value/100))
        height = int(height * (vertical_value/100))

        cv2.line(detection_frame, (width, height), (width, height), (0, 255, 0), 1)
        radius = self.error_tolerance_frame1
        cv2.circle(detection_frame, (width, height), radius, (0, 255, 0), 1)

        detection_frame = imutils.resize(detection_frame, height=410, width=768)

        # self.process_this_frame = not self.process_this_frame

        return detection_frame

    def error_tolerance_frame(self):
        # Grab a single frame of video
        frame = self.camera.get_frame()
        frame1_move_x = 0
        frame1_move_y = 0

        # 얼굴 인식 모델 로드
        face_detector = "./face_detector/"
        prototxt = face_detector + "deploy.prototxt"  # prototxt 파일 : 모델의 레이어 구성 및 속성 정의
        weights = face_detector + "res10_300x300_ssd_iter_140000.caffemodel"  # caffemodel 파일 : 얼굴 인식을 위해 ResNet 기본 네트워크를 사용하는 SSD(Single Shot Detector) 프레임워크를 통해 사전 훈련된 모델 가중치 사용
        net = cv2.dnn.readNet(prototxt, weights)  # cv2.dnn.readNet() : 네트워크를 메모리에 로드
        # 인식할 최소 확률
        minimum_confidence = 0.5
        # 얼굴 검출 프레임 resize
        detection_frame = imutils.resize(frame, width=400)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = detection_frame[:, :, ::-1]
        # 이미지 크기
        (H, W) = detection_frame.shape[:2]
        # blob 이미지 생성
        blob = cv2.dnn.blobFromImage(detection_frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        # 얼굴 인식
        net.setInput(blob)  # setInput() : blob 이미지를 네트워크의 입력으로 설정
        detections = net.forward()  # forward() : 네트워크 실행(얼굴 인식)
        # 얼굴 번호
        number = 0

        # Only process every other frame of video to save time
        # if self.process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        self.face_names = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            min_value = min(distances)

            # tolerance: How much distance between faces to consider it a match. Lower is more strict.
            # 0.6 is typical best performance.
            name = "Unknown"
            if min_value < 0.6:
                index = np.argmin(distances)
                name = self.known_face_names[index]

            self.face_names.append(name)

        # 얼굴 인식을 위한 반복
        for i in range(0, detections.shape[2]):
            # 얼굴 인식 확률 추출
            confidence = detections[0, 0, i, 2]

            # 얼굴 인식 확률이 최소 확률보다 큰 경우
            if confidence > minimum_confidence:
                # bounding box 위치 계산
                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")

                # bounding box 가 전체 좌표 내에 있는지 확인
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(W - 1, endX), min(H - 1, endY))

                # 얼굴 중심점과의 오차를 구하기 위한 사전코드
                my_face_center_x = (endX + startX) // 2
                my_face_center_y = (endY + startY) // 2

                # 영상에서 프레임 센터를 구하기 위함.
                width, height = 400, 225  # 225 = 720(카메라 입력 높이값)/1280(카메라 입력 너비값)*400(얼굴 검출하기 쉽도록 너비를 400으로 리사이즈시킴)
                # horizontal_value
                f = open("horizontal_value.txt", 'r')
                data2 = f.read()
                horizontal_value = int(data2)
                f.close()
                # vertical_value
                f = open("vertical_value.txt", 'r')
                data1 = f.read()
                vertical_value = int(data1)
                f.close()

                frame_center_x = int(width * (horizontal_value / 100))
                frame_center_y = int(height * (vertical_value / 100))

                frame1_move_x = frame_center_x - my_face_center_x
                frame1_move_y = frame_center_y - my_face_center_y
                error_ref = ((frame1_move_x)**2 + (frame1_move_y)**2)**0.5
                if error_ref <= self.error_tolerance_frame1:
                    frame1_move_x, frame1_move_y = 0, 0

        return frame1_move_x, frame1_move_y

    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()

    def change_error_tolerance_value(self, value):
        self.error_tolerance_frame1 = value
        return True


if __name__ == '__main__':
    face_recog = FaceRecog()
    servo = servo.Servo()
    print(face_recog.known_face_names)

    # 오차허용프레임 반지름 값 변경하기
    f = open("error_tolerance_value.txt", 'r')
    data = f.read()
    face_recog.change_error_tolerance_value(int(data))
    f.close()

    while True:
        frame = face_recog.get_frame()
        # show the frame
        cv2.imshow("Frame", frame)

        # 사용자 얼굴 중심점과의 오차 프린트문
        f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
        print("x좌표 : ", f1_move_x, ", ", "y좌표 : ", f1_move_y)

        if (f1_move_x > 0) and (f1_move_y > 0):
            while True:
                f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
                if (f1_move_x == 0) and (f1_move_y == 0):
                    break
                if abs(f1_move_x) >= 100:
                    move_x = abs(f1_move_x) // 100
                elif abs(f1_move_x) >= 50:
                    move_x = abs(f1_move_x) // 50
                elif abs(f1_move_x) >= 25:
                    move_x = abs(f1_move_x) // 25
                else:
                    move_x = abs(f1_move_x) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                if abs(f1_move_y) >= 100:
                    move_y = abs(f1_move_y) // 100
                elif abs(f1_move_y) >= 50:
                    move_y = abs(f1_move_y) // 50
                elif abs(f1_move_y) >= 25:
                    move_y = abs(f1_move_y) // 25
                else:
                    move_y = abs(f1_move_y) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                servo.rotate_right(move_x)
                servo.rotate_up(move_y)

        elif (f1_move_x > 0) and (f1_move_y < 0):
            while True:
                f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
                if (f1_move_x == 0) and (f1_move_y == 0):
                    break
                if abs(f1_move_x) >= 100:
                    move_x = abs(f1_move_x) // 100
                elif abs(f1_move_x) >= 50:
                    move_x = abs(f1_move_x) // 50
                elif abs(f1_move_x) >= 25:
                    move_x = abs(f1_move_x) // 25
                else:
                    move_x = abs(f1_move_x) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                if abs(f1_move_y) >= 100:
                    move_y = abs(f1_move_y) // 100
                elif abs(f1_move_y) >= 50:
                    move_y = abs(f1_move_y) // 50
                elif abs(f1_move_y) >= 25:
                    move_y = abs(f1_move_y) // 25
                else:
                    move_y = abs(f1_move_y) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                servo.rotate_right(move_x)
                servo.rotate_down(move_y)

        elif (f1_move_x < 0) and (f1_move_y < 0):
            while True:
                f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
                if (f1_move_x == 0) and (f1_move_y == 0):
                    break
                if abs(f1_move_x) >= 100:
                    move_x = abs(f1_move_x) // 100
                elif abs(f1_move_x) >= 50:
                    move_x = abs(f1_move_x) // 50
                elif abs(f1_move_x) >= 25:
                    move_x = abs(f1_move_x) // 25
                else:
                    move_x = abs(f1_move_x) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                if abs(f1_move_y) >= 100:
                    move_y = abs(f1_move_y) // 100
                elif abs(f1_move_y) >= 50:
                    move_y = abs(f1_move_y) // 50
                elif abs(f1_move_y) >= 25:
                    move_y = abs(f1_move_y) // 25
                else:
                    move_y = abs(f1_move_y) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                servo.rotate_left(move_x)
                servo.rotate_down(move_y)

        elif (f1_move_x < 0) and (f1_move_y > 0):
            while True:
                f1_move_x, f1_move_y = face_recog.error_tolerance_frame()
                if (f1_move_x == 0) and (f1_move_y == 0):
                    break
                if abs(f1_move_x) >= 100:
                    move_x = abs(f1_move_x) // 100
                elif abs(f1_move_x) >= 50:
                    move_x = abs(f1_move_x) // 50
                elif abs(f1_move_x) >= 25:
                    move_x = abs(f1_move_x) // 25
                else:
                    move_x = abs(f1_move_x) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                if abs(f1_move_y) >= 100:
                    move_y = abs(f1_move_y) // 100
                elif abs(f1_move_y) >= 50:
                    move_y = abs(f1_move_y) // 50
                elif abs(f1_move_y) >= 25:
                    move_y = abs(f1_move_y) // 25
                else:
                    move_y = abs(f1_move_y) // 13  # 13보다 작은 값이 들어오면 무조건 0으로 반환되는 것 주의!

                servo.rotate_left(move_x)
                servo.rotate_up(move_y)

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    # do a bit of cleanup
    cv2.destroyAllWindows()
    print('finish')