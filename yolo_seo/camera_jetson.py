# -*- coding:utf-8 -*-

import cv2


def gstreamer_pipline(
    capture_width=1280,
    capture_height=720,
    display_width=640,
    display_height=480,
    framerate=60,
    flip_method=0
):
    return(
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(gstreamer_pipline(flip_method=0), cv2.CAP_GSTREAMER)
    
    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.video.read()
        return frame

        return frame
    def show_camera(self):
        if self.video.isOpened():
            window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
            while cv2.getWindowProperty("CSI Camera", 0) >= 0:
                img = self.get_frame()
                cv2.imshow("CSI Camera", img)
                
                # key = cv2.waitKey(30) & 0xFF
                # if key == 27:
                #     break
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
        else:
            print("Unable to Use Camera")
