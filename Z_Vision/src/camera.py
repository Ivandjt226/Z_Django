"""
import time
from base_camera import BaseCamera


class Camera(BaseCamera):
    #An emulated camera implementation that streams a repeated sequence of
    #files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second.
    imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    @staticmethod
    def frames():
        while True:
            yield Camera.imgs[int(time.time()) % 3]
            time.sleep(1)

"""

import cv2
#from fem import FacialExpressionModel
import numpy as np


facec = cv2.CascadeClassifier('./models/detection_models/haarcascade_frontalface_default.xml')
#model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            #pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

            #cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()