# pan-tilt-camera
pan-tilt-camera with face localization and tracking

## Module1 : Face_recognition

### 1. OpenCV Face_Recognition

### 2.

### 3. 

## Module2 : Servo
* PWM 드라이버를 제어하여 서보모터의 pan, tilt 기능을 수행한다.
* panning 각도 (0~180)
* tilting 각도 (25~155)
### 내부 구조
* initialize : servo.Servo()
* method : 
    * set_angle(channel, angle)
    * rotate_left(angle)
    * rotate_right(angle)
    * rotate_up(angle)
    * rotate_down(angle)

## Module3 : Control
* 프레임 사이즈와, fps, 목표물의 좌표 정보를 바탕으로 위치, 속도 등을 부드럽게 제어한다.
* 예) fps가 10일 때 10도를 움직여야 할 경우, 1/100초에 1도씩 움직여서 10도를 부드럽게 움직인다.
### Structure
* initialize : control.Controler(width, height, fps)
* method:
    * control(x1,y1,x2,y2)