from cv2 import VideoCapture, circle, putText, FONT_HERSHEY_COMPLEX_SMALL, imshow, waitKey
from Module import PoseDetector
from time import time

cam = VideoCapture('rtsp://admin:BRGOII@192.168.247.55:554/Streaming/Channels/102')
det = PoseDetector().ProccessMultiple

s = time()

while True:
    _, frame = cam.read()
    e = time()
    if (1 / (e - s) > 20):
        continue
    s = e
    cs = det(frame)
    for ix, (cx, cy) in enumerate(cs):
        circle(frame, (cx, cy), 50, (0, 0, 255), 1)
        putText(frame, f"{ix}", (cx - 25, cy + 25), 1, FONT_HERSHEY_COMPLEX_SMALL, (0, 0, 0), 1)
    imshow('Mat', frame)
    waitKey(1)